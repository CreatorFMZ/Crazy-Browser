# crazy_browser-4.0.py
# Version 4.0 - PyQt6 / QtWebEngine (Chromium latest)
# Features: multi-tab, bookmarks, history, settings, HTTPS enforcement,
#           custom crazy:// protocol, Chrome Dino game.

import sys
import json
import os
from datetime import datetime
from urllib.parse import urlparse, parse_qs, quote

from PyQt6.QtCore import QUrl, Qt, QTimer          # added QTimer
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QToolBar, QLineEdit,
    QPushButton, QStatusBar, QVBoxLayout, QHBoxLayout,
    QMenu, QDialog, QListWidget, QListWidgetItem,
    QMessageBox, QFileDialog
)
from PyQt6.QtGui import QAction, QKeySequence, QCloseEvent

from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage

# ---------- constants ----------
CONFIG_FILE    = "crazy_config.json"
BOOKMARKS_FILE = "crazy_bookmarks.json"
HISTORY_FILE   = "crazy_history.json"

NEW_TAB_URL    = "crazy://newtab"
SETTINGS_URL   = "crazy://settings"
DINO_URL       = "crazy://dino"

# ---------- data manager ----------
class DataManager:
    @staticmethod
    def load_json(file, default):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return default

    @staticmethod
    def save_json(file, data):
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

# ---------- custom web page (handles crazy://) ----------
class CrazyWebPage(QWebEnginePage):
    def __init__(self, view, parent=None):
        super().__init__(parent)
        self.view = view

    def acceptNavigationRequest(self, url, nav_type, is_main_frame):
        url_str = url.toString()

        if url_str.startswith("crazy://"):
            main = self.view.get_main_window()
            if not main:
                return False

            if url_str == NEW_TAB_URL:
                self.view.load_new_tab_page()
                return False

            elif url_str == DINO_URL:
                self.view.setUrl(QUrl("chrome://dino"))
                return False

            elif url_str.startswith(SETTINGS_URL):
                parsed = urlparse(url_str)
                params = parse_qs(parsed.query)
                if 'save' in params:
                    home = params.get('home', [main.config.get('home_url', '')])[0]
                    engine = params.get('engine', [main.config.get('search_engine', '')])[0]
                    clear_hist = params.get('clear_history', ['false'])[0].lower() == 'true'
                    force_https = params.get('force_https', ['true'])[0].lower() == 'true'

                    if home.strip():
                        main.config['home_url'] = home.strip()
                    if engine.strip():
                        main.config['search_engine'] = engine.strip()
                    main.config['clear_history_on_close'] = clear_hist
                    main.config['force_https'] = force_https
                    DataManager.save_json(CONFIG_FILE, main.config)
                    self.view.load_settings_page()
                else:
                    self.view.load_settings_page()
                return False

            else:
                return False

        # Enforce HTTPS with deferred navigation to avoid recursion/crash
        if url.scheme() == "http":
            main = self.view.get_main_window()
            if main and main.config.get("force_https", True):
                new_url = QUrl(url_str.replace("http://", "https://", 1))
                if new_url.isValid():
                    # Defer the redirect to break the navigation chain
                    QTimer.singleShot(0, lambda: self.view.setUrl(new_url))
                    return False
                # If conversion fails, cancel the navigation
                return False

        return super().acceptNavigationRequest(url, nav_type, is_main_frame)

# ---------- custom web view ----------
class CrazyWebView(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.download_progress = 0

        self.setPage(CrazyWebPage(self, self))
        self.page().profile().downloadRequested.connect(self.handle_download)

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.open_context_menu)

    def get_main_window(self):
        p = self.parent()
        while p:
            if isinstance(p, CrazyBrowser):
                return p
            p = p.parent()
        return None

    def createWindow(self, window_type):
        main = self.get_main_window()
        if main:
            new_view = CrazyWebView(parent=None)
            idx = main.tab_widget.addTab(new_view, "New Tab")
            main.tab_widget.setCurrentIndex(idx)
            new_view.titleChanged.connect(lambda t: main.update_tab_title(new_view, t))
            new_view.urlChanged.connect(lambda q: main.update_url_bar(q, new_view))
            new_view.loadProgress.connect(lambda p: main.update_status(p, new_view))
            new_view.loadFinished.connect(lambda ok: main.record_history(new_view))
            return new_view
        return super().createWindow(window_type)

    def setUrl(self, url):
        super().setUrl(url)

    def load_new_tab_page(self):
        main = self.get_main_window()
        engine = main.config.get("search_engine", "https://www.bing.com/search?q={}") if main else "https://www.bing.com/search?q={}"

        html = f"""
        <!DOCTYPE html>
        <html>
        <head><meta charset="UTF-8"><title>New Tab</title>
        <style>
            body {{ margin:0; display:flex; justify-content:center; align-items:center; height:100vh; background:#f0f0f0; font-family:Arial,sans-serif; }}
            .container {{ text-align:center; padding:40px; background:#fff; border-radius:20px; box-shadow:0 10px 40px rgba(0,0,0,0.1); }}
            h1 {{ color:#333; font-size:36px; margin-bottom:30px; }}
            .search-box {{ display:flex; justify-content:center; gap:10px; }}
            #search-input {{ width:400px; padding:14px 20px; font-size:18px; border:1px solid #ccc; border-radius:30px; outline:none; background:#fafafa; color:#333; }}
            #search-btn {{ padding:14px 28px; font-size:18px; border:none; border-radius:30px; background:#4a90d9; color:#fff; cursor:pointer; transition:background 0.2s; }}
            #search-btn:hover {{ background:#5a9ef0; }}
        </style>
        </head>
        <body>
        <div class="container">
            <h1>🌐 Crazy Browser</h1>
            <div class="search-box">
                <input id="search-input" type="text" placeholder="Search or enter address..." autofocus>
                <button id="search-btn">Search</button>
            </div>
        </div>
        <script>
            const input = document.getElementById('search-input');
            const btn = document.getElementById('search-btn');
            function doSearch() {{
                const q = input.value.trim();
                if (!q) return;
                const engine = '{engine}';
                const url = engine.replace('{{}}', encodeURIComponent(q));
                window.location.href = url;
            }}
            btn.addEventListener('click', doSearch);
            input.addEventListener('keydown', (e) => {{ if (e.key === 'Enter') doSearch(); }});
        </script>
        </body>
        </html>
        """
        self.setHtml(html, baseUrl=QUrl(NEW_TAB_URL))

    def load_settings_page(self):
        main = self.get_main_window()
        if not main:
            return
        config = main.config
        home_url = config.get("home_url", "")
        search_engine = config.get("search_engine", "https://www.bing.com/search?q={}")
        clear_hist = config.get("clear_history_on_close", False)
        force_https = config.get("force_https", True)

        presets = {
            "Bing": "https://www.bing.com/search?q={}",
            "Google": "https://www.google.com/search?q={}",
            "DuckDuckGo": "https://duckduckgo.com/?q={}"
        }
        engine_options = ""
        for label, tmpl in presets.items():
            sel = "selected" if tmpl == search_engine else ""
            engine_options += f'<option value="{tmpl}" {sel}>{label}</option>'
        if search_engine not in presets.values():
            engine_options += '<option value="custom" selected>Custom</option>'
        else:
            engine_options += '<option value="custom">Custom</option>'

        chk_clear = "checked" if clear_hist else ""
        chk_https = "checked" if force_https else ""

        html = f"""
        <!DOCTYPE html>
        <html>
        <head><meta charset="UTF-8"><title>Settings</title>
        <style>
            body {{ margin:0; display:flex; justify-content:center; align-items:center; min-height:100vh; background:#f0f0f0; font-family:Arial,sans-serif; }}
            .container {{ text-align:left; padding:40px; background:#fff; border-radius:20px; box-shadow:0 10px 40px rgba(0,0,0,0.1); color:#333; width:450px; }}
            h1 {{ color:#333; font-size:32px; margin-bottom:25px; text-align:center; }}
            .field {{ display:flex; flex-direction:column; margin:12px 0; }}
            .field label {{ font-size:16px; margin-bottom:4px; }}
            .field input, .field select {{ padding:8px 12px; font-size:15px; border:1px solid #ccc; border-radius:8px; background:#fafafa; color:#333; outline:none; }}
            .field input:focus, .field select:focus {{ border-color:#4a90d9; }}
            .field-checkbox {{ flex-direction:row; align-items:center; gap:10px; }}
            .field-checkbox input {{ width:18px; height:18px; margin:0; }}
            #custom-engine-container {{ margin-top:6px; }}
            #save-btn {{ margin-top:20px; padding:12px 32px; font-size:18px; border:none; border-radius:30px; background:#4a90d9; color:#fff; cursor:pointer; transition:background 0.2s; width:100%; }}
            #save-btn:hover {{ background:#5a9ef0; }}
            .footer {{ margin-top:30px; text-align:center; font-size:14px; color:#777; border-top:1px solid #eee; padding-top:20px; }}
            .footer a {{ color:#4a90d9; text-decoration:none; }}
            .footer a:hover {{ text-decoration:underline; }}
            .dino-btn {{ margin-top:15px; padding:10px 20px; font-size:16px; border:none; border-radius:30px; background:#f5a623; color:#fff; cursor:pointer; transition:background 0.2s; width:100%; }}
            .dino-btn:hover {{ background:#f7b840; }}
        </style>
        </head>
        <body>
        <div class="container">
            <h1>Settings</h1>
            <div class="field">
                <label>Home page</label>
                <input id="home-input" type="text" value="{home_url}" placeholder="https://example.com">
            </div>
            <div class="field">
                <label>Default Search Engine</label>
                <select id="engine-select">
                    {engine_options}
                </select>
                <div id="custom-engine-container" style="display:{'block' if search_engine not in presets.values() else 'none'};">
                    <input id="custom-engine-input" type="text" value="{search_engine if search_engine not in presets.values() else ''}" placeholder="Custom URL (use {{}} for query)">
                </div>
            </div>
            <div class="field field-checkbox">
                <label for="clear-check">Clear history on close</label>
                <input id="clear-check" type="checkbox" {chk_clear}>
            </div>
            <div class="field field-checkbox">
                <label for="https-check">Always use HTTPS</label>
                <input id="https-check" type="checkbox" {chk_https}>
            </div>
            <button id="save-btn">Save</button>
            <button id="dino-btn" class="dino-btn">No Internet? Play Chrome Dino!</button>
            <div class="footer">
                <div style="font-weight:bold; font-size:16px;">Crazy Browser</div>
                <div>© <a href="https://fshp.oneapp.dev" target="_blank">Fantastic Star</a> 2026, all rights reserved.</div>
            </div>
        <script>
            const engineSelect = document.getElementById('engine-select');
            const customContainer = document.getElementById('custom-engine-container');
            const customInput = document.getElementById('custom-engine-input');

            engineSelect.addEventListener('change', function() {{
                if (this.value === 'custom') {{
                    customContainer.style.display = 'block';
                    customInput.focus();
                }} else {{
                    customContainer.style.display = 'none';
                }}
            }});

            document.getElementById('save-btn').addEventListener('click', function() {{
                const home = document.getElementById('home-input').value.trim();
                let engine = engineSelect.value;
                if (engine === 'custom') {{
                    engine = customInput.value.trim();
                    if (!engine) {{ alert('Please enter a custom search URL.'); return; }}
                    if (!engine.includes('{{}}')) {{ alert('Custom URL must contain "{{}}" as placeholder.'); return; }}
                }}
                const clearHistory = document.getElementById('clear-check').checked;
                const forceHttps = document.getElementById('https-check').checked;
                const params = new URLSearchParams({{
                    save: '1',
                    home: home,
                    engine: engine,
                    clear_history: clearHistory ? 'true' : 'false',
                    force_https: forceHttps ? 'true' : 'false'
                }});
                window.location.href = 'crazy://settings?' + params.toString();
            }});

            document.getElementById('dino-btn').addEventListener('click', function() {{
                window.location.href = 'crazy://dino';
            }});
        </script>
        </body>
        </html>
        """
        self.setHtml(html, baseUrl=QUrl(SETTINGS_URL))

    def handle_download(self, download):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save File", download.suggestedFileName()
        )
        if file_path:
            download.setPath(file_path)
            download.accept()
            main = self.get_main_window()
            if main:
                download.downloadProgress.connect(
                    lambda r, t: main.statusBar().showMessage(
                        f"Downloading: {download.suggestedFileName()} {int(r/t*100)}%"
                    )
                )
                download.finished.connect(
                    lambda: main.statusBar().showMessage(
                        f"Download complete: {os.path.basename(file_path)}"
                    )
                )

    def open_context_menu(self, pos):
        menu = self.page().createStandardContextMenu()
        menu.exec(self.mapToGlobal(pos))

# ---------- main browser window ----------
class CrazyBrowser(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("crazy_browser")
        self.setGeometry(100, 100, 1200, 800)

        self.config = DataManager.load_json(CONFIG_FILE, {
            "home_url": "https://creativesearch.pages.dev",
            "search_engine": "https://www.bing.com/search?q={}",
            "clear_history_on_close": False,
            "force_https": True
        })
        self.bookmarks = DataManager.load_json(BOOKMARKS_FILE, [])
        self.history_data = DataManager.load_json(HISTORY_FILE, [])

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        self.setCentralWidget(self.tab_widget)

        self.create_toolbar()
        self.create_menu_bar()

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.apply_light_theme()

        self.new_tab(self.config["home_url"])
        self.setup_shortcuts()

    def apply_light_theme(self):
        style = """
            QMainWindow, QDialog { background-color: #f0f0f0; color: #000000; }
            QToolBar, QStatusBar, QMenuBar, QMenu { background-color: #e0e0e0; color: #000000; }
            QLineEdit, QComboBox, QListWidget { background-color: #ffffff; color: #000000; border: 1px solid #aaa; }
            QPushButton { background-color: #4a90d9; color: #ffffff; border: none; padding: 6px 12px; border-radius: 4px; }
            QPushButton:hover { background-color: #5a9ef0; }
            QTabWidget::pane { border: 1px solid #aaa; }
            QTabBar::tab { background-color: #e0e0e0; color: #000000; padding: 8px 12px; }
            QTabBar::tab:selected { background-color: #4a90d9; color: #ffffff; }
        """
        self.setStyleSheet(style)

    def create_toolbar(self):
        nav = QToolBar("Navigation")
        self.addToolBar(nav)

        back = QPushButton("←")
        back.clicked.connect(lambda: self.current_view().back())
        nav.addWidget(back)

        fwd = QPushButton("→")
        fwd.clicked.connect(lambda: self.current_view().forward())
        nav.addWidget(fwd)

        reload = QPushButton("↻")
        reload.clicked.connect(lambda: self.current_view().reload())
        nav.addWidget(reload)

        stop = QPushButton("✕")
        stop.clicked.connect(lambda: self.current_view().stop())
        nav.addWidget(stop)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        nav.addWidget(self.url_bar)

        home = QPushButton("🏠")
        home.clicked.connect(self.go_home)
        nav.addWidget(home)

        new_tab = QPushButton("+")
        new_tab.clicked.connect(lambda: self.new_tab(None))
        nav.addWidget(new_tab)

        bookmark = QPushButton("☆")
        bookmark.setToolTip("Add bookmark")
        bookmark.clicked.connect(self.add_current_bookmark)
        nav.addWidget(bookmark)

    def create_menu_bar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        new_tab_act = QAction("New Tab (Ctrl+T)", self)
        new_tab_act.triggered.connect(lambda: self.new_tab(None))
        file_menu.addAction(new_tab_act)

        new_win_act = QAction("New Window", self)
        new_win_act.triggered.connect(self.new_window)
        file_menu.addAction(new_win_act)

        file_menu.addSeparator()
        close_tab_act = QAction("Close Tab (Ctrl+W)", self)
        close_tab_act.triggered.connect(lambda: self.close_tab(self.tab_widget.currentIndex()))
        file_menu.addAction(close_tab_act)

        history_menu = menubar.addMenu("History")
        show_hist_act = QAction("Show All History", self)
        show_hist_act.triggered.connect(self.show_history_dialog)
        history_menu.addAction(show_hist_act)

        clear_hist_act = QAction("Clear History", self)
        clear_hist_act.triggered.connect(self.clear_history)
        history_menu.addAction(clear_hist_act)

        book_menu = menubar.addMenu("Bookmarks")
        add_bm_act = QAction("Add Current Page", self)
        add_bm_act.triggered.connect(self.add_current_bookmark)
        book_menu.addAction(add_bm_act)

        manage_bm_act = QAction("Manage Bookmarks", self)
        manage_bm_act.triggered.connect(self.show_bookmarks_dialog)
        book_menu.addAction(manage_bm_act)

        settings_act = QAction("Settings", self)
        settings_act.triggered.connect(self.open_settings_tab)
        menubar.addAction(settings_act)

    def setup_shortcuts(self):
        new = QAction(self)
        new.setShortcut(QKeySequence("Ctrl+T"))
        new.triggered.connect(lambda: self.new_tab(None))
        self.addAction(new)

        close = QAction(self)
        close.setShortcut(QKeySequence("Ctrl+W"))
        close.triggered.connect(lambda: self.close_tab(self.tab_widget.currentIndex()))
        self.addAction(close)

    # ---------- tab management ----------
    def new_tab(self, url=None, title="New Tab"):
        view = CrazyWebView(self)
        if url is None or url == NEW_TAB_URL:
            view.load_new_tab_page()
            display = "New Tab"
        elif url == SETTINGS_URL:
            view.load_settings_page()
            display = "Settings"
        else:
            view.setUrl(QUrl(url))
            display = title

        idx = self.tab_widget.addTab(view, display)
        self.tab_widget.setCurrentIndex(idx)

        view.urlChanged.connect(lambda q: self.update_url_bar(q, view))
        view.titleChanged.connect(lambda t: self.update_tab_title(view, t))
        view.loadProgress.connect(lambda p: self.update_status(p, view))
        view.loadFinished.connect(lambda ok: self.record_history(view))
        return view

    def close_tab(self, index):
        if self.tab_widget.count() > 1:
            self.tab_widget.removeTab(index)
        else:
            self.close()

    def current_view(self):
        return self.tab_widget.currentWidget()

    def on_tab_changed(self, index):
        if index >= 0:
            view = self.tab_widget.widget(index)
            if view:
                self.update_url_bar(view.url(), view)
                self.setWindowTitle("crazy_browser - " + view.title())

    def update_tab_title(self, view, title):
        idx = self.tab_widget.indexOf(view)
        if idx >= 0:
            short = title[:20] + "..." if len(title) > 20 else title
            self.tab_widget.setTabText(idx, short)
            if view == self.current_view():
                self.setWindowTitle("crazy_browser - " + title)

    # ---------- navigation ----------
    def navigate_to_url(self):
        """
        Handle user input from the address bar.
        Uses QUrl.fromUserInput for URLs and URL-encodes search queries.
        """
        text = self.url_bar.text().strip()
        if not text:
            return

        # Heuristic: if it contains a dot or starts with a known scheme, treat as URL
        is_url = ('.' in text) or text.startswith(('chrome://', 'http://', 'https://', 'crazy://'))

        if is_url:
            # QUrl.fromUserInput automatically adds scheme and encodes special characters
            url = QUrl.fromUserInput(text)
            if url.isValid():
                self.current_view().setUrl(url)
                return
            # fall through to search if URL is invalid

        # Treat as search query: URL-encode and insert into search template
        query = quote(text)   # properly encode spaces, etc.
        search_url = self.config["search_engine"].format(query)
        self.current_view().setUrl(QUrl(search_url))

    def go_home(self):
        self.current_view().setUrl(QUrl(self.config["home_url"]))

    def update_url_bar(self, url, view):
        if view == self.current_view():
            self.url_bar.setText(url.toString())

    def update_status(self, progress, view):
        if view == self.current_view():
            self.status_bar.showMessage(f"Loading {progress}%")

    def record_history(self, view):
        if view.url().isValid():
            url_str = view.url().toString()
            if not self.history_data or self.history_data[-1]["url"] != url_str:
                self.history_data.append({
                    "url": url_str,
                    "title": view.title(),
                    "time": datetime.now().isoformat()
                })
                DataManager.save_json(HISTORY_FILE, self.history_data)

    # ---------- window management ----------
    def new_window(self):
        win = CrazyBrowser()
        win.show()

    # ---------- bookmarks ----------
    def add_current_bookmark(self):
        view = self.current_view()
        url = view.url().toString()
        title = view.title()
        if not url or url in ("about:blank",) or url.startswith("crazy://"):
            return
        for b in self.bookmarks:
            if b["url"] == url:
                QMessageBox.information(self, "Bookmark", "Already bookmarked.")
                return
        self.bookmarks.append({"url": url, "title": title})
        DataManager.save_json(BOOKMARKS_FILE, self.bookmarks)
        QMessageBox.information(self, "Bookmark", f"Added: {title}")

    def show_bookmarks_dialog(self):
        if not self.bookmarks:
            QMessageBox.information(self, "Bookmarks", "No bookmarks.")
            return
        dlg = QDialog(self)
        dlg.setWindowTitle("Manage Bookmarks")
        dlg.resize(500, 400)
        layout = QVBoxLayout()
        list_widget = QListWidget()
        for b in self.bookmarks:
            item = QListWidgetItem(f"{b['title']} - {b['url']}")
            item.setData(Qt.ItemDataRole.UserRole, b)
            list_widget.addItem(item)
        layout.addWidget(list_widget)

        btn_layout = QHBoxLayout()
        open_btn = QPushButton("Open")
        delete_btn = QPushButton("Delete")
        close_btn = QPushButton("Close")

        def open_bookmark():
            item = list_widget.currentItem()
            if item:
                b = item.data(Qt.ItemDataRole.UserRole)
                self.new_tab(b["url"], b["title"])
                dlg.accept()

        def delete_bookmark():
            item = list_widget.currentItem()
            if item:
                b = item.data(Qt.ItemDataRole.UserRole)
                self.bookmarks = [x for x in self.bookmarks if x["url"] != b["url"]]
                DataManager.save_json(BOOKMARKS_FILE, self.bookmarks)
                list_widget.takeItem(list_widget.row(item))

        open_btn.clicked.connect(open_bookmark)
        delete_btn.clicked.connect(delete_bookmark)
        close_btn.clicked.connect(dlg.accept)

        btn_layout.addWidget(open_btn)
        btn_layout.addWidget(delete_btn)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)
        dlg.setLayout(layout)
        dlg.exec()

    # ---------- history ----------
    def show_history_dialog(self):
        if not self.history_data:
            QMessageBox.information(self, "History", "No history.")
            return
        dlg = QDialog(self)
        dlg.setWindowTitle("History")
        dlg.resize(600, 400)
        layout = QVBoxLayout()
        list_widget = QListWidget()
        for h in reversed(self.history_data):
            item = QListWidgetItem(f"{h['title']} - {h['url']}  ({h['time'][:16]})")
            item.setData(Qt.ItemDataRole.UserRole, h)
            list_widget.addItem(item)
        layout.addWidget(list_widget)

        btn_layout = QHBoxLayout()
        open_btn = QPushButton("Open")
        close_btn = QPushButton("Close")

        def open_history():
            item = list_widget.currentItem()
            if item:
                h = item.data(Qt.ItemDataRole.UserRole)
                self.new_tab(h["url"], h["title"])
                dlg.accept()

        open_btn.clicked.connect(open_history)
        close_btn.clicked.connect(dlg.accept)
        btn_layout.addWidget(open_btn)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)
        dlg.setLayout(layout)
        dlg.exec()

    def clear_history(self):
        self.history_data = []
        DataManager.save_json(HISTORY_FILE, self.history_data)
        QMessageBox.information(self, "History", "History cleared.")

    # ---------- settings ----------
    def open_settings_tab(self):
        self.new_tab(SETTINGS_URL, "Settings")

    # ---------- close event ----------
    def closeEvent(self, event: QCloseEvent):
        if self.config.get("clear_history_on_close", False):
            self.clear_history()
        event.accept()

# ---------- entry point ----------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("crazy_browser")
    main = CrazyBrowser()
    main.show()
    sys.exit(app.exec())