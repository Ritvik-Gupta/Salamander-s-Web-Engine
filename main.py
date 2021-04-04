import os
import socket
import sys
from threading import Thread
from typing import Any

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QUrl as Url
from PyQt5.QtWebEngineWidgets import QWebEngineView as WebEngineView
from PyQt5.QtWidgets import QAction as Action
from PyQt5.QtWidgets import QApplication as Application
from PyQt5.QtWidgets import QDockWidget as DockWidget
from PyQt5.QtWidgets import QLineEdit as LineEdit
from PyQt5.QtWidgets import QListWidget as ListWidget
from PyQt5.QtWidgets import QMainWindow as MainWindow
from PyQt5.QtWidgets import QToolBar as NavBar

homePageUrl = "https://www.google.com"
Qt: Any = Qt


def fetchHostIpAddress() -> str:
    return socket.gethostbyname(socket.gethostname())


def executeSystemCommand(command: str) -> None:
    systemThread = Thread(target=lambda: os.system('cmd /k "' + command + '"'))
    systemThread.start()


class NetworksBrowserWindow(MainWindow):
    def __init__(self):
        super(NetworksBrowserWindow, self).__init__()
        self.browserEngineView = WebEngineView()
        self.browserEngineView.setUrl(Url(homePageUrl))
        self.setCentralWidget(self.browserEngineView)
        self.showMaximized()

        self.createNavBar()
        self.createDockWidget()

        self.browserEngineView.urlChanged.connect(self.updateUrl)

    def createDockWidget(self) -> None:
        dockWidget = DockWidget("Executed Operations", self)
        self.addDockWidget(Qt.RightDockWidgetArea, dockWidget)

        self.listWidget = ListWidget()
        dockWidget.setWidget(self.listWidget)
        dockWidget.setFloating(False)
        self.listWidget.setSpacing(10)

    def createNavBar(self) -> None:
        navbar = NavBar()
        self.addToolBar(navbar)
        self.addToolBarBreak()

        backButton = Action("Go Back", self)
        backButton.triggered.connect(self.browserEngineView.back)

        forwardButton = Action("Go Forward", self)
        forwardButton.triggered.connect(self.browserEngineView.forward)

        reloadButton = Action("Reload Page", self)
        reloadButton.triggered.connect(self.browserEngineView.reload)

        homeButton = Action("Go to Home", self)
        homeButton.triggered.connect(self.navigateHome)

        networkDetailsButton = Action("Network Details", self)
        networkDetailsButton.triggered.connect(self.fetchNetworkDetails)

        ipConfigButton = Action("IP Config", self)
        ipConfigButton.triggered.connect(self.fetchIpConfig)

        navbar.addActions(
            [
                backButton,
                forwardButton,
                reloadButton,
                homeButton,
                networkDetailsButton,
                ipConfigButton,
            ]
        )
        self.urlBar = LineEdit()
        self.urlBar.returnPressed.connect(self.navigateToUrl)
        navbar.addWidget(self.urlBar)

    def navigateHome(self) -> None:
        self.listWidget.addItem("Navigating Back to Home")
        self.browserEngineView.setUrl(Url(homePageUrl))
        self.listWidget.addItem("Navigation Back to Home Ended")

    def navigateToUrl(self) -> None:
        self.listWidget.addItem("Navigating to given url")
        windowUrl = self.urlBar.text()
        self.browserEngineView.setUrl(Url(windowUrl))
        self.listWidget.addItem("Navigation to given url Ended")

    def updateUrl(self, query: Any) -> None:
        self.listWidget.addItem("Updating url")
        self.urlBar.setText(query.toString())
        self.listWidget.addItem("Update operation on url Ended")

    def fetchIpConfig(self) -> None:
        self.listWidget.addItem("Fetching System's IP Config")
        executeSystemCommand("ipconfig")

    def fetchNetworkDetails(self) -> None:
        self.listWidget.addItem("Fetching Network Details")
        try:
            ipAddress = fetchHostIpAddress()
            print("\nWindow IP address is :\t", ipAddress)
            windowUrl = self.urlBar.text()
            formattedUrl = windowUrl[windowUrl.find("www.") + 4 : windowUrl.rfind("/")]

            tracertWithUrl = "tracert " + formattedUrl
            self.listWidget.addItem("Executing '" + tracertWithUrl + "'")
            executeSystemCommand(tracertWithUrl)
        except:
            self.listWidget.addItem("Could not Fetch Network Details")


def main() -> None:
    app = Application(sys.argv)
    app.setApplicationName("Salamander's Browser")
    window = NetworksBrowserWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
