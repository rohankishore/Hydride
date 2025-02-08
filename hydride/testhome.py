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

        # KEAM Content Label
        keam_label = QLabel("Welcome to KEAM Content!", self)
        keam_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        keam_label.setFont(QFont("Poppins", 18, QFont.Weight.Bold))
        keam_label.setStyleSheet("color: white;")
        self.layout.addWidget(keam_label)

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


class DashboardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setMinimumSize(800, 600)
        self.spacer_item = QSpacerItem(30, 40)
        self.spacer_item_small = QSpacerItem(10, 10)
        self.parent_stack = parent

        # Set gradient background
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#272727"))
        gradient.setColorAt(1.0, QColor("#272727"))
        gradient.setColorAt(2.0, QColor("#202027"))
        gradient.setColorAt(3.0, QColor("#202020"))

        palette.setBrush(QPalette.ColorRole.Window, QBrush(gradient))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(25, 25, 25, 25)

        # ======== Greeting Bar (Fixed) ========
        self.greeting_bar = QWidget()
        self.greeting_bar.setStyleSheet("background-color: #272727;")
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
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
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
        self.pyq_header = CaptionLabel("Chapter wise PYQ Bank")
        self.pyq_header.setFont(QFont("Poppins", 15, QFont.Weight.Bold))
        self.pyq_header.setStyleSheet("color: #ffffff;")
        self.scroll_layout.addWidget(self.pyq_header)
        self.scroll_layout.addSpacerItem(self.spacer_item_small)

        # Exam Buttons Layout
        self.button_layout = QHBoxLayout()

        self.jee_button = self.create_button("JEE", "resources/icons/icon/JEE.png")
        self.neet_button = self.create_button("NEET", "resources/icons/icon/NEET.png")
        self.keam_button = self.create_button("KEAM", "resources/icons/icon/KEAM.png")
        self.keam_button.clicked.connect(lambda: self.parent_stack.switch_to_widget(self.parent_stack.page2))
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

        self.addCards(QIcon("resources/icons/icon/chem_card.png"), function=self.showMathContent)

        self.addCards(QIcon("resources/icons/icon/phy_card.png"), function=self.showMathContent)

        if field == "Engineering":
            self.neet_button.hide()
        elif field == "Medical":
            self.keam_button.hide()
            self.jee_button.hide()

        # Add additional spacer at the bottom for smooth scrolling
        self.scroll_layout.addSpacerItem(QSpacerItem(20, 50, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Subject buttons click actions
        # self.jee_button.clicked.connect(self.showMathContent)
        # self.neet_button.clicked.connect(self.showChemistryContent)
        # self.keam_button.clicked.connect(self.showPhysicsContent)

    def clearLayout(self, layout):
        """ Removes all widgets from the given layout. """
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)  # Detach the widget from the layout
                widget.deleteLater()  # Schedule it for deletion
            elif item.layout() is not None:
                self.clearLayout(item.layout())  # Recursively clear nested layouts

    def showMathContent(self):
        """ Replace the main content with Math subject content in the same layout. """

        # Clear existing content inside the scroll layout
        self.clearLayout(self.scroll_layout)

        # Create new Math content
        math_label = QLabel("Welcome to Math Content!", self)
        math_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        math_label.setFont(QFont("Poppins", 18, QFont.Weight.Bold))
        math_label.setStyleSheet("color: white;")
        self.scroll_layout.addWidget(math_label)

        # Add a Back button
        back_button = QPushButton("Back to Home")
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
        back_button.clicked.connect(self.restoreDashboard)
        self.scroll_layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # self.math_content_window.show()

    def showKeamContent(self):
        """ Replaces the current widgets with a KEAM content label and a back button """
        # Clear existing widgets in the scroll layout
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Add KEAM Content Label
        keam_label = QLabel("Welcome to KEAM Content!", self)
        keam_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        keam_label.setFont(QFont("Poppins", 18, QFont.Weight.Bold))
        keam_label.setStyleSheet("color: white;")
        self.scroll_layout.addWidget(keam_label)

        # Add Back Button
        back_button = QPushButton("Back to Home")
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
                border: 2px solid #007BFF; /* Blue border on hover */
            }
        """)
        back_button.clicked.connect(self.restoreDashboard)
        self.scroll_layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignCenter)

    def restoreDashboard(self):
        print("cl")
        self.clearLayout(self.scroll_layout)
        print("cleared")

        # Re-add original content
        self.setupDashboardContent()

    def setupDashboardContent(self):
        # Debug: Check if layouts and widgets exist before adding
        if not hasattr(self, "scroll_layout") or self.scroll_layout is None:
            print("Error: scroll_layout does not exist!")
            print(f"pyq_header: {self.pyq_header}")
            return  # Prevent crashes

        if hasattr(self, "pyq_header") and self.pyq_header is not None:
            print("Adding pyq_header...")
            self.scroll_layout.addWidget(self.pyq_header)
        else:
            print("Error: pyq_header does not exist!")

        if hasattr(self, "button_layout") and self.button_layout is not None:
            print("Adding button_layout...")
            self.scroll_layout.addLayout(self.button_layout)
        else:
            print("Error: button_layout does not exist!")

        # Add back buttons for exams
        for btn_name, btn in [("JEE", self.jee_button), ("NEET", self.neet_button), ("KEAM", self.keam_button)]:
            if hasattr(self, btn_name.lower() + "_button") and btn is not None:
                print(f"Adding {btn_name} button...")
                self.button_layout.addWidget(btn)
            else:
                print(f"Error: {btn_name} button does not exist!")

        # Re-add all static cards with a check
        for icon_path, function in [
            ("resources/icons/icon/math_card.png", self.showMathContent),
            ("resources/icons/icon/chem_card.png", self.showMathContent),
            ("resources/icons/icon/phy_card.png", self.showMathContent)
        ]:
            if os.path.exists(icon_path):
                print(f"Adding card with icon: {icon_path}")
                self.addCards(QIcon(icon_path), function=function)
            else:
                print(f"Error: Icon file not found at {icon_path}")

    def showChemistryContent(self):
        """ Switch to the Chemistry subject content. """
        self.hide()  # Hide the main dashboard
        self.chem_content_window = SubjectContentWindow("Chemistry", self)  # Pass self as parent
        self.chem_content_window.show()

    def showPhysicsContent(self):
        """ Switch to the Physics subject content. """
        self.hide()  # Hide the main dashboard
        self.phy_content_window = SubjectContentWindow("Physics", self)
        # Pass self as parent
        self.phy_content_window.show()

    def addCards(self, icon, function):
        button = QPushButton()
        button.clicked.connect(function)  # Set the function to be called when the button is clicked
        button.setFixedSize(QSize(380, 227))
        button.setIcon(QIcon(icon))
        button.setIconSize(QSize(379, 226))
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


class StackableWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.stacked_widget = QStackedWidget()
        self.history = []  # Stack to track previous widgets

        self.setObjectName("testhome")

        # Create pages
        self.page1 = QWidget()
        self.page2 = QWidget()

        # Page 1 layout
        layout1 = QVBoxLayout()
        self.home = DashboardWidget(self)
        layout1.addWidget(self.home)
        self.page1.setLayout(layout1)

        # Page 2 layout
        layout2 = QVBoxLayout()
        layout2.addWidget(QLabel("This is Page 2"))
        self.keam_widget = KeamContentWidget(self.go_back)
        btn_to_page1 = QPushButton("Go to Page 1")
        btn_to_page1.clicked.connect(self.go_back)
        layout2.addWidget(self.keam_widget)
        layout2.addWidget(btn_to_page1)
        self.page2.setLayout(layout2)

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)

        self.layout.addWidget(self.stacked_widget)
        self.setLayout(self.layout)

    def showKeamContent(self):
        self.stacked_widget.setCurrentWidget(self.keam_widget)

    def switch_to_widget(self, widget):
        """Switches to the given widget and stores the previous one."""
        current_widget = self.stacked_widget.currentWidget()
        if current_widget:
            self.history.append(current_widget)
        if self.stacked_widget.indexOf(widget) == -1:
            self.stacked_widget.addWidget(widget)  # Add if not already in stack
        self.stacked_widget.setCurrentWidget(widget)

    def go_back(self):
        """Goes back to the last visited widget if possible."""
        if self.history:
            last_widget = self.history.pop()
            self.stacked_widget.setCurrentWidget(last_widget)
