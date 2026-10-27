import copy
import json
import tempfile
import unittest
from pathlib import Path

from prepare import load_translations, make_labels


ROOT = Path(__file__).resolve().parent


class TranslationTests(unittest.TestCase):
    def test_complete_catalog_and_metadata_preserved(self):
        catalog = json.loads((ROOT / "catalog-original.json").read_text(encoding="utf-8"))
        original = copy.deepcopy(catalog)
        translations = load_translations(ROOT / "catalog-zh.tsv")
        labels = make_labels(catalog, translations)
        self.assertEqual(511, len(translations))
        self.assertEqual(catalog, original)
        for package in catalog["packages"]:
            self.assertIn(f"catalog.name.{package['name']}", labels)
            self.assertIn(f"catalog.description.{package['name']}", labels)
        self.assertEqual("USB 文件传输", labels["homebrew.name./switch/haze.nro"])
        self.assertEqual("自制菜单与商店", labels["homebrew.name./switch/sphaira/sphaira.nro"])
        self.assertEqual("", labels.get("catalog.name.future-unknown-app", ""))

    def test_missing_package_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "do not match"):
            make_labels({"packages": [{"name": "missing"}]}, {})

    def test_duplicate_and_invalid_translation_rows_are_rejected(self):
        for content in ("a\t名称\t简介\na\t名称\t简介\n", "a\tName\tDescription\n", "a\t名称\n"):
            with self.subTest(content=content), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "labels.tsv"
                path.write_text(content, encoding="utf-8")
                with self.assertRaises(ValueError):
                    load_translations(path)


if __name__ == "__main__":
    unittest.main()
