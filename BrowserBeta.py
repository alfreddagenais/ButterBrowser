# Imports
import sys
import requests
from PyQt5.QtCore import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

# Vars
useMoreSearchEngines = True
moreEngineRawDataAddress = 'https://raw.githubusercontent.com/Parsa-GP/api/gh-pages/SE_iran.json'
defaultSearchEngine = 'Google'

# Functions
def mergeDict(dict1, dict2):
    res = {**dict1, **dict2}
    return res

# Set default vars
seData = requests.get("https://raw.githubusercontent.com/Parsa-GP/api/gh-pages/search_engines.json")
searchEngine = seData.json()
if useMoreSearchEngines == True:
    aseData = requests.get(moreEngineRawDataAddress)
    altSearchEngine = aseData.json()
    searchEngines = mergeDict(searchEngine, altSearchEngine)

defaultSE = defaultSearchEngine
homePage = searchEngines[defaultSE][0]
searchArgs = searchEngines[defaultSE][1]

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(homePage))
        self.setCentralWidget(self.browser)
        self.showMaximized()

        profile = QWebEngineProfile("storage", self.browser)
        cookie_store = profile.cookieStore()
        cookie_store.cookieAdded.connect(self.onCookieAdded)
        self.cookies = []

        # Add widgets to navbar
        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QAction('\u25C0', self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        forward_btn = QAction('\u25B6', self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        reload_btn = QAction('\u21bb', self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        home_btn = QAction('\u2302', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        self.cb = QComboBox()
        self.cb.addItems(searchEngines)
        self.cb.currentIndexChanged.connect(self.selectionchange)
        navbar.addWidget(self.cb)

        self.browser.urlChanged.connect(self.update_url)
        self.browser.loadFinished.connect(self.finished_url)

    # Functions
    def onCookieAdded(self, cookie):
        for c in self.cookies:
            if c.hasSameIdentifier(cookie):
                return
        self.cookies.append(QNetworkCookie(cookie))
        self.toJson()

    def toJson(self):
        cookies_list_info = []
        for c in self.cookies:
            data = {"name": bytearray(c.name()).decode(), "domain": c.domain(), "value": bytearray(c.value()).decode(),
                    "path": c.path(), "expirationDate": c.expirationDate().toString(Qt.ISODate), "secure": c.isSecure(),
                    "httponly": c.isHttpOnly()}
            cookies_list_info.append(data)
        print("Cookie as list of dictionary:")
        print(cookies_list_info)

    def selectionchange(self,i):
        global homePage
        global searchArgs
        homePage = searchEngines[self.cb.currentText()][0]
        searchArgs = searchEngines[self.cb.currentText()][1]


    def navigate_home(self):
        self.browser.setUrl(QUrl(homePage))

    def navigate_to_url(self):
        url = self.url_bar.text()
        if url[0:7] == 'http://' or url[0:8] == 'https://' or url[0:6] == 'about:':
            self.url_bar.setText(url)
            self.browser.setUrl(QUrl(url))
        else:
            self.url_bar.setText(f'{searchArgs}{url}')
            self.browser.setUrl(QUrl(f'{searchArgs}{url}'))

    def update_url(self, q):
        address = q.toString()
        self.url_bar.setText(q.toString())


    def finished_url(self, q):
        title = self.browser.page().title()
        self.setWindowTitle(f'{title} - Browser')\
        
# Run the app
app = QApplication(sys.argv)
QApplication.setApplicationName('Browser')
window = MainWindow()
app.exec_()