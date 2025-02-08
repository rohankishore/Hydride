import json
import os

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QColor, QPalette, QBrush, QIcon, QLinearGradient
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QHBoxLayout,
    QSpacerItem, QSizePolicy, QStackedWidget
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QLinearGradient, QColor, QPalette, QBrush, QIcon
from PyQt6.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QSpacerItem, QSizePolicy,
    QScrollArea, QLabel
)
from qfluentwidgets import LargeTitleLabel, CaptionLabel


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


class KeamContentWidget(QWidget):
    def __init__(self, go_back_callback):
        """
        A widget displaying KEAM content with a back button.

        :param go_back_callback: Function to call when the back button is clicked.
        """
        super().__init__()

        # Layout setup
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setSpacing(80)
        #self.layout.addStretch()# Space between elements

        self.greeting_bar = QWidget()
        self.greeting_bar.setStyleSheet("background-color: #272727;")
        self.greeting_bar.setFixedHeight(140)
        self.greeting_bar_layout = QVBoxLayout(self.greeting_bar)
        self.greeting_bar_layout.addStretch()
        self.greeting_bar_layout.addSpacing(5)
        self.greeting_bar_layout.setContentsMargins(0, 0, 0, 0)

        self.title_label = LargeTitleLabel("Kerala Engineering, Architecture, and Medical (KEAM)")
        self.title_label.setFont(QFont("Helvetica", 33, QFont.Weight.DemiBold))
        self.title_label.setStyleSheet("color: #ffffff;")

        self.field_caption = CaptionLabel("2019-2024  |  19 Papers")
        self.field_caption.setFont(QFont("Poppins", 12, QFont.Weight.Bold))

        self.greeting_bar_layout.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.greeting_bar_layout.addWidget(self.field_caption, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.layout.addWidget(self.greeting_bar)  # Keep it fixed at the top

        # Subject Buttons (Physics, Chemistry, Mathematics)
        self.physics_button = self.create_card_button(icon=(QIcon("resources/icons/icon/phy_button.png")), function=None)
        self.chemistry_button = self.create_card_button(icon=(QIcon("resources/icons/icon/chem_button.png")), function=None)
        self.maths_button = self.create_card_button(icon=(QIcon("resources/icons/icon/math_button.png")), function=None)

        self.layout.addWidget(self.physics_button)
        self.layout.addWidget(self.chemistry_button, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.maths_button, Qt.AlignmentFlag.AlignCenter)

        # Back Button
        back_button = QPushButton("Back to Home", self)
        back_button.setFixedSize(QSize(150, 50))
        back_button.setFont(QFont("Poppins", 12, QFont.Weight.Bold))
        back_button.setStyleSheet("""
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
        back_button.clicked.connect(go_back_callback)
        self.layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignBottom)

    def create_card_button(self, icon, function):
        """Creates a rounded rectangular card-like button for subjects."""
        button = QPushButton()
#        button.clicked.connect(function)  # Set the function to be called when the button is clicked
        button.setFixedSize(QSize(1000, 180))
        button.setIcon(QIcon(icon))
        button.setIconSize(QSize(1000, 180))
        button.setStyleSheet("""
                        QPushButton {
                            background: none;
                            border-radius: 39px;
                            padding: 10px;
                            border: none;

                        }
                        QPushButton:hover {
                            border: 2px solid #007BFF; /* Blue border on hover */
                        }
                    """)
        return button