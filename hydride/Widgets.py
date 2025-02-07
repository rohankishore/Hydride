# coding:utf-8

from PyQt6.QtCore import Qt, QUrl, QSize, QPoint
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel
from qfluentwidgets import (CardWidget, IconWidget, BodyLabel, CaptionLabel, TransparentToolButton, FluentIcon,
                            RoundMenu, Action, ImageLabel, SimpleCardWidget,
                            HeaderCardWidget, HyperlinkLabel, PrimaryPushButton, TitleLabel, PillPushButton, setFont,
                            VerticalSeparator)
from PyQt6.QtGui import QFont, QLinearGradient, QColor, QPalette, QBrush, QIcon
from PyQt6.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QSpacerItem, QSizePolicy)

class PhysicsCard(CardWidget):
    def __init__(self, icon, title, content, parent=None):
        super().__init__(parent)
        self.iconWidget = IconWidget(icon)
        self.titleLabel = BodyLabel(title, self)
        self.contentLabel = CaptionLabel(content, self)
        self.moreButton = TransparentToolButton(FluentIcon.RIGHT_ARROW, self)

        self.parent = parent

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#202020"))
        gradient.setColorAt(1.0, QColor("#202020"))
        palette.setBrush(QPalette.ColorRole.Window, QBrush(gradient))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        self.setFixedHeight(210)
        self.setFixedWidth(300)
        self.setStyleSheet("background-color: #f67913; border-radius: 10px;")  # Green background
        self.iconWidget.setFixedSize(48, 48)
        self.contentLabel.setTextColor("#ffffff", "#d2d2d2")  # Adjusted text color for contrast

        # Increase title font size
        self.titleLabel.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")

        self.hBoxLayout.setContentsMargins(20, 11, 11, 11)
        self.hBoxLayout.setSpacing(15)
        self.hBoxLayout.addWidget(self.iconWidget)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignmentFlag.AlignVCenter)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignmentFlag.AlignVCenter)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.hBoxLayout.addLayout(self.vBoxLayout)

        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.moreButton, 0, Qt.AlignmentFlag.AlignRight)

        self.moreButton.setFixedSize(32, 32)
        self.moreButton.clicked.connect(self.onMoreButtonClicked)

    def onMoreButtonClicked(self):
        menu = RoundMenu(parent=self)
        view_todays_reminders = Action(FluentIcon.VIEW, "View Today's Reminders", self)
        view_todays_reminders.triggered.connect(self.parent.today_reminders)
        menu.addAction(view_todays_reminders)

        x = (self.moreButton.width() - menu.width()) // 2 + 10
        pos = self.moreButton.mapToGlobal(QPoint(x, self.moreButton.height()))
        menu.exec(pos)


class ChemCard(CardWidget):
    def __init__(self, icon, title, content, parent=None):
        super().__init__(parent)
        self.iconWidget = IconWidget(icon)
        self.titleLabel = BodyLabel(title, self)
        self.titleLabel.setFixedWidth(75)
        self.contentLabel = CaptionLabel(content, self)
        self.moreButton = TransparentToolButton(FluentIcon.RIGHT_ARROW, self)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#059851"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        self.parent = parent

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedHeight(210)
        self.setFixedWidth(300)
        self.setStyleSheet("background-color: #39af4e; border-radius: 10px; opacity: 10;")
        self.iconWidget.setFixedSize(48, 48)
        self.contentLabel.setTextColor("#000000", "#059851")  # Adjusted text color for contrast

        # Increase title font size
        self.titleLabel.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")

        self.hBoxLayout.setContentsMargins(20, 11, 11, 11)
        self.hBoxLayout.setSpacing(15)
        self.hBoxLayout.addWidget(self.iconWidget)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignmentFlag.AlignVCenter)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignmentFlag.AlignVCenter)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.hBoxLayout.addLayout(self.vBoxLayout)

        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.moreButton, 0, Qt.AlignmentFlag.AlignRight)

        self.moreButton.setFixedSize(32, 32)
        self.moreButton.clicked.connect(self.onMoreButtonClicked)

    def onMoreButtonClicked(self):
        menu = RoundMenu(parent=self)
        view_todays_reminders = Action(FluentIcon.VIEW, "View Today's Reminders", self)
        view_todays_reminders.triggered.connect(self.parent.today_reminders)
        menu.addAction(view_todays_reminders)

        x = (self.moreButton.width() - menu.width()) // 2 + 10
        pos = self.moreButton.mapToGlobal(QPoint(x, self.moreButton.height()))
        menu.exec(pos)


class MathCard(CardWidget):
    def __init__(self, icon, title, content, parent=None):
        super().__init__(parent)
        self.iconWidget = IconWidget(icon)
       # self.titleLabel = QLabel(title, self)
        self.contentLabel = CaptionLabel(content, self)
        self.moreButton = TransparentToolButton(FluentIcon.RIGHT_ARROW, self)

        self.parent = parent

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        #self.titleLabel.setFixedWidth(75)


        self.setFixedHeight(210)
        self.setFixedWidth(300)
        #self.setStyleSheet("background-color: #005cb0; border-radius: 10px;")  # Green background
        self.iconWidget.setFixedSize(300, 80)
        #self.contentLabel.setTextColor("#ffffff", "#d2d2d2")  # Adjusted text color for contrast

        # Increase title font size
        #self.titleLabel.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")

        #self.hBoxLayout.setContentsMargins(20, 11, 11, 11)
        self.hBoxLayout.setSpacing(15)
#        self.hBoxLayout.addWidget(self.iconWidget)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.addWidget(self.iconWidget)
        #self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignmentFlag.AlignVCenter)
        #self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignmentFlag.AlignVCenter)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.hBoxLayout.addLayout(self.vBoxLayout)

        #self.hBoxLayout.addStretch(1)
        #self.hBoxLayout.addWidget(self.moreButton, 0, Qt.AlignmentFlag.AlignRight)

        self.moreButton.setFixedSize(32, 32)
        self.moreButton.clicked.connect(self.onMoreButtonClicked)

    def onMoreButtonClicked(self):
        menu = RoundMenu(parent=self)
        view_todays_reminders = Action(FluentIcon.VIEW, "View Today's Reminders", self)
        view_todays_reminders.triggered.connect(self.parent.today_reminders)
        menu.addAction(view_todays_reminders)

        x = (self.moreButton.width() - menu.width()) // 2 + 10
        pos = self.moreButton.mapToGlobal(QPoint(x, self.moreButton.height()))
        menu.exec(pos)
