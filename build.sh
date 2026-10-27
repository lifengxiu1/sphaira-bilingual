#!/usr/bin/env bash
set -euo pipefail

package_dir=$(cd "$(dirname "$0")" && pwd)
cd "$package_dir"
python3 -m unittest discover -p 'test_*.py' -v
python3 - <<'PY'
import hashlib, json
from pathlib import Path
for name, expected in json.loads(Path('input-sha256.json').read_text()).items():
    actual = hashlib.sha256(Path(name).read_bytes()).hexdigest()
    if actual != expected:
        raise SystemExit(f'Input digest mismatch: {name}')
PY

fetch_commit() {
    git init "$3"
    git -C "$3" remote add origin "$1"
    git -C "$3" fetch --depth 1 origin "$2"
    git -C "$3" checkout --detach FETCH_HEAD
    test "$(git -C "$3" rev-parse HEAD)" = "$2"
}

fetch_commit https://github.com/NaGaa95/sphaira.git 338348e74b6d278bc570a9be5373d25197bf6c8d upstream
git -C upstream apply --check "$package_dir/source.patch"
git -C upstream apply "$package_dir/source.patch"
python3 prepare.py --catalog catalog-original.json --source upstream
g++ -std=c++20 -Wall -Wextra -Werror -I upstream/sphaira/include upstream/sphaira/source/app_category.cpp test_categories.cpp -o /tmp/category-tests
/tmp/category-tests

fetch_commit https://github.com/switchbrew/libnx.git b156b4774fb2df7b93402169509266da7547fc4c libnx
git -C libnx submodule update --init --recursive --depth 1
fetch_commit https://github.com/R-YaTian/newlib.git 8e4d4166b043622b1fe463dbdb8255a05f0d56b2 newlib

(cd newlib && bash build-libgloss-local.sh)
make -C libnx install -j"$(nproc)"
(cd upstream && cmake --preset Release -Dsphaira_VERSION_OVERRIDE=1.0.8-zhcat)
cmake --build upstream/build/Release --parallel "$(nproc)"

mkdir -p dist/package/switch/sphaira
cp upstream/build/Release/sphaira.nro dist/package/switch/sphaira/
(cd dist/package && zip -r ../sphaira-bilingual-1.0.8.zip switch)
git -C upstream archive --format=zip --prefix=sphaira/ HEAD > dist/sphaira-source-base.zip
python3 - <<'PY'
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
root = Path('upstream')
with ZipFile('dist/sphaira-source-base.zip') as original:
    with ZipFile('dist/sphaira-bilingual-source.zip', 'w', ZIP_DEFLATED) as result:
        for info in original.infolist():
            relative = info.filename.removeprefix('sphaira/')
            path = root / relative
            if not info.is_dir() and path.is_file():
                result.writestr(info.filename, path.read_bytes())
        for name in ('sphaira/source/bilingual_zh.inc', 'sphaira/source/app_categories.inc',
                     'sphaira/include/app_category.hpp', 'sphaira/source/app_category.cpp'):
            result.write(root / name, 'sphaira/' + name)
PY
(cd dist && sha256sum sphaira-bilingual-1.0.8.zip sphaira-bilingual-source.zip > SHA256SUMS.txt)
