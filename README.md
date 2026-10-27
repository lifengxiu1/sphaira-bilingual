# Sphaira 中英分类版

让 Nintendo Switch 的自制应用更容易看懂、查找：**中文用途 + 原英文名**，配合六种用途分类。

基于 [Sphaira 1.0.8](https://github.com/NaGaa95/sphaira/tree/338348e74b6d278bc570a9be5373d25197bf6c8d) 的社区定制项目，提供公开补丁、译文、测试和编译流程。

[下载安装包](https://github.com/lifengxiu1/sphaira-bilingual/releases/tag/v1.0.8-zhcat-preview.1) · [安装与使用](docs/INSTALL.md) · [自行开发](docs/DEVELOPMENT.md) · [完整分类](分类.md) · [中英预览](预览.md)

> 当前发布为 **1.0.8-zhcat 预览版**。中英名称和简介已完成真机确认；分类代码、数据测试和交叉编译已通过，但分类菜单的真机显示与操作仍待确认。欢迎反馈具体页面、版本和按键步骤。

## 功能

- 本地应用显示 `中文用途 (English name)`，例如 `存档管理 (JKSV)`，保留原来的英文品牌和文件。
- 内置商店已为目录快照中的 **511 个软件**整理中文用途和简介，同时保留英文名称及原文简介。
- 本地列表与内置商店共用六种用途分类，可查看各分类数量。
- 中文标签内置在程序中，无需另架翻译服务或替换设备配置。包 ID、下载地址和原始校验信息保持原样。
- 中英名称与简介在**简体中文**界面启用；分类规则不依赖界面语言。

| 分类 | 当前目录条目 |
|---|---:|
| 游戏 | 193 |
| 游戏工具 | 84 |
| 模拟器 | 45 |
| 系统工具 | 98 |
| 影音网络 | 64 |
| 其他 | 27 |

以上数量来自随项目保存的公开目录快照，不代表设备已安装数量，也不保证未来在线目录条目数不变。

## 快速安装

适用于**已经能运行 `.nro` 自制程序**的 Switch。本项目是应用定制版；系统引导环境请按各自上游文档配置。

1. 下载 [Release](https://github.com/lifengxiu1/sphaira-bilingual/releases/tag/v1.0.8-zhcat-preview.1) 中的 `sphaira-bilingual-1.0.8.zip`。安装用这个附件，GitHub 自动生成的 `Source code` 压缩包用于开发。
2. 退出正在运行的 Sphaira，备份 SD 卡中已有的 `/switch/sphaira/sphaira.nro`。
3. 解压后将 `switch` 文件夹合并到 SD 卡根目录，最终路径为 `/switch/sphaira/sphaira.nro`。
4. 在 hbmenu 中启动 **sphaira**。界面使用简体中文后，本地应用应显示中英名称。
5. 在 Sphaira 内按 **Y** 查看菜单标题旁的版本，应包含 `1.0.8-zhcat`，再按 **B** 返回列表。

也可以通过 USB 文件传输复制，覆盖前应先退出旧程序。分步方法、校验和恢复见 [安装文档](docs/INSTALL.md)。

## 使用入口

| 操作 | 位置与按键 |
|---|---|
| 打开本项目 | 在原来的 hbmenu 中选中 `sphaira`，按 A |
| 打开内置商店 | 从 Sphaira 本地应用列表按右肩键 **R**，适用于默认页签配置 |
| 切换本地分类 | 在本地应用图标列表按 **X → 分类**，选择“全部”恢复完整列表 |
| 切换商店分类 | 在内置商店的目录列表按 **X → 分类**；先按 B 退出应用详情页 |
| 查看定制版本 | 按 **Y** 查看菜单标题旁版本，再按 **B** 关闭菜单 |

如果左上角写着 **hbmenu** 并显示红色 **Applet Mode**，请先从图标列表启动 sphaira。本地列表里的 **Homebrew App Store** 是另一款独立软件，本项目的中英目录显示在 Sphaira **内置商店**中。

## 范围与已知限制

- 分类菜单尚待完整真机确认。找不到时，先确认版本，再关闭 Y 菜单，回到本地图标列表或商店目录后按 X；文件浏览器、商店应用详情页不提供这个分类入口。仍无菜单请提交反馈，勿反复覆盖安装。
- 此定制只增加用途标签、简短说明和分类，不会把各个软件的内部菜单全部翻译成中文。
- 本地用途名称和分类按已知 `.nro` 路径匹配；未知路径保留原名并归“其他”。新出现的商店 ID 使用原始类别回退，尚无译文时显示原文。
- 分类只筛选自制程序，不会替商业游戏建立 HOME 菜单文件夹。项目也不提供商业游戏资源。
- 更新为上游原版可能覆盖定制功能；安装第三方应用前仍需自行确认来源与兼容性。本项目不承诺免封禁。

## 源码与构建

仓库采用“固定上游源码 + 可审查补丁”的形式，减少重复维护。`source.patch` 保存 C++ 改动，`catalog-zh.tsv` 保存译文，`categories.json` 保存分类规则。

- 每个 Release 附带安装包、与该二进制对应的修改后 Sphaira 源码包及 `SHA256SUMS.txt`。
- Fork 后可使用 **Actions → Build bilingual Sphaira → Run workflow** 编译；无需在电脑安装 Switch SDK。流程会生成草稿 Release，由仓库所有者检查后发布。
- Python 测试仅依赖标准库；完整构建还会编译并运行实际 C++ 分类器测试。
- 可修改译文、调整分类、扩展界面或迁移到新版本，具体步骤见 [开发文档](docs/DEVELOPMENT.md) 与 [贡献说明](CONTRIBUTING.md)。

当前基线固定到 Sphaira 提交 `338348e74b6d278bc570a9be5373d25197bf6c8d`。工具链容器仍使用 `latest`，后续重建结果不保证与已有安装包逐字节一致。

## 来源、许可与致谢

- 上游程序：[NaGaa95/sphaira](https://github.com/NaGaa95/sphaira)，保留其原始版权、许可证与依赖署名。
- 商店目录：[fortheusers 官方公开目录](https://switch.cdn.fortheusers.org/repo.json)，快照中的原作者、项目链接和英文说明保留。
- 代码按 [GNU GPL v3](LICENSE) 开源；上游及各依赖原有许可继续适用。修改、再分发时请保留相应版权与许可证，并提供对应源码。
- 贡献与问题反馈：[GitHub Issues](https://github.com/lifengxiu1/sphaira-bilingual/issues)。

## Codex 开发与后续维护

**本项目的中英标签、用途分类补丁、测试、构建配置及文档由 Codex 根据项目发起人的需求开发整理。** Sphaira 原始程序及其依赖由各自作者开发，Codex 署名仅指本次定制工作。

项目已经公开，后续可自行 **Fork、修改、编译和继续开发**；也可以使用 Codex 或其他开发工具协助维护。欢迎改进译文、补充分类、修复问题并提交 Pull Request。
