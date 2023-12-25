from PyQt6 import QtCore
import requests
from bs4 import BeautifulSoup


class htmlThread(QtCore.QThread):

    def setter(self, url, ui):
        self.url = url
        self.html = None
        self.ui = ui

    def getter(self):
        self.ui.html = self.html
        self.ui.FoundHtml()

    def run(self):
        s = requests.Session()
        html = s.get(self.url)
        s.close()
        self.html = BeautifulSoup(html.content, 'html.parser')
        self.getter()


class jsonThread(QtCore.QThread):

    def setter(self, url, ui, session):
        self.session = session
        self.url = url
        self.json_content = None
        self.ui = ui

    def getter(self):
        self.ui.json = self.json_content
        self.ui.FoundJson()

    def run(self):
        self.json_content: requests.get = self.session.get(self.url).json()
        print()
        self.getter()


class loggedInThread(QtCore.QThread):

    def setter(self, url, ui, session):
        self.session = session
        self.url = url
        self.json_content = None
        self.ui = ui

    def getter(self):
        self.ui.seats_data = self.json_content
        self.ui.FoundSeatData()

    def run(self):
        self.json_content = self.session.get(self.url).json()
        self.getter()
