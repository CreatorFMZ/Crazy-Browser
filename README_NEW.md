# Crazy Browser

A lightweight web browser written in Python, powered by **PyQt** and **QtWebEngine**.  
Version 4.0 is built on **PyQt6 / QtWebEngine (Chromium latest)**, offering a modern browsing experience with multi‑tab, bookmarks, history, built‑in settings, HTTPS enforcement, and even the Chrome Dino game – all in one package.

---

## ✨ Features

- **Multi‑tab browsing** – open, close, and switch tabs seamlessly.
- **Bookmarks & History** – add, manage, and open bookmarks; view and clear browsing history.
- **Customizable settings** – choose your home page, default search engine (Bing, Google, DuckDuckGo, or custom), and toggle HTTPS enforcement and history clearing on exit.
- **Internal pages** – a clean new‑tab page with a search box, and a fully HTML‑based settings page (via `crazy://` protocol).
- **Chrome Dino game** – integrated shortcut to `chrome://dino` for offline fun.
- **HTTPS enforcement** – automatically redirects HTTP requests to HTTPS (configurable).
- **Smart address bar** – accepts URLs or search queries; auto‑completes protocols.
- **Download support** – file downloads with progress indication in the status bar.
- **Light theme only** – clean, consistent appearance across all platforms.

---

## 🚀 Requirements

- **Python 3.8+**
- **PyQt6** (for version 4.0) or **PyQt5** (for version 3.x)
- **PyQt6-WebEngine** (if using PyQt6) – often included with `PyQt6`.

---

## 📦 Installation & Running

1. **Clone or download** this repository.
2. **Install dependencies** (choose your version):

   ```bash
   # For version 4.0 (PyQt6)
   pip install PyQt6 PyQt6-WebEngine

   # For earlier versions (PyQt5)
   pip install PyQt5 PyQtWebEngine
   ```

3. **Run the browser**:

   ```bash
   python crazy_browser-4.0.py
   ```

> **Note**: Replace the file name with the version you wish to use (e.g., `crazy_browser-3.4.py`).

---

## 🔧 Configuration

All settings are persisted in JSON files:
- `crazy_config.json` – home page, search engine, HTTPS enforcement, clear history on exit.
- `crazy_bookmarks.json` – list of bookmarks.
- `crazy_history.json` – browsing history.

You can modify these directly or use the built‑in settings page (`crazy://settings`).

---

## 📜 Changelog

### [4.0] – 2026-08-23 (Latest)
- **Migrated to PyQt6 / QtWebEngine (Chromium latest)** – better performance and modern WebKit.
- **Fixed HTTPS redirection** – uses `QTimer.singleShot` to prevent recursion and potential crashes.
- **Refined internal protocol handling** – more robust interception of `crazy://` pages.
- All features from previous versions preserved.

---

### [3.4] – 2026-08-23
- **Added “Always use HTTPS”** (default on) – automatically upgrades HTTP to HTTPS for all navigation.
- **Added Chrome Dino game button** in settings – click to open `chrome://dino` via `crazy://dino`.
- Improved settings page with a dedicated button for the Dino game.

---

### [3.3] – Final Stable (PyQt5)
- Removed language switching, dark theme, and developer tools.
- Kept light theme only, “Clear history on exit”, and persistent configuration.
- Added copyright footer linking to [Fantastic Star](https://fshp.oneapp.dev).
- Shortcuts: `Ctrl+T` new tab, `Ctrl+W` close tab.

---

### [3.2] – Simplification
- Removed developer tools (F12) and dark theme.
- Cleaned up menus and code.

---

### [3.1] – Enhanced Built‑in Settings
- Fully HTML‑based settings page (`crazy://settings`) with home page, search engine, clear‑history‑on‑exit, and more.
- Custom search engine support with `{}` placeholder validation.
- Settings persist via URL parameters and auto‑refresh on save.

---

### [3.0] – Internal Pages & New Tab
- Custom new‑tab page with a search box (HTML/CSS/JS).
- Introduced `crazy://` protocol for internal pages (`newtab`, `settings`).
- Removed private browsing mode.

---

### [2.26.x] – Feature Accumulation
- Bookmarks, history, download support, private windows (later removed), whitelist blocking (in SP editions), and `target="_blank"` fix.
- Status bar, stop button, Bing search for non‑URL input.

---

### [2.5] – Internationalization & Copyright
- Language switching (Chinese/English), copyright notice.

---

### [2.0 – 2.2] – Tabs, Progress, Settings Dialog
- Multi‑tab support, progress bar, user‑agent switcher, settings dialog with theme and privacy options.

---

### [1.0] – Initial Release
- Single‑tab browser with back/forward/reload and address bar.

---

## 📄 License & Credits

© **Fantastic Star** 2026, all rights reserved.  
Visit our official page: [https://fshp.oneapp.dev](https://fshp.oneapp.dev)

---

*Happy browsing!*