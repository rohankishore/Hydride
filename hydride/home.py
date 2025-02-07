# coding:utf-8
import json

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QLinearGradient, QColor, QPalette, QBrush, QIcon
from PyQt6.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QSpacerItem, QSizePolicy,
    QScrollArea
)
from qfluentwidgets import LargeTitleLabel, CaptionLabel

import Widgets

# import qdarktheme

with open("resources/data/json/init.json", "r") as config_file:
    _config = json.load(config_file)

name = _config["name"]
field = _config["field"]

# coding:utf-8
import json

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QLinearGradient, QColor, QPalette, QBrush, QIcon
from PyQt6.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QSpacerItem, QSizePolicy,
    QScrollArea, QStackedWidget
)
from qfluentwidgets import LargeTitleLabel, CaptionLabel

import Widgets

# import qdarktheme

with open("resources/data/json/init.json", "r") as config_file:
    _config = json.load(config_file)

name = _config["name"]
field = _config["field"]

import json
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QLinearGradient, QColor, QPalette, QBrush, QIcon
from PyQt6.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QSpacerItem, QSizePolicy,
    QScrollArea, QLabel
)
from qfluentwidgets import LargeTitleLabel, CaptionLabel

# import qdarktheme

with open("resources/data/json/init.json", "r") as config_file:
    _config = json.load(config_file)

name = _config["name"]
field = _config["field"]


class SubjectContentWindow(QWidget):
    def __init__(self, subject_name, parent):
        super().__init__()
        self.subject_name = subject_name
        self.parent_widget = parent  # Keep track of parent widget (Dashboard)
        self.setWindowTitle(f"{self.subject_name} Content")

        self.layout = QVBoxLayout(self)

        content_label = QLabel(f"Welcome to {self.subject_name} content!", self)
        content_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(content_label)

        # Back button to go back to home screen (Dashboard)
        self.back_button = QPushButton("Back")
        self.back_button.setFixedSize(QSize(110, 50))
        self.back_button.setFont(QFont("Poppins", 12, QFont.Weight.Bold))
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #222d3f;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                border: 2px solid #007BFF; /* Blue border on hover */
            }
        """)
        self.back_button.clicked.connect(self.closeSubjectWindow)
        self.layout.addWidget(self.back_button)

    def closeSubjectWindow(self):
        """ Close the current subject window and return to the dashboard. """
        self.close()
        self.parent_widget.show()  # Show the parent widget (Dashboard) again


class SubjectContentWidget(QWidget):
    def __init__(self, subject_name, parent):
        super().__init__()
        self.subject_name = subject_name
        self.parent_widget = parent  # Keep track of parent widget (Dashboard)
        self.setWindowTitle(f"{self.subject_name} Content")

        layout = QVBoxLayout(self)

        content_label = QLabel(f"Welcome to {self.subject_name} content!", self)
        content_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(content_label)

        back_button = QPushButton("Back")
        back_button.setFixedSize(QSize(110, 50))
        back_button.setFont(QFont("Poppins", 12, QFont.Weight.Bold))
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #222d3f;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                border: 2px solid #007BFF; /* Blue border on hover */
            }
        """)
        back_button.clicked.connect(self.back_to_dashboard)
        layout.addWidget(back_button)

    def back_to_dashboard(self):
        """ Replace the current widget with the dashboard. """
        self.parent_widget.setCurrentIndex(0)  # Show the first widget (Dashboard)

class DashboardWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)

        # Set gradient background (This part is already correct)
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#202020"))
        gradient.setColorAt(1.0, QColor("#202020"))
        palette.setBrush(QPalette.ColorRole.Window, QBrush(gradient))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(25, 25, 25, 25)

        self.greeting_bar = QWidget()
        self.greeting_bar.setFixedHeight(120)
        self.greeting_bar_layout = QVBoxLayout(self.greeting_bar)
        self.greeting_bar_layout.setContentsMargins(0, 0, 0, 0)

        self.title_label = LargeTitleLabel(f"👋 Hey, {name}")
        self.title_label.setFont(QFont("Poppins", 35, QFont.Weight.DemiBold))
        self.title_label.setStyleSheet("color: #ffffff;")

        caption_emoji = "➗ " if field == "Engineering" else "🩺 "
        caption = "            " + caption_emoji + field
        self.field_caption = CaptionLabel(caption)
        self.field_caption.setFont(QFont("Poppins", 15, QFont.Weight.DemiBold))

        self.greeting_bar_layout.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignVCenter)
        self.greeting_bar_layout.addWidget(self.field_caption, alignment=Qt.AlignmentFlag.AlignVCenter)
        self.main_layout.addWidget(self.greeting_bar)

        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("border: none; background: transparent;")
        self.scroll_area.setWidgetResizable(True)

        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)
        self.main_layout.addWidget(self.scroll_area)

        self.scroll_layout.addSpacerItem(QSpacerItem(20, 50))

        pyq_header = CaptionLabel("Chapter wise PYQ Bank")
        pyq_header.setFont(QFont("Poppins", 15, QFont.Weight.Bold))
        pyq_header.setStyleSheet("color: #ffffff;")
        self.scroll_layout.addWidget(pyq_header)
        self.scroll_layout.addSpacerItem(QSpacerItem(10, 10))

        self.button_layout = QHBoxLayout()
        self.jee_button = self.create_button("JEE", "resources/icons/icon/JEE.png")
        self.neet_button = self.create_button("NEET", "resources/icons/icon/NEET.png")
        self.keam_button = self.create_button("KEAM", "resources/icons/icon/KEAM.png")

        self.button_layout.addWidget(self.jee_button)
        self.button_layout.addWidget(self.neet_button)
        self.button_layout.addWidget(self.keam_button)
        self.button_layout.addStretch(1)
        self.scroll_layout.addLayout(self.button_layout)
        self.scroll_layout.addSpacerItem(QSpacerItem(20, 50))

        shortnotes_header = CaptionLabel("Short Notes")
        shortnotes_header.setFont(QFont("Poppins", 15, QFont.Weight.Bold))
        shortnotes_header.setStyleSheet("color: #ffffff;")
        self.scroll_layout.addWidget(shortnotes_header)

        self.shortnotes_layout = QHBoxLayout()
        self.scroll_layout.addLayout(self.shortnotes_layout)

        self.addCards(QIcon("resources/icons/icon/math_card.png"), self.showMathContent)
        self.addCards(QIcon("resources/icons/icon/chem_card.png"), self.showChemistryContent)
        self.addCards(QIcon("resources/icons/icon/phy_card.png"), self.showPhysicsContent)

        if field == "Engineering":
            self.neet_button.hide()
        elif field == "Medical":
            self.keam_button.hide()
            self.jee_button.hide()

        self.scroll_layout.addSpacerItem(QSpacerItem(20, 50, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Use QStackedWidget for switching between widgets
        self.stacked_widget = QStackedWidget(self)  # Notice the self passed here
        self.main_layout.addWidget(self.stacked_widget)  # Add QStackedWidget to layout
        self.stacked_widget.addWidget(self)  # Add the dashboard as the first widget

    def showMathContent(self):
        math_content_widget = SubjectContentWidget("Math", self)
        self.stacked_widget.addWidget(math_content_widget)
        self.stacked_widget.setCurrentWidget(math_content_widget)  # Switch to Math content widget

    def showChemistryContent(self):
        chemistry_content_widget = SubjectContentWidget("Chemistry", self)
        self.stacked_widget.addWidget(chemistry_content_widget)
        self.stacked_widget.setCurrentWidget(chemistry_content_widget)  # Switch to Chemistry content widget

    def showPhysicsContent(self):
        physics_content_widget = SubjectContentWidget("Physics", self)
        self.stacked_widget.addWidget(physics_content_widget)
        self.stacked_widget.setCurrentWidget(physics_content_widget)  # Switch to Physics content widget

    def addCards(self, icon, function):
        button = QPushButton()
        button.clicked.connect(function)
        button.setFixedSize(QSize(346, 232))
        button.setIcon(icon)
        button.setIconSize(QSize(345, 245))
        button.setStyleSheet(""" 
            QPushButton {
                background: none;
                border-radius: 10px;
                padding: 10px;
                border: none;
            }
            QPushButton:hover {
                border: 2px solid #007BFF;
            }
        """)
        self.shortnotes_layout.addWidget(button)

    def create_button(self, text, icon_path):
        button = QPushButton()
        button.setFixedSize(QSize(110, 80))
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(80, 60))
        button.setFont(QFont("Poppins", 14, QFont.Weight.Bold))
        button.setStyleSheet(""" 
            QPushButton {
                background-color: #222d3f;
                color: white;
                border-radius: 10px;
                padding: 10px;
                border: 2px solid transparent;
            }
            QPushButton:hover {
                border: 2px solid #007BFF;
            }
        """)
        return button
