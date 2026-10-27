# 自行开发

本仓库保存定制补丁与构建输入。完整 Sphaira 源码在构建时从固定提交取得；每个公开 Release 同时提供与二进制对应的修改后源码压缩包。

## 目录

| 文件 | 修改场景 |
|---|---|
| `catalog-original.json` | 公开商店目录快照，保留原始 ID、路径、来源与元数据 |
| `catalog-zh.tsv` | 三列：包 ID、中文用途名称、中文简介，无标题行 |
| `categories.json` | 六类中的显式用途覆盖，其余条目按原始类别推导 |
| `prepare.py` | 生成中英标签表、C++ 分类表和 `分类.md` |
| `source.patch` | 相对固定上游提交的 C++ 与构建配置改动 |
| `input-sha256.json` | 四个构建输入文件的 SHA-256，修改输入后需要更新 |
| `test_*.py` / `test_categories.cpp` | 数据校验与真实 C++ 分类器回归测试 |
| `build.sh` | 固定依赖提交、测试、交叉编译、安装包与源码包生成 |
| `.github/workflows/` | 数据检查及手动完整构建 |

## 方式一：Fork 后在 GitHub 编译

1. Fork 此仓库，在自己的仓库中修改译文、分类或源码补丁。
2. 修改了四个构建输入中的任意一个时，按下文更新校验表并提交。
3. 首次使用时在 **Actions** 页面启用工作流。
4. 选择 **Build bilingual Sphaira → Run workflow → main**。流程只接受手动触发，完整构建需要网络和 GitHub Actions 可用额度。
5. 成功后，到自己的 **Releases** 页面查看草稿；下载并核对安装包、对应源码和校验文件。自行真机验证后再发布草稿。

工作流使用 GitHub 自动提供的 `GITHUB_TOKEN` 发布草稿，不需要添加个人访问令牌。Pull Request 的数据检查只有读取权限，不发布附件。

## 方式二：本地准备源码

以下命令使用 Bash 和 Python 3.10 或更新版本。Windows 可在 Git Bash 中准备文件；完整编译建议使用 GitHub Actions，或配好 Docker / Linux devkitPro 环境。

```bash
git clone https://github.com/lifengxiu1/sphaira-bilingual.git
cd sphaira-bilingual
python3 -m unittest discover -p 'test_*.py' -v

git init upstream
git -C upstream remote add origin https://github.com/NaGaa95/sphaira.git
git -C upstream fetch --depth 1 origin 338348e74b6d278bc570a9be5373d25197bf6c8d
git -C upstream checkout --detach FETCH_HEAD
git -C upstream apply --check ../source.patch
git -C upstream apply ../source.patch
python3 prepare.py --catalog catalog-original.json --source upstream
```

这会在 `upstream/sphaira/source/` 生成 `bilingual_zh.inc` 和 `app_categories.inc`，不要手工修改这两个生成文件。

## 修改翻译或分类

- 修改 `catalog-zh.tsv`：保持包 ID 与快照完全一致，每行恰好三列，用 Tab 分隔；中文名称与中文简介均不能为空。
- 修改 `categories.json`：类别键为 `Games`、`GameTools`、`Emulators`、`SystemTools`、`MediaNetwork`、`Other`。覆盖项中每个包 ID 只能出现一次，且必须存在于目录快照。
- 补充本地路径：在 `prepare.py` 的本地名称与路径分类规则中增加对应路径，并更新相关测试。
- 更新目录快照：同时补齐所有新增 ID 的译文；当前测试使用 511 条基线，主动扩展快照时需同步调整数量断言，并审查删改的包 ID。

然后运行：

```bash
python3 -m unittest discover -p 'test_*.py' -v
python3 prepare.py --catalog catalog-original.json --source upstream
```

`分类.md` 由生成器更新；`预览.md` 是展示文档，改动译文后应同步更新相关内容。

## 修改 C++ 功能与更新补丁

当前补丁涉及 NRO 显示名、i18n 初始化、本地列表、商店、公共分类器和 CMake。原始 NACP 名称仍用于身份识别；用途标签只作用于显示。

修改 `upstream/` 下源码后，先将两个新源码文件标为 intent-to-add，再导出补丁，这样新文件也会包含在补丁里：

```bash
git -C upstream add -N -- sphaira/include/app_category.hpp sphaira/source/app_category.cpp
git -C upstream diff --no-ext-diff --binary > source.patch
```

不要对 `upstream` 使用 `git add -A` 后再导出补丁，避免把生成表或本地编译产物混进去。若新增其他源码，按同样方式将所需新文件加入补丁，并更新 CMake 及 `build.sh` 的源码包清单。

已有宿主 C++20 编译器时，运行实际分类器测试：

```bash
g++ -std=c++20 -Wall -Wextra -Werror -I upstream/sphaira/include \
  upstream/sphaira/source/app_category.cpp test_categories.cpp -o category-tests
./category-tests
```

## 更新输入校验表

在仓库根目录执行：

```bash
python3 - <<'PY'
import hashlib
import json
from pathlib import Path
names = ('source.patch', 'catalog-original.json', 'catalog-zh.tsv', 'categories.json')
hashes = {name: hashlib.sha256(Path(name).read_bytes()).hexdigest() for name in names}
Path('input-sha256.json').write_text(json.dumps(hashes, indent=2) + '\n', encoding='utf-8')
PY
```

仓库通过 `.gitattributes` 保持文本 LF 换行，避免跨平台换行导致补丁或输入哈希变化。请先检查实际改动，再更新哈希，不要用更新哈希掩盖意外文件变化。

## 完整编译与产物

`build.sh` 面向**全新的构建目录和已配置的 devkitPro 环境**，会创建 `upstream`、`libnx`、`newlib`；不要在已经准备过同名目录的工作区直接重复运行。推荐在 Fork 的 Actions 中运行，每次使用干净 runner。

Docker 已安装时，可在一份没有这些生成目录的干净仓库副本中运行与工作流相同的环境：

```bash
docker run --rm -v "$PWD:/workspace" -w /workspace devkitpro/devkita64:latest bash -lc '
  sudo -n apt-get update &&
  sudo -n apt-get install -y texinfo cmake zip python3 g++ &&
  git config --global --add safe.directory /workspace &&
  bash build.sh
'
```

输出在 `dist/`：

```text
dist/sphaira-bilingual-1.0.8.zip
dist/sphaira-bilingual-source.zip
dist/SHA256SUMS.txt
```

Sphaira、libnx 和 newlib 提交已在脚本中固定；容器工具链与其他上游依赖仍可能更新，当前不宣称可复现的逐字节构建。升级基线时需检查依赖兼容性、补丁、版本号、打包内容与真机行为。

## 提交前

运行 Python 测试、输入校验和实际 C++ 分类器测试。影响界面的修改应在主机确认本地列表、内置商店、分类空列表和退出重启行为；写清哪些检查没有完成。

请保留 Sphaira 与依赖的版权和许可证。再发布修改后的二进制时，提供与该版本对应的源码及构建说明。
