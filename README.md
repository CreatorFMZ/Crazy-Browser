# Crazy Browser

A browser written in Python.  
Run `crazy_browser-3.3.py` (or `crazy_browser-3.3-sp.py` for the security-enhanced version) to use.  
© Fantastic Star 2026, all rights reserved.

---

## 更新日志 / Changelog

---

### [1.0] – 初始版本 / Initial Release
- 基于 PyQt6 构建的单标签页浏览器。  
- 核心功能：地址栏导航（自动补全协议）、后退/前进/刷新按钮。  
- 默认打开 Google 首页。  

- Single‑tab browser built with PyQt6.  
- Core features: address bar navigation (auto‑completes protocol), back/forward/reload buttons.  
- Default home page is Google.

---

### [2.0] – 多标签与增强导航 / Tabs & Enhanced Navigation
- **多标签页支持**：使用 `QTabWidget`，可新建、关闭标签页。  
- **进度条**：显示页面加载进度。  
- **用户代理切换**：下拉菜单切换桌面/iPhone/Android UA。  
- **工具栏**：添加主页按钮，地址栏塞入工具栏。  

- **Tab support** via `QTabWidget` – create and close tabs.  
- **Progress bar** shows page loading progress.  
- **User‑Agent switcher** (Desktop / iPhone / Android) via dropdown.  
- **Home button** added to toolbar; address bar integrated into the toolbar.

---

### [2.1] – 设置面板与隐私选项 / Settings Panel & Privacy
- 新增 **设置对话框**（`SettingsDialog`）：  
  - 主题切换（浅色/深色）。  
  - 保留历史记录与登录状态（持久化）。  
  - 一键清除缓存、Cookie 和历史记录。  
- 引入配置文件持久化机制（`QWebEngineProfile` 默认持久化）。  

- Added **Settings dialog** (`SettingsDialog`) with:  
  - Theme switching (Light/Dark).  
  - Option to keep history and login state (persistent).  
  - One‑click clear cache, cookies, and history.  
- Persistent configuration using `QWebEngineProfile` (default profile).

---

### [2.2] – 优化与 Bug 修复 / Optimizations & Bug Fixes
- 修复导航按钮状态（后退/前进按钮根据历史自动启用/禁用）。  
- 进度条加载完成后自动隐藏。  
- 地址栏添加占位文本提示。  
- 深色主题样式完善（工具栏、标签页、输入框等）。  
- 代码结构优化，去除冗余。  

- Fixed navigation button states (back/forward enabled/disabled based on history).  
- Progress bar auto‑hides after loading finishes.  
- Placeholder text added to the address bar.  
- Improved dark theme styling (toolbar, tabs, inputs, etc.).  
- Code cleaned up and restructured.

---

### [2.5] – 国际化与版权信息 / Internationalization & Copyright
- **语言支持**：设置对话框增加语言选择（中文/English），界面文本动态切换。  
- **版权与版本**：设置中显示 `Crazy Browser 2.5 © Fantastic Star`。  
- 翻译字典（`translations`）集中管理所有界面字符串。  

- **Language support**: Language selection (Chinese/English) in settings, UI texts update dynamically.  
- **Copyright & version** shown in settings: `Crazy Browser 2.5 © Fantastic Star`.  
- Centralised translation dictionary (`translations`) for all UI strings.

---

### [2.5_r.1] – 首页自定义增强 / Homepage Customization Enhancement
- 设置对话框新增 **“恢复默认首页”** 按钮，一键重置为 Google。  
- 新标签页统一使用自定义首页，不再硬编码。  
- 使用 `QSettings` 持久化保存首页配置（`custom_home/enabled`、`custom_home/url`）。  
- 设置加载时自动补全协议（`http://` / `https://`）。  

- Added a **“Reset to default homepage”** button in settings to quickly restore Google.  
- New tabs now consistently use the custom homepage (no hard‑coded fallback).  
- Homepage settings are persisted via `QSettings` (`custom_home/enabled`, `custom_home/url`).  
- Protocol (`http://` / `https://`) is auto‑prepended when loading custom URLs.

---

### [2.5_r.2] – 设置独立标签页 + 书签 + AI 集成 / Settings as Tab + Bookmarks + AI Integration
- **设置页面独立为标签页**：访问 `crazy://setting` 在浏览器内打开设置，不再使用模态对话框。  
- **书签管理**：在设置标签页中添加书签列表，支持添加当前页面、移除选中条目。  
- **搜索引擎选择**：下拉菜单支持 Google / Bing / Baidu，设置生效。  
- **AI 集成**：设置中增加“打开 DeepLost X2”按钮，直接跳转至 `https://deeplost.oneapp.dev/`（外部链接）。  
- 使用 `QSettings` 保存书签列表和搜索引擎偏好。  
- 切换语言或主题时自动刷新设置页（若已打开）。  

- **Settings as a standalone tab**: visit `crazy://setting` to open settings inside the browser (no modal dialog).  
- **Bookmark management**: added a bookmark list in the settings tab – supports adding the current page and removing selected entries.  
- **Search engine selection**: dropdown supports Google / Bing / Baidu – takes effect immediately.  
- **AI integration**: added an “Open DeepLost X2” button in settings, linking to `https://deeplost.oneapp.dev/` (external).  
- `QSettings` is used to persist bookmarks and the search engine preference.  
- Settings tab auto‑refreshes when language or theme changes.

---

### [2.26.1] – PyQt5 迁移与简化 / Migration to PyQt5 & Simplification
- 从 PyQt6 迁移至 PyQt5。  
- 简化 UI，仅保留核心导航栏和地址栏。  
- 地址栏自动补全 `http://` 协议。  

- Migrated from PyQt6 to PyQt5.  
- Simplified UI – only core navigation bar and address bar.  
- Address bar auto‑prepends `http://` when missing.

---

### [2.26.2] – 状态栏与搜索增强 / Status Bar & Search Enhancement
- 添加 **状态栏** 显示加载进度。  
- 新增 **停止加载** 按钮。  
- 地址栏输入非 URL 时自动使用 Bing 搜索。  
- 默认主页设为 `https://search.oneapp.dev`。  

- Added **status bar** showing loading progress.  
- Added **Stop** button.  
- Non‑URL input in address bar triggers a Bing search.  
- Default home page set to `https://search.oneapp.dev`.

---

### [2.26.3] – 书签、历史、无痕模式与下载 / Bookmarks, History, Private Mode & Downloads
- **书签管理**：添加当前页面、管理书签（打开/删除）。  
- **历史记录**：查看全部历史、打开历史条目、清除历史。  
- **无痕模式**（Private Browsing）：新建无痕窗口，不保留任何数据。  
- **下载支持**：文件下载时弹出保存对话框，状态栏显示进度。  
- **开发者工具**：右键菜单增加“开发者工具 (F12)”。  
- **设置持久化**：可配置首页地址和默认搜索引擎。  
- **快捷键**：Ctrl+T 新建标签，Ctrl+W 关闭标签，Ctrl+Shift+N 新建无痕窗口。  

- **Bookmarks**: add current page, manage (open/delete).  
- **History**: view all, open entries, clear history.  
- **Private browsing**: new private window – no data retained.  
- **Download support**: save‑file dialog with progress in status bar.  
- **Developer tools** added to right‑click context menu (F12).  
- **Persistent settings**: configurable home page and default search engine.  
- **Shortcuts**: Ctrl+T new tab, Ctrl+W close tab, Ctrl+Shift+N new private window.

---

### [2.26.3-sp] – 白名单拦截（国内网站）/ Whitelist Blocking (China Sites)
- 在 2.26.3 基础上增加 **白名单机制**。  
- 只允许访问 `.cn` 域名以及预定义的国内网站（如 baidu.com, qq.com 等）。  
- 拦截时显示友好的“访问被拒绝”页面，并带有返回/首页链接。  

- Built on 2.26.3 with a **whitelist mechanism**.  
- Only allows `.cn` domains and a predefined list of Chinese sites (e.g., baidu.com, qq.com).  
- Shows a friendly "Access Denied" page with links to go back or to the home page.

---

### [2.26.4] – 修复 `target="_blank"` 链接 / Fix for `target="_blank"` Links
- 实现 `createWindow` 方法，使带有 `target="_blank"` 的链接在新标签页中打开。  
- 新标签页继承原标签页的无痕状态。  

- Implemented `createWindow` so links with `target="_blank"` open in a new tab.  
- New tab inherits the private state of the original tab.

---

### [3.0] – 内置页面与全新新标签页 / Built‑in Pages & New Tab Redesign
- **自定义新标签页**：使用 HTML+CSS+JS 的搜索框界面，支持直接搜索。  
- **内部协议**：引入 `crazy://` 协议，用于处理 `newtab` 和 `settings` 等内部页面。  
- 移除无痕模式（代码中 `is_private` 参数未启用）。  
- 设置页面从对话框改为内置网页（`crazy://settings`）。  

- **Custom new tab page** with a search box built in HTML/CSS/JS, supports direct searching.  
- **Internal protocol** `crazy://` for handling pages like `newtab` and `settings`.  
- Removed private mode (the `is_private` parameter was not active).  
- Settings changed from a dialog to a built‑in web page (`crazy://settings`).

---

### [3.1] – 完善内置设置页面 / Enhanced Built‑in Settings Page
- 设置页面支持修改：  
  - 首页地址  
  - 搜索引擎（Bing/Google/DuckDuckGo/自定义）  
  - 语言（中/英）  
  - 主题（浅色/深色）  
  - UA 模式（桌面/移动）  
- 设置保存后立即生效（主题、UA、语言等）。  
- 菜单栏增加“设置”入口，打开设置标签页。  

- Settings page now allows changing:  
  - Home page URL  
  - Search engine (Bing/Google/DuckDuckGo/Custom)  
  - Language (Chinese/English)  
  - Theme (Light/Dark)  
  - UA mode (Desktop/Mobile)  
- Settings take effect immediately (theme, UA, language, etc.).  
- Added "Settings" entry in the menu bar to open the settings tab.

---

### [3.1_r.1] – 设置页面优化（第一次修订）/ Settings Page Refinement (Revision 1)
- 修复设置保存逻辑，使用 URL 参数（`?save=1&lang=...`）传递数据。  
- 设置页面完全由 HTML 生成，不再依赖 Qt 对话框。  

- Fixed settings saving logic – now uses URL parameters (`?save=1&lang=...`).  
- Settings page is now completely HTML‑generated, no Qt dialogs.

---

### [3.1_r.2] – 设置页面优化（第二次修订）/ Settings Page Refinement (Revision 2)
- 增加自定义搜索引擎输入框（当选择“Custom”时显示）。  
- 验证自定义 URL 必须包含 `{}` 占位符。  
- 改进页面样式，更美观。  

- Added custom search engine input field (shown when "Custom" is selected).  
- Validates that the custom URL must contain `{}` as a placeholder.  
- Improved page styling for better appearance.

---

### [3.1_r.3] – 设置页面优化（第三次修订）/ Settings Page Refinement (Revision 3)
- 设置页面新增 **“退出时清除历史”** 复选框。  
- 整合所有配置项（首页、搜索引擎、语言、主题、UA、清除历史）。  
- 保存后自动刷新设置页。  

- Added a **“Clear history on exit”** checkbox to the settings page.  
- All config items (home, search engine, language, theme, UA, clear‑on‑exit) are unified.  
- Settings page auto‑refreshes after saving.

---

### [3.2] – 简化与移除功能 / Simplification & Feature Removal
- **移除开发者工具**（F12 快捷键和菜单项）。  
- **移除暗色主题**，仅保留浅色主题。  
- 精简菜单栏，去掉“开发者”菜单。  
- 代码清理，去除未使用的导入。  

- **Removed Developer Tools** (F12 shortcut and menu item).  
- **Removed Dark theme** – only Light theme remains.  
- Simplified menu bar – removed the "Developer" menu.  
- Code cleaned up – unused imports removed.

---

### [3.3] – 最终稳定版 / Final Stable Release
- 彻底移除语言和主题切换，统一使用浅色主题。  
- 保留“退出时清除历史”选项（在设置页中配置）。  
- 设置页脚添加版权信息：`© Fantastic Star 2026, all rights reserved.` 并链接至官网。  
- 移除无痕模式（私有窗口功能被完全移除）。  
- 仅保留新建窗口（普通模式），快捷键 Ctrl+T、Ctrl+W。  
- 代码精简，稳定可靠。  

- Completely removed language and theme switching – now always uses Light theme.  
- Kept "Clear history on exit" option (configurable in settings).  
- Added footer with copyright: `© Fantastic Star 2026, all rights reserved.` with a link to the official site.  
- Removed private browsing entirely.  
- Only normal windows remain; shortcuts Ctrl+T and Ctrl+W.  
- Code is lean, stable, and reliable.

---

### [3.3-sp] – 安全增强版（SP）/ Security‑Enhanced Edition (SP)
- 基于 3.3 版本，**恢复无痕模式**（新建无痕窗口，快捷键 Ctrl+Shift+N）。  
- **恢复开发者工具**（右键菜单和 F12 快捷键）。  
- **增加白名单拦截功能**：只允许访问国内网站（.cn 域名及预定义列表），其余网站显示拦截页面。  
- 拦截页面美观，提供返回上一页和前往首页的链接。  
- 最终版本，兼顾安全与功能。  

- Built on 3.3, **restored private mode** (new private window with Ctrl+Shift+N).  
- **Restored Developer Tools** (right‑click menu and F12 shortcut).  
- **Added whitelist blocking**: only allows Chinese sites (.cn and predefined list); others show a block page.  
- Block page is user‑friendly, with links to go back or to the home page.  
- The final version balances security and functionality.

---

**更新说明**：版本号从 3.0 开始采用“主版本.次版本”格式，中间修订版本（如 3.1_r.1）表示开发过程中的内部迭代。最终推荐使用 `crazy_browser-3.3.py`（稳定版）或 `crazy_browser-3.3-sp.py`（安全增强版）。

**Note**: From version 3.0 onward, the numbering follows "major.minor"; intermediate revisions (e.g., 3.1_r.1) indicate internal iterations during development. We recommend using `crazy_browser-3.3.py` (stable) or `crazy_browser-3.3-sp.py` (security‑enhanced).
---

在README_NEW.md中了解更多。
Learn more in README_NEW.md.