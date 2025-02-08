# coding:utf-8
import sys

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtWidgets import QApplication, QFrame, QStatusBar

from qfluentwidgets import (NavigationBar, NavigationItemPosition, isDarkTheme, setTheme, Theme,
                            PopUpAniStackedWidget)
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import FramelessWindow, TitleBar
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QLinearGradient, QColor, QPalette, QBrush
from PyQt6.QtWidgets import QLabel, QHBoxLayout, QWidget
import json
import onboarding, flashcard
import testhome as home

CONFIG_FILE = "resources/data/json/init.json"

with open(CONFIG_FILE, "r") as config_file:
    _config = json.load(config_file)

name = _config["name"]
field = _config["field"]


class Widget(QWidget):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = QLabel(text, self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))


class StackedWidget(QFrame):
    currentChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.view = PopUpAniStackedWidget(self)

        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.view)
        self.view.currentChanged.connect(self.currentChanged)

    def addWidget(self, widget):
        self.view.addWidget(widget)

    def widget(self, index: int):
        return self.view.widget(index)

    def setCurrentWidget(self, widget, popOut=False):
        self.view.setCurrentWidget(widget, duration=300)

    def setCurrentIndex(self, index, popOut=False):
        self.setCurrentWidget(self.view.widget(index), popOut)

    def previousIndex(self):
        return max(0, self.view.currentIndex() - 1)


class CustomTitleBar(TitleBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.iconLabel = QLabel(self)
        self.iconLabel.setFixedSize(18, 18)
        self.hBoxLayout.insertSpacing(0, 10)
        self.hBoxLayout.insertWidget(1, self.iconLabel, 0, Qt.AlignmentFlag.AlignLeft)
        self.window().windowIconChanged.connect(self.setIcon)

        self.titleLabel = QLabel(self)
        self.hBoxLayout.insertWidget(2, self.titleLabel, 0, Qt.AlignmentFlag.AlignLeft)
        self.titleLabel.setObjectName('titleLabel')
        self.window().windowTitleChanged.connect(self.setTitle)

    def setTitle(self, title):
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()

    def setIcon(self, icon):
        self.iconLabel.setPixmap(QIcon(icon).pixmap(18, 18))


class Window(FramelessWindow):
    def __init__(self):
        super().__init__()
        self.setTitleBar(CustomTitleBar(self))
        self.hBoxLayout = QHBoxLayout(self)
        self.navigationBar = NavigationBar(self)
        self.stackWidget = StackedWidget(self)

        """
        to get the screen's width and height. For future use. 
        """

        screen = QGuiApplication.primaryScreen()  # Get the primary screen
        if screen:  # Check if a screen is available
            geometry = screen.availableGeometry()
            screen_width = geometry.width()
            screen_height = geometry.height()

        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, self.height())  # Adjust gradient to span the entire height
        gradient.setColorAt(0.0, QColor("#1b2033"))  # Top gradient color (darker shade)
        gradient.setColorAt(1.0, QColor("#202020"))  # Bottom gradient color (slightly lighter shade)
        palette.setBrush(QPalette.ColorRole.Window, QBrush(gradient))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        status_bar = QStatusBar(self)
        status_bar.setLayout(self.hBoxLayout)

        setTheme(Theme.DARK)

        self.homeInterface = home.StackableWidget()
        self.appInterface = Widget('Test Interface', self)
        self.videoInterface = Widget('Notebook Interface', self)
        self.flashcardInterface = flashcard.FlashcardWidget()

        self.initLayout()
        self.initNavigation()
        self.setQss()
        self.initWindow()

    def initLayout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 48, 0, 0)
        self.hBoxLayout.addWidget(self.navigationBar)
        self.hBoxLayout.addWidget(self.stackWidget)
        self.hBoxLayout.setStretchFactor(self.stackWidget, 1)

    def setQss(self):
        color = 'dark' if isDarkTheme() else 'light'
        with open(f'resources/{color}/demo.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, 'Home', selectedIcon=FIF.HOME_FILL)
        self.addSubInterface(self.appInterface, FIF.PENCIL_INK, 'Tests')
        self.addSubInterface(self.videoInterface, FIF.BOOK_SHELF, 'Notebooks', selectedIcon=FIF.LIBRARY_FILL)
        self.addSubInterface(self.flashcardInterface, QIcon("resources/icons/icon/flashcards.png"), 'Flashcards',
                             NavigationItemPosition.BOTTOM,
                             QIcon("resources/icons/icon/flashcards.png"))
        self.stackWidget.currentChanged.connect(self.onCurrentInterfaceChanged)
        self.navigationBar.setCurrentItem(self.homeInterface.objectName())

    def initWindow(self):
        # self.resize(900, 700)
        self.showMaximized()
        self.setWindowTitle('Hydride')
        setTheme(Theme.DARK)

    def addSubInterface(self, interface, icon, text: str, position=NavigationItemPosition.TOP, selectedIcon=None):
        self.stackWidget.addWidget(interface)
        self.navigationBar.addItem(
            routeKey=interface.objectName(),
            icon=icon,
            text=text,
            onClick=lambda: self.switchTo(interface),
            selectedIcon=selectedIcon,
            position=position,
        )

    def switchTo(self, widget):
        self.stackWidget.setCurrentWidget(widget)

    def onCurrentInterfaceChanged(self, index):
        widget = self.stackWidget.widget(index)
        self.navigationBar.setCurrentItem(widget.objectName())

    def goBack(self):
        previous_index = self.stackWidget.previousIndex()
        self.stackWidget.setCurrentIndex(previous_index)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open("resources/data/json/init.json", "r") as config_file:
        _config = json.load(config_file)
    if _config["onboarding"]:
        w = Window()
        w.show()
    else:
        onboarding_dialog = onboarding.OnboardingScreen()
        onboarding_dialog.exec()
        w = Window()
        w.show()

    app.exec()
