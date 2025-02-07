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

        # Add content for subject (math/chemistry/physics)
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


class DashboardWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)
        self.spacer_item = QSpacerItem(30, 40)
        self.spacer_item_small = QSpacerItem(10, 10)

        # Set gradient background
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#202020"))
        gradient.setColorAt(1.0, QColor("#202020"))
        palette.setBrush(QPalette.ColorRole.Window, QBrush(gradient))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(25, 25, 25, 25)

        # ======== Greeting Bar (Fixed) ========
        self.greeting_bar = QWidget()
        self.greeting_bar.setStyleSheet("background-color: #202020;")
        self.greeting_bar.setFixedHeight(120)
        self.greeting_bar_layout = QVBoxLayout(self.greeting_bar)
        self.greeting_bar_layout.setContentsMargins(0, 0, 0, 0)

        self.title_label = LargeTitleLabel(f"👋 Hey, {name}")
        self.title_label.setFont(QFont("Poppins", 35, QFont.Weight.DemiBold))
        self.title_label.setStyleSheet("color: #ffffff;")

        caption_emoji = ""
        if _config["field"] == "Engineering":
            caption_emoji = "➗ "
        else:
            caption_emoji = "🩺 "

        caption = "            " + caption_emoji + _config["field"]
        self.field_caption = CaptionLabel(caption)
        self.field_caption.setFont(QFont("Poppins", 15, QFont.Weight.DemiBold))

        self.greeting_bar_layout.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignVCenter)
        self.greeting_bar_layout.addWidget(self.field_caption, alignment=Qt.AlignmentFlag.AlignVCenter)

        self.main_layout.addWidget(self.greeting_bar)  # Keep it fixed at the top

        # ======== Scrollable Area ========
        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("border: none; background: transparent;")  # Make it transparent
        self.scroll_area.setWidgetResizable(True)  # Make it resize dynamically

        self.scroll_widget = QWidget()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(gradient))
        self.scroll_widget.setPalette(palette)
        self.scroll_widget.setAutoFillBackground(True)
        self.scroll_layout = QVBoxLayout(self.scroll_widget)

        self.scroll_area.setWidget(self.scroll_widget)
        self.main_layout.addWidget(self.scroll_area)  # Add scrollable area

        # Spacer
        self.scroll_layout.addSpacerItem(QSpacerItem(20, 50))

        # ======== Content inside Scroll Area ========
        pyq_header = CaptionLabel("Chapter wise PYQ Bank")
        pyq_header.setFont(QFont("Poppins", 15, QFont.Weight.Bold))
        pyq_header.setStyleSheet("color: #ffffff;")
        self.scroll_layout.addWidget(pyq_header)
        self.scroll_layout.addSpacerItem(self.spacer_item_small)

        # Exam Buttons Layout
        self.button_layout = QHBoxLayout()

        self.jee_button = self.create_button("JEE", "resources/icons/icon/JEE.png")
        self.neet_button = self.create_button("NEET", "resources/icons/icon/NEET.png")
        self.keam_button = self.create_button("KEAM", "resources/icons/icon/KEAM.png")
        self.test2 = self.create_button("NEET", "resources/icons/icon/NEET.png")
        self.test3 = self.create_button("NEET", "resources/icons/icon/NEET.png")

        self.button_layout.addWidget(self.jee_button)
        self.button_layout.addWidget(self.neet_button)
        self.button_layout.addWidget(self.keam_button)
        self.button_layout.addStretch(1)  # Add stretch to distribute buttons evenly
        self.button_layout.addSpacing(10)
        self.scroll_layout.addLayout(self.button_layout)
        self.scroll_layout.addSpacerItem(self.spacer_item)

        shortnotes_header = CaptionLabel("Short Notes")
        shortnotes_header.setFont(QFont("Poppins", 15, QFont.Weight.Bold))
        shortnotes_header.setStyleSheet("color: #ffffff;")
        self.scroll_layout.addWidget(shortnotes_header)

        self.shortnotes_layout = QHBoxLayout()
        self.scroll_layout.addLayout(self.shortnotes_layout)

        self.addCards(icon=(QIcon("resources/icons/icon/math_card.png")), function=self.showMathContent)

        self.addCards(QIcon("resources/icons/icon/chem_card.png"),function=self.showMathContent)

        self.addCards(QIcon("resources/icons/icon/phy_card.png"), function=self.showMathContent)

        if field == "Engineering":
            self.neet_button.hide()
        elif field == "Medical":
            self.keam_button.hide()
            self.jee_button.hide()

        # Add additional spacer at the bottom for smooth scrolling
        self.scroll_layout.addSpacerItem(QSpacerItem(20, 50, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Subject buttons click actions
        #self.jee_button.clicked.connect(self.showMathContent)
        #self.neet_button.clicked.connect(self.showChemistryContent)
        #self.keam_button.clicked.connect(self.showPhysicsContent)

    def showMathContent(self):
        """ Switch to the Math subject content. """
        self.hide()  # Hide the main dashboard
        self.math_content_window = SubjectContentWindow("Math", self)  # Pass self as parent
        self.math_content_window.show()

    def showChemistryContent(self):
        """ Switch to the Chemistry subject content. """
        self.hide()  # Hide the main dashboard
        self.chem_content_window = SubjectContentWindow("Chemistry", self)  # Pass self as parent
        self.chem_content_window.show()

    def showPhysicsContent(self):
        """ Switch to the Physics subject content. """
        self.hide()  # Hide the main dashboard
        self.phy_content_window = SubjectContentWindow("Physics", self)  # Pass self as parent
        self.phy_content_window.show()

    def addCards(self, icon, function):
        button = QPushButton()
        button.clicked.connect(function)  # Set the function to be called when the button is clicked
        button.setFixedSize(QSize(346, 232))
        button.setIcon(QIcon(icon))
        button.setIconSize(QSize(345, 245))
        button.setStyleSheet("""
                        QPushButton {
                            background: none;
                            border-radius: 10px;
                            padding: 10px;
                            border: none;

                        }
                        QPushButton:hover {
                            border: 2px solid #007BFF; /* Blue border on hover */
                        }
                    """)
        self.shortnotes_layout.addWidget(button)

    def create_button(self, text, icon_path):
        """ Helper method to create a styled QPushButton """
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
                    border: 2px solid transparent; /* Default border */
                }
                QPushButton:hover {
                    border: 2px solid #007BFF; /* Blue border on hover */
                }
            """)
        return button

























































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

        # Add content for subject (math/chemistry/physics)
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
                border: 2px solid #007BFF;
            }
        """)
        self.back_button.clicked.connect(self.closeSubjectWindow)
        self.layout.addWidget(self.back_button)

    def closeSubjectWindow(self):
        self.close()
        self.parent_widget.show()


class DashboardWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)
        self.spacer_item = QSpacerItem(30, 40)
        self.spacer_item_small = QSpacerItem(10, 10)

        # Set gradient background
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#202020"))
        gradient.setColorAt(1.0, QColor("#202020"))
        palette.setBrush(QPalette.ColorRole.Window, QBrush(gradient))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(25, 25, 25, 25)

        # Greeting Bar
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

        # Scrollable Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("border: none; background: transparent;")
        self.scroll_area.setWidgetResizable(True)

        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)
        self.main_layout.addWidget(self.scroll_area)

        self.scroll_layout.addSpacerItem(QSpacerItem(20, 50))

        # Chapter-wise PYQ Bank Heading
        pyq_header = CaptionLabel("Chapter wise PYQ Bank")
        pyq_header.setFont(QFont("Poppins", 15, QFont.Weight.Bold))
        pyq_header.setStyleSheet("color: #ffffff;")
        self.scroll_layout.addWidget(pyq_header)
        self.scroll_layout.addSpacerItem(self.spacer_item_small)

        # Exam Buttons
        self.button_layout = QHBoxLayout()
        self.jee_button = self.create_button("JEE", "resources/icons/icon/JEE.png")
        self.neet_button = self.create_button("NEET", "resources/icons/icon/NEET.png")
        self.keam_button = self.create_button("KEAM", "resources/icons/icon/KEAM.png")

        self.button_layout.addWidget(self.jee_button)
        self.button_layout.addWidget(self.neet_button)
        self.button_layout.addWidget(self.keam_button)
        self.button_layout.addStretch(1)
        self.scroll_layout.addLayout(self.button_layout)
        self.scroll_layout.addSpacerItem(self.spacer_item)

        # Short Notes Heading
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

    def showMathContent(self):
        self.hide()
        self.math_content_window = SubjectContentWindow("Math", self)
        self.math_content_window.show()

    def showChemistryContent(self):
        self.hide()
        self.chem_content_window = SubjectContentWindow("Chemistry", self)
        self.chem_content_window.show()

    def showPhysicsContent(self):
        self.hide()
        self.phy_content_window = SubjectContentWindow("Physics", self)
        self.phy_content_window.show()

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
