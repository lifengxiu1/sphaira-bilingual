import copy
import json
import unittest
from pathlib import Path

from prepare import make_categories


ROOT = Path(__file__).resolve().parent


class CategoryTests(unittest.TestCase):
    def setUp(self):
        self.catalog = json.loads((ROOT / "catalog-original.json").read_text(encoding="utf-8"))
        self.overrides = json.loads((ROOT / "categories.json").read_text(encoding="utf-8"))

    def test_every_package_is_classified_without_changing_metadata(self):
        original = copy.deepcopy(self.catalog)
        categories = make_categories(self.catalog, self.overrides)
        self.assertEqual(self.catalog, original)
        self.assertTrue(set(self.catalog["packages"][i]["name"] for i in range(511)).issubset(categories))
        self.assertEqual({"Games", "GameTools", "Emulators", "SystemTools", "MediaNetwork", "Other"}, set(categories.values()))

    def test_game_helpers_media_and_installed_apps(self):
        categories = make_categories(self.catalog, self.overrides)
        for name in ("jksv", "TranslateNX", "FPSLocker", "MissionControl", "sys-clk"):
            self.assertEqual("GameTools", categories[name], name)
        self.assertEqual("Games", categories["OpenTTD"])
        self.assertEqual("Games", categories["snek"])
        self.assertEqual("Emulators", categories["mGBA"])
        self.assertEqual("MediaNetwork", categories["Moonlight-Switch"])
        self.assertEqual("Other", categories["Calculator_NX"])
        self.assertEqual("GameTools", categories["/switch/TranslateNX.nro"])
        self.assertEqual("SystemTools", categories["/switch/haze.nro"])

    def test_unknown_duplicate_and_invalid_overrides_are_rejected(self):
        for overrides in ({"Games": ["not-in-catalog"]}, {"Games": ["jksv"], "GameTools": ["jksv"]}, {"Invalid": ["jksv"]}):
            with self.subTest(overrides=overrides), self.assertRaises(ValueError):
                make_categories(self.catalog, overrides)


if __name__ == "__main__":
    unittest.main()
