# Imports
import sys
import requests
from PyQt5.QtCore import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

# Set dafault vars
'''searchEngines = {'Google':['http://google.com/?hl=en', 'https://www.google.com/search?q=']}'''
seData = requests.get("https://raw.githubusercontent.com/Parsa-GP/api/gh-pages/search_engines.json")
searchEngines = seData.json()
defaultSE = 'Google'
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

        # Add widdgets to navbar
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
        self.setWindowTitle(f'Browser - {title}')

#Run the app
app = QApplication(sys.argv)
QApplication.setApplicationName('Browser')
window = MainWindow()
app.exec_()