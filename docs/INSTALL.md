# 安装与使用

## 准备

需要一台已经可以运行 `.nro` 自制程序的 Switch，以及可写入 SD 卡的读卡器或 USB 文件传输工具。先保存已有 `sphaira.nro`，便于恢复。

从 [项目 Release](https://github.com/lifengxiu1/sphaira-bilingual/releases/tag/v1.0.8-zhcat-preview.1) 下载：

| 附件 | 用途 |
|---|---|
| `sphaira-bilingual-1.0.8.zip` | 安装用，内含 `/switch/sphaira/sphaira.nro` |
| `sphaira-bilingual-source.zip` | 与安装包对应的修改后 Sphaira 源码 |
| `SHA256SUMS.txt` | 两个压缩包的 SHA-256 校验值 |

此版本是预览版：中英显示已在真机确认；分类菜单仍待完整真机验证。

## 方法一：读卡器

1. 正常关闭 Switch 后再取出 SD 卡，用读卡器连接电脑。
2. 将已有 `/switch/sphaira/sphaira.nro` 复制到电脑留存，避免把多个备份 NRO 放在应用扫描目录。
3. 解压安装包，将里面的 `switch` 文件夹合并到 SD 卡根目录。覆盖的是 `switch/sphaira/sphaira.nro`。
4. 确认路径没有多套一层：应为 `SD:/switch/sphaira/sphaira.nro`，而不是 `SD:/sphaira-bilingual/switch/...`。
5. 安全弹出 SD 卡，装回 Switch，按自己已有的引导方式启动自制环境。

安装包只包含一个应用文件，无需替换 SD 根目录的 `hbmenu.nro`，也无需改动系统分区。

## 方法二：USB 文件传输

1. 在 Switch 中启动 **USB File Transfer / Haze**，使用支持数据传输的 USB 线连接电脑。
2. 在 Windows 的“此电脑”中打开 `Nintendo Switch → SD Card → switch → sphaira`。若文件夹不存在，可以创建。
3. 将旧 `sphaira.nro` 复制到电脑备份，再移走旧文件；把解压得到的新 `sphaira.nro` 复制进去。部分 MTP 传输不会可靠地同名覆盖，移走旧文件后再复制更容易确认。
4. 等复制完成，在 Switch 上按 **＋**退出文件传输，再重新打开 sphaira。

也可以使用已有 Hekate 的 **Tools → USB Tools → SD Card** 共享 SD 卡；复制后先在电脑安全弹出共享磁盘，再在主机结束共享。不要在运行 Sphaira 时通过另一路径覆盖它。

## 校验下载与版本

Windows PowerShell：

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath .\sphaira-bilingual-1.0.8.zip
Get-Content -LiteralPath .\SHA256SUMS.txt
```

Linux：

```bash
sha256sum -c SHA256SUMS.txt
```

当前首个预览版的 NRO 信息：

```text
文件大小：5487385 字节
SHA-256：fa6efdc9cddfdbeff8a43238b9e0ecd21fa592857e168ac18b27063eac900c0b
程序内版本：1.0.8-zhcat [338348e]
NACP 版本：1.0.8
```

进入 sphaira 后按 **Y**，查看菜单标题附近的版本，再按 **B** 返回。NACP 只显示 `1.0.8` 属正常情况，识别定制版应看程序内的 `1.0.8-zhcat`。

## 打开中英列表和内置商店

1. 在原来的 hbmenu 里选中 **sphaira**，按 A。原 hbmenu 自身的图标名称不会因安装本项目而全部改变。
2. 让 Sphaira 使用简体中文，可在其语言设置中选择简体中文，或自动跟随简体中文的主机语言。
3. 本地列表应显示 `中文用途 (English name)`。在默认页签配置下，按右肩键 **R** 打开 Sphaira 内置商店。
4. 本地列表里的 **Homebrew App Store** 是独立客户端，其内部目录不会应用本项目的定制译文。

## 分类入口与排查

代码提供的入口是：本地应用图标列表或内置商店目录列表 → **X → 分类** → 选择分类。选择“全部”可恢复完整列表；本地数量统计的是已安装自制应用。

找不到“分类”时：

1. 按 Y 确认正在运行 `1.0.8-zhcat`，再按 B 关闭 Y 菜单。
2. 返回本地应用图标列表或商店目录。若在文件浏览器、商店详情页或独立 HB App Store，请先返回。
3. 按 X，在本地列表的选项中查看第一项；在商店选项中查看商店来源附近的分类项。非简体中文界面可能显示为 `Category`。
4. 仍然没有时，请提交版本、当前页面标题、操作步骤及菜单照片。本预览版尚未完成该入口的真机确认，不应直接把问题当作安装错误。

若仍显示英文，请先确认进入的是 sphaira，而不是带红色 `Applet Mode` 字样的原 hbmenu；再区分 Sphaira 内置商店与独立 Homebrew App Store。

## 更新与恢复

更新时退出应用，保留旧 NRO，用新 Release 附件覆盖同一路径。恢复时把备份的旧 `sphaira.nro` 放回原处，再启动。

本项目不需要删除 `/config/sphaira`，也不要求格式化 SD 卡。上游自动更新或商店中的官方 Sphaira 包可能覆盖定制版；需要中英分类功能时，请使用本项目的 Release。
