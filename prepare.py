"""Generate display-only labels from public HB App Store metadata (stdlib only)."""

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


CATEGORY_TITLES = {
    "Games": "游戏", "GameTools": "游戏工具", "Emulators": "模拟器",
    "SystemTools": "系统工具", "MediaNetwork": "影音网络", "Other": "其他",
}


def make_categories(catalog: dict, overrides: dict) -> dict[str, str]:
    defaults = {"game": "Games", "emu": "Emulators", "tool": "SystemTools",
                "advanced": "SystemTools", "theme": "SystemTools"}
    categories = {package["name"]: defaults.get(package.get("category"), "Other")
                  for package in catalog["packages"]}
    if len(categories) != len(catalog["packages"]):
        raise ValueError("Duplicate catalog package IDs")
    assigned = set()
    for category, names in overrides.items():
        if category not in CATEGORY_TITLES or not isinstance(names, list):
            raise ValueError(f"Invalid category: {category}")
        for name in names:
            if name not in categories or name in assigned:
                raise ValueError(f"Unknown or duplicate category override: {name}")
            assigned.add(name)
            categories[name] = category

    for package in catalog["packages"]:
        binary = package.get("binary", "").removeprefix("sdmc:")
        if binary.startswith("/") and binary.endswith(".nro"):
            category = categories[package["name"]]
            if binary in categories and categories[binary] != category:
                raise ValueError(f"Conflicting categories for binary: {binary}")
            categories[binary] = category
    for path in ("/switch/daybreak.nro", "/switch/haze.nro", "/switch/reboot_to_payload.nro",
                 "/switch/appstore/appstore.nro", "/switch/sphaira/sphaira.nro"):
        categories[path] = "SystemTools"
    categories["/switch/TranslateNX.nro"] = "GameTools"
    return categories


def load_translations(path: Path) -> dict[str, tuple[str, str]]:
    translations = {}
    with path.open(encoding="utf-8", newline="") as stream:
        for row in csv.reader(stream, delimiter="\t"):
            if len(row) != 3 or not all(row):
                raise ValueError(f"Expected three nonempty columns: {row!r}")
            package_id, label, description = row
            if package_id in translations:
                raise ValueError(f"Duplicate package ID: {package_id}")
            if not all(any("\u3400" <= char <= "\u9fff" for char in text)
                       for text in (label, description)):
                raise ValueError(f"Missing Chinese text: {package_id}")
            translations[package_id] = label, description
    return translations


def make_labels(catalog: dict, translations: dict) -> dict[str, str]:
    packages = catalog["packages"]
    package_ids = [package["name"] for package in packages]
    if len(package_ids) != len(set(package_ids)):
        raise ValueError("Duplicate package IDs in catalog")
    if set(package_ids) != set(translations):
        raise ValueError("Catalog and translation IDs do not match")

    labels = {}
    for package in packages:
        package_id = package["name"]
        label, description = translations[package_id]
        labels[f"catalog.name.{package_id}"] = label
        labels[f"catalog.description.{package_id}"] = description
        binary = package.get("binary", "")
        if binary.startswith("sdmc:"):
            binary = binary[5:]
        if binary.startswith("/") and binary.endswith(".nro"):
            # shortcut: shared binary paths use the first catalog label; split if their purpose differs.
            labels.setdefault(f"homebrew.name.{binary}", label)

    for path, label in {
        "/switch/daybreak.nro": "系统更新工具",
        "/switch/haze.nro": "USB 文件传输",
        "/switch/reboot_to_payload.nro": "重启进入引导菜单",
        "/switch/TranslateNX.nro": "游戏实时翻译",
        "/switch/appstore/appstore.nro": "自制软件商店",
        "/switch/sphaira/sphaira.nro": "自制菜单与商店",
    }.items():
        labels[f"homebrew.name.{path}"] = label
    labels.update({"Category": "分类", "All": "全部", "Games": "游戏",
                   "Game Tools": "游戏工具", "Emulators": "模拟器", "System Tools": "系统工具",
                   "Media & Network": "影音网络", "Other": "其他",
                   "No installed apps in this category": "此分类暂无已安装应用"})
    return labels


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    args = parser.parse_args()
    directory = Path(__file__).resolve().parent
    translations = load_translations(directory / "catalog-zh.tsv")
    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    labels = make_labels(catalog, translations)
    target = args.source / "sphaira/source/bilingual_zh.inc"
    if not target.parent.is_dir():
        raise ValueError("Not a Sphaira source checkout")
    text = "// Generated from catalog-zh.tsv; display text only.\n"
    text += "".join(
        "    {" + json.dumps(key, ensure_ascii=False) + ", "
        + json.dumps(value, ensure_ascii=False) + "},\n"
        for key, value in sorted(labels.items())
    )
    target.write_text(text, encoding="utf-8", newline="\n")
    overrides = json.loads((directory / "categories.json").read_text(encoding="utf-8"))
    categories = make_categories(catalog, overrides)
    category_text = "// Generated from the public catalog and categories.json.\n"
    category_text += "".join("    {" + json.dumps(key, ensure_ascii=False) + ", Type::" + value + "},\n"
                             for key, value in sorted(categories.items()))
    (target.parent / "app_categories.inc").write_text(category_text, encoding="utf-8", newline="\n")
    counts = Counter(categories[package["name"]] for package in catalog["packages"])
    preview = ["# 应用分类", "", "本地自制应用和 Sphaira 内置商店使用相同的六类。在 X 菜单中选择分类。", ""]
    for category, title in CATEGORY_TITLES.items():
        preview += [f"## {title}（{counts[category]}）", "", "| 软件 | 用途 |", "|---|---|"]
        for package in catalog["packages"]:
            if categories[package["name"]] == category:
                label, description = translations[package["name"]]
                title = (package.get("title") or package["name"]).replace("|", "/")
                preview.append(f"| {label}（{title}） | {description} |")
        preview.append("")
    (directory / "分类.md").write_text("\n".join(preview), encoding="utf-8", newline="\n")
    print(f"Validated {len(translations)} packages; generated {len(labels)} labels")
    print("Categories: " + json.dumps(counts, ensure_ascii=False))


if __name__ == "__main__":
    main()
