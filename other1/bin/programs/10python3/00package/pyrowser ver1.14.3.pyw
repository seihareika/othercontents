import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTabWidget, QPushButton, QLineEdit, QMenu, QAction, QListWidget, QListWidgetItem, QFileDialog, QSlider, QDialog, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineSettings
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QClipboard, QCursor

class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, browser, parent=None):
        super().__init__(parent)
        self.browser = browser

    def acceptNavigationRequest(self, url, _type, isMainFrame):
        if _type == QWebEnginePage.NavigationTypeLinkClicked and isMainFrame:
            self.browser.tabs.currentWidget().setUrl(url)
            return False
        return super().acceptNavigationRequest(url, _type, isMainFrame)

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        print(f"JavaScript Console: {message} (line: {lineNumber})")

    def inject_adblocker(self):
        with open('adblocker.js', 'r') as f:
            adblock_script = f.read()
        self.runJavaScript(adblock_script)

class Browser(QMainWindow):
    def show_bookmarks(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("ブックマーク")
        bookmark_list = QListWidget(dialog)
        bookmark_list.itemDoubleClicked.connect(self.open_bookmark)
        bookmark_list.itemClicked.connect(self.handle_bookmark_click)
        bookmarks_path = os.path.join(os.path.dirname(__file__), "bookmarks", "bookmarks.txt")
        if os.path.exists(bookmarks_path):
            with open(bookmarks_path, 'r') as f:
                for line in f:
                    url = line.strip()
                    item = QListWidgetItem(url)
                    bookmark_list.addItem(item)
        layout = QVBoxLayout()
        layout.addWidget(bookmark_list)
        dialog.setLayout(layout)
        dialog.exec_()

    def handle_bookmark_click(self, item):
        context_menu = QMenu(self)
        open_action = context_menu.addAction("開く")
        delete_action = context_menu.addAction("削除")

        action = context_menu.exec_(QCursor.pos())

        if action == open_action:
            self.open_bookmark(item)
        elif action == delete_action:
            self.delete_bookmark(item)

    def delete_bookmark(self, item):
        url = item.text()
        bookmarks_path = os.path.join(os.path.dirname(__file__), "bookmarks", "bookmarks.txt")

        with open(bookmarks_path, 'r') as f:
            lines = f.readlines()

        with open(bookmarks_path, 'w') as f:
            for line in lines:
                if line.strip() != url:
                    f.write(line)

        print(f"Deleted bookmark: {url}")

    def open_bookmark(self, item):
        url = item.text()
        self.add_new_tab(QUrl(url))

    def bookmark_page(self):
        current_url = self.tabs.currentWidget().url().toString()
        bookmarks_path = os.path.join(os.path.dirname(__file__), "bookmarks", "bookmarks.txt")
        with open(bookmarks_path, 'a') as f:
            f.write(current_url + '\n')
        print(f"Bookmarked: {current_url}")

    def __init__(self):
        super().__init__()
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.tabBarDoubleClicked.connect(self.add_new_tab)
        self.tabs.currentChanged.connect(self.update_zoom_label)
        
        self.zoom_label = QLineEdit('75')
        self.zoom_label.setFixedWidth(30)
        self.zoom_label.returnPressed.connect(self.set_zoom_from_label)
        
        self.url_bar = QLineEdit()
        self.url_bar.setAlignment(Qt.AlignLeft)
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        
        self.back_btn = QPushButton('←')
        self.back_btn.setFixedWidth(30)
        self.forward_btn = QPushButton('→')
        self.forward_btn.setFixedWidth(30)
        self.new_tab_btn = QPushButton('AddNewTab')
        self.new_tab_btn.clicked.connect(self.add_new_tab)
        self.back_btn.clicked.connect(self.go_back)
        self.forward_btn.clicked.connect(self.go_forward)
        
        self.zoom_in_btn = QPushButton('+')
        self.zoom_in_btn.setFixedWidth(20)
        self.zoom_out_btn = QPushButton('-')
        self.zoom_out_btn.setFixedWidth(20)
        self.zoom_in_btn.clicked.connect(self.zoom_in)
        self.zoom_out_btn.clicked.connect(self.zoom_out)
        
        self.refresh_btn = QPushButton('⟳')
        self.refresh_btn.setFixedWidth(20)
        self.refresh_btn.clicked.connect(self.refresh_page)
        
        self.menu_btn = QPushButton('☰')
        self.menu = QMenu()
        self.menu_btn.setFixedWidth(35)
        
        bookmark_action = QAction('ブックマークに保存', self)
        bookmark_action.triggered.connect(self.bookmark_page)
        print_action = QAction('印刷', self)
        print_action.triggered.connect(self.print_page)
        bookmarks_list_action = QAction('ブックマーク一覧を表示', self)
        bookmarks_list_action.triggered.connect(self.show_bookmarks)
        history_list_action = QAction('閲覧履歴を表示', self)
        history_list_action.triggered.connect(self.show_history)
        dev_tools_action = QAction('開発者ツール', self)
        dev_tools_action.triggered.connect(self.open_dev_tools)
        
        self.menu.addAction(bookmark_action)
        self.menu.addAction(bookmarks_list_action)
        self.menu.addAction(print_action)
        self.menu.addAction(history_list_action)
        self.menu.addAction(dev_tools_action)
        self.menu_btn.setMenu(self.menu)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_btn)
        button_layout.addWidget(self.forward_btn)
        button_layout.addWidget(self.new_tab_btn)
        button_layout.addWidget(self.zoom_out_btn)
        button_layout.addWidget(self.zoom_label)
        button_layout.addWidget(self.zoom_in_btn)
        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.url_bar)
        button_layout.addWidget(self.menu_btn)
        
        control_widget = QWidget()
        control_layout = QVBoxLayout()
        control_layout.addLayout(button_layout)
        control_layout.addWidget(self.tabs)
        control_widget.setLayout(control_layout)
        self.setCentralWidget(control_widget)
        
        self.setWindowTitle('Pyrowser Ver1.14.3')
        self.resize(375, 690)
        self.setStyleSheet("background-color: #141414; color: #AFAFAF;")
        
        self.bookmarks = []
        self.history = []
        self.bookmarks_window = None
        self.history_window = None
        
        self.add_new_tab(QUrl('https://www.google.co.jp'))

        self.back_btn.setStyleSheet("background-color: #330033;")
        self.forward_btn.setStyleSheet("background-color: #330033;")
        self.new_tab_btn.setStyleSheet("background-color: #330033;")
        self.zoom_in_btn.setStyleSheet("background-color: #330033;")
        self.zoom_out_btn.setStyleSheet("background-color: #330033;")
        self.refresh_btn.setStyleSheet("background-color: #330033;")
        self.menu_btn.setStyleSheet("background-color: #330033;")

    def add_new_tab(self, url=None):
        if url is None:
            url = QUrl('https://www.google.co.jp')
        browser = QWebEngineView()
        browser.setPage(CustomWebEnginePage(self))
        browser.setUrl(url)
        i = self.tabs.addTab(browser, url.toString())
        self.tabs.setCurrentIndex(i)

    def refresh_page(self):
        current_view = self.tabs.currentWidget()
        if current_view:
            current_view.reload()
    
    def open_dev_tools(self):
        current_view = self.tabs.currentWidget()
        if current_view:
            current_view.page().setDevToolsPage(CustomWebEnginePage(self))
            self.add_new_tab(QUrl("about:blank"))

    def add_new_tab(self, qurl=None):
        if qurl is None or isinstance(qurl, int):
            qurl = QUrl('https://www.google.co.jp')
        browser = QWebEngineView()
        browser.setPage(CustomWebEnginePage(self))
        browser.setUrl(qurl)
        browser.setZoomFactor(0.60)
        browser.titleChanged.connect(lambda title, browser=browser: self.update_tab_title(title, browser))
        browser.urlChanged.connect(self.update_url_bar)
        i = self.tabs.addTab(browser, "Loading...")
        self.tabs.setCurrentIndex(i)
        self.update_zoom_label()
        self.update_url_bar()

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def update_tab_title(self, title, browser):
        index = self.tabs.indexOf(browser)
        if index != -1:
            self.tabs.setTabText(index, title)

    def update_zoom_label(self):
        current_view = self.tabs.currentWidget()
        if current_view:
            zoom_factor = current_view.zoomFactor() * 100
            self.zoom_label.setText(f'{zoom_factor:.0f}')
            self.update_url_bar()

    def zoom_in(self):
        current_view = self.tabs.currentWidget()
        if current_view:
            current_view.setZoomFactor(current_view.zoomFactor() + 0.1)
            self.update_zoom_label()

    def zoom_out(self):
        current_view = self.tabs.currentWidget()
        if current_view:
            current_view.setZoomFactor(current_view.zoomFactor() - 0.1)
            self.update_zoom_label()

    def set_zoom_from_label(self):
        try:
            zoom_factor = int(self.zoom_label.text()) / 100.0
            zoom_factor = max(0.25, min(zoom_factor, 5))
            current_view = self.tabs.currentWidget()
            if current_view:
                current_view.setZoomFactor(zoom_factor)
                self.zoom_label.setText(f'{zoom_factor * 100:.0f}')
        except ValueError:
            print("Invalid zoom input")

    def navigate_to_url(self):
        url = QUrl(self.url_bar.text())
        if url.scheme() == "":
            url.setScheme("http")
        current_view = self.tabs.currentWidget()
        if current_view and isinstance(current_view, QWebEngineView):
            current_view.setUrl(url)
            self.history.append(url.toString())  # Add URL to history

    def update_url_bar(self, url=None):
        if url is None:
            current_view = self.tabs.currentWidget()
            if current_view and isinstance(current_view, QWebEngineView):
                self.url_bar.setText(current_view.url().toString())
        else:
            self.url_bar.setText(url.toString())

    def go_back(self):
        current_view = self.tabs.currentWidget()
        if current_view and current_view.history().canGoBack():
            current_view.back()

    def go_forward(self):
        current_view = self.tabs.currentWidget()
        if current_view and current_view.history().canGoForward():
            current_view.forward()

    def print_page(self):
        current_view = self.tabs.currentWidget()
        if current_view:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf);;All Files (*)", options=options)
            if file_path:
                current_view.page().printToPdf(file_path)
                print(f'Saved PDF to {file_path}')

    def show_history(self):
        if self.history_window is None or not self.history_window.isVisible():
            self.history_window = QWidget()
            layout = QVBoxLayout()
            history_list = QListWidget()
            for entry in self.history:
                item = QListWidgetItem(entry)
                history_list.addItem(item)
            layout.addWidget(history_list)
            self.history_window.setLayout(layout)
            self.history_window.setWindowTitle('閲覧履歴')
            self.history_window.resize(400, 300)
            self.history_window.show()

    def copy_to_clipboard(self, item):
        clipboard = QApplication.clipboard()
        clipboard.setText(item.text())
        print(f'Copied {item.text()} to clipboard')  # Optional print to console for confirmation

app = QApplication(sys.argv)
window = Browser()
window.show()
window.resize(370, 690)  # Ensure the window is resized after showing
sys.exit(app.exec_())