import json
import os

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QLinearGradient, QColor, QPalette, QBrush, QIcon
from PyQt6.QtWidgets import (
    QHBoxLayout, QWidget, QPushButton, QSpacerItem, QSizePolicy,
    QScrollArea
)
from PyQt6.QtWidgets import (
    QStackedWidget, QListWidget
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


import json


class QuestionListWidget(QWidget):
    def __init__(self, stack_widget):
        super().__init__()
        self.stack_widget = stack_widget

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(40, 20, 40, 20)

        self.title_label = QLabel("")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(QFont("Poppins", 24, QFont.Weight.Bold))
        self.title_label.setStyleSheet("color: #ffffff; padding: 10px;")
        layout.addWidget(self.title_label)

        back_button = QPushButton("⬅️ Back to Chapters", self)
        back_button.setFixedSize(QSize(200, 50))
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
        back_button.clicked.connect(lambda: self.stack_widget.setCurrentIndex(2))
        layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignCenter)


        self.list_widget = QListWidget()
        self.list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.list_widget.setStyleSheet("""
            QListWidget {
                background-color: #222d3f;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QListWidget::item {
                padding: 10px;
            }
            QListWidget::item:hover {
                background-color: #007BFF;
            }
        """)
        self.list_widget.itemClicked.connect(self.open_quiz)
        layout.addWidget(self.list_widget)

        self.setLayout(layout)

    def load_questions(self, chapter_name):
        """Loads questions from the JSON file and updates QuizWidget."""
        filename = f"resources/chapters/keam/{chapter_name.replace(' ', '_')}.json"
        print(f"Loading questions from: {filename}")

        try:
            with open(filename, "r") as file:
                data = json.load(file)

                if not isinstance(data, list):
                    raise ValueError("Invalid JSON format: Expected a list")

                valid_questions = [entry["question"] for entry in data if "question" in entry]

                print(f"✅ Loaded {len(valid_questions)} valid questions.")

                # 🔥 Ensure we are setting questions in the correct QuizWidget index
                quiz_widget_index = 6  # Change this if needed
                quiz_widget = self.stack_widget.widget(quiz_widget_index)
                quiz_widget.questions = valid_questions  # Store the questions

                print(f"✅ Stored {len(quiz_widget.questions)} questions in QuizWidget (index {quiz_widget_index})")

                # Populate list widget
                self.list_widget.clear()
                for i, question in enumerate(valid_questions, 1):
                    self.list_widget.addItem(f"{i}. {question['content']}")

        except Exception as e:
            print("❌ Error loading questions:", e)
            self.list_widget.clear()
            self.list_widget.addItem("No questions available.")

    def open_quiz(self, item):
        """Opens the quiz window with the selected question."""
        try:
            question_index = self.list_widget.row(item)
            print(f"Clicked question index: {question_index}")

            # Debugging: Print available questions
            print(f"Available questions in QuizWidget: {len(self.stack_widget.widget(6).questions)}")

            # Ensure questions are loaded before switching
            if 0 <= question_index < len(self.stack_widget.widget(6).questions):
                self.stack_widget.setCurrentIndex(6)  # Switch to QuizWidget
                self.stack_widget.widget(6).load_question(question_index)
            else:
                print("Error: Index out of range!")

        except Exception as e:
            print("Error opening quiz:", e)


from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QListWidgetItem
import requests

class QuizWidget(QWidget):
    def __init__(self, stack_widget):
        super().__init__()
        self.stack_widget = stack_widget
        self.current_question_index = 0
        self.questions = []
        self.selected_option = None

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(40, 20, 40, 20)

        # Question Label
        self.question_label = QLabel()
        self.question_label.setWordWrap(True)
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question_label.setFont(QFont("Poppins", 14, QFont.Weight.Bold))
        self.question_label.setStyleSheet("color: white; background: #222d3f; padding: 15px; border-radius: 10px;")
        self.question_label.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(self.question_label)

        # ✅ **Fix: Define `self.question_image`**
        self.question_image = QLabel()
        self.question_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question_image.hide()  # Hide initially
        layout.addWidget(self.question_image)

        # Explanation Label (Hidden Initially)
        self.explanation_label = QLabel()
        self.explanation_label.setWordWrap(True)
        self.explanation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.explanation_label.setFont(QFont("Poppins", 12, QFont.Weight.Medium))
        self.explanation_label.setStyleSheet("color: white; padding: 5px;")
        self.explanation_label.hide()
        layout.addWidget(self.explanation_label)

        # Explanation Image (Hidden Initially)
        self.explanation_image = QLabel()
        self.explanation_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.explanation_image.hide()
        layout.addWidget(self.explanation_image)

        # Options List
        self.option_list = QListWidget()
        self.option_list.setStyleSheet("""
            QListWidget {
                background-color: #222d3f;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QListWidget::item {
                padding: 10px;
            }
            QListWidget::item:hover {
                background-color: #007BFF;
            }
        """)
        self.option_list.itemClicked.connect(self.store_selected_option)
        layout.addWidget(self.option_list)

        # Navigation Buttons
        nav_layout = QHBoxLayout()
        self.prev_button = QPushButton("⬅️ Previous")
        self.next_button = QPushButton("Next ➡️")

        self.prev_button.clicked.connect(self.previous_question)
        self.next_button.clicked.connect(self.check_answer_and_next)

        nav_layout.addWidget(self.prev_button)
        nav_layout.addWidget(self.next_button)
        layout.addLayout(nav_layout)

        self.setLayout(layout)

    def store_selected_option(self, item):
        """Stores the selected option."""
        self.selected_option = item.text().split(".")[0]  # Extract the option identifier (A, B, C, etc.)
        print(f"Selected answer: {self.selected_option}")  # Debugging

    def check_answer_and_next(self):
        """First click shows answer feedback, second click shows explanation (if any), third click moves to the next question."""
        if not self.questions:
            return

        question_data = self.questions[self.current_question_index]
        correct_answers = question_data["correct_options"]

        # Step 1: Show answer feedback
        if self.explanation_label.isHidden():  # Means feedback not shown yet
            if self.selected_option:  # Only show feedback if an option was chosen
                if self.selected_option in correct_answers:
                    self.explanation_label.setText("✅ Correct!")
                    self.explanation_label.setStyleSheet("color: #00FF00; padding: 5px;")
                else:
                    correct_text = ", ".join(correct_answers) if correct_answers else "None"
                    self.explanation_label.setText(f"❌ Incorrect! Correct answer: {correct_text}")
                    self.explanation_label.setStyleSheet("color: #FF4444; padding: 5px;")
            self.explanation_label.show()
            return  # Stops execution here

        # Step 2: Show explanation (if available)
        if self.explanation_label.text() != "" and question_data.get("explanation"):
            explanation_data = question_data["explanation"]
            if isinstance(explanation_data, dict):
                explanation_text = explanation_data.get("content", "")
                explanation_image = explanation_data.get("image", "")

                if explanation_text:
                    self.explanation_label.setText(f"📌 Explanation: {explanation_text}")

                if explanation_image:
                    self.load_image(self.explanation_image, explanation_image)
            return  # Stops execution to show explanation before moving to next question

        # Step 3: Move to next question
        self.explanation_label.setText("")
        self.explanation_label.hide()
        self.explanation_image.hide()
        if self.current_question_index < len(self.questions) - 1:
            self.next_question()

    def previous_question(self):
        """Moves to the previous question."""
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.load_question(self.current_question_index)

    def next_question(self):
        """Moves to the next question."""
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
            self.load_question(self.current_question_index)

    def load_question(self, index):
        """Loads a question and displays an image if available."""
        if not self.questions:
            self.question_label.hide()
            self.question_label.setText("No questions available.")
            return

        self.current_question_index = index
        question_data = self.questions[self.current_question_index]

        # Handle question text (Hide if empty)
        if "content" in question_data and question_data["content"].strip():
            formatted_question = question_data["content"].replace("$", "<sup>").replace("$", "</sup>")
            self.question_label.setText(formatted_question)
            self.question_label.show()
        else:
            self.question_label.hide()

        # Handle question image (Larger Size)
        if "image" in question_data and question_data["image"].strip():
            self.load_image(self.question_image, question_data["image"])
        else:
            self.question_image.hide()

        # Load options
        self.option_list.clear()
        self.selected_option = None  # Reset selection

        for option in question_data["options"]:
            item = QListWidgetItem(f"{option['identifier']}. {option['content']}")
            self.option_list.addItem(item)

            # Handle option image
            if "image" in option and option["image"].strip():
                image_label = QLabel()
                self.load_image(image_label, option["image"])
                self.option_list.setItemWidget(item, image_label)

    def load_image(self, label, url, wsize=500, hsize=600):
        """Loads and displays an image from a URL (e.g., GitHub raw file)."""
        try:
            print(f"🔍 Loading image from: {url}")  # Debug print

            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses

            pixmap = QPixmap()
            if pixmap.loadFromData(response.content):
                label.setPixmap(pixmap.scaled(wsize, hsize, Qt.AspectRatioMode.KeepAspectRatio))
                label.show()
                print("✅ Image loaded successfully!")
            else:
                print("❌ Failed to load image into QPixmap")
                label.hide()

        except Exception as e:
            print(f"❌ Error loading image from {url}: {e}")
            label.hide()


class PhysicsWidget(QWidget):
    def __init__(self, stack_widget):
        super().__init__()
        self.stack_widget = stack_widget

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(40, 20, 40, 20)

        title_label = QLabel("📘 Physics Chapters")
        caption_label = QLabel("28 Chapters | 14 11th | 14 12th")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        caption_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Poppins", 24, QFont.Weight.Bold))
        caption_label.setFont(QFont("Poppins", 14, QFont.Weight.DemiBold))
        title_label.setStyleSheet("color: #ffffff; padding: 10px;")
        caption_label.setStyleSheet("color: #ffffff; padding: 10px;")
        layout.addWidget(title_label)
        layout.addWidget(caption_label)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none; background: transparent;")
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(10)

        chapters = [
            "Units and Measurements", "Motion in a Straight Line", "Motion in a Plane",
            "Laws of Motion", "Work, Energy, and Power", "System of Particles and Rotational Motion",
            "Gravitation", "Mechanical Properties of Solids", "Mechanical Properties of Fluids",
            "Thermal Properties of Matter", "Thermodynamics", "Kinetic Theory",
            "Oscillations", "Waves"
        ]

        for chapter in chapters:
            chapter_button = QPushButton(chapter)
            chapter_button.setFixedHeight(60)
            chapter_button.setFont(QFont("Poppins", 14, QFont.Weight.Medium))
            chapter_button.setStyleSheet("""
                QPushButton {
                    background-color: #222d3f;
                    color: white;
                    border-radius: 15px;
                    padding: 10px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #007BFF;
                    color: white;
                }
            """)
            chapter_button.clicked.connect(lambda _, ch=chapter: self.open_question_list(ch))
            scroll_layout.addWidget(chapter_button)

        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)

        back_button = QPushButton("⬅️ Back to KEAM", self)
        back_button.setFixedSize(QSize(200, 50))
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
        back_button.clicked.connect(lambda: self.stack_widget.setCurrentIndex(1))
        layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def open_question_list(self, chapter_name):
        """Opens the question list for the selected chapter."""
        self.stack_widget.setCurrentIndex(5)  # Assume 5 is the index for QuestionListWidget
        self.stack_widget.widget(5).load_questions(chapter_name)


class MathsWidget(QWidget):
    def __init__(self, stack_widget):
        super().__init__()
        self.stack_widget = stack_widget  # Store stack reference

        # Main layout
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(40, 20, 40, 20)

        # Title and Caption Labels
        title_label = QLabel("📐 Maths Chapters")
        caption_label = QLabel("29 Chapters | 14 11th | 15 12th")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        caption_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Poppins", 24, QFont.Weight.Bold))
        caption_label.setFont(QFont("Poppins", 14, QFont.Weight.DemiBold))
        title_label.setStyleSheet("color: #ffffff; padding: 10px;")
        caption_label.setStyleSheet("color: #ffffff; padding: 10px;")
        layout.addWidget(title_label)
        layout.addWidget(caption_label)

        # Scrollable List
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none; background: transparent;")
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(10)

        # Maths Chapters (Class 11 & 12)
        chapters = [
            # Class 11
            "➕ Sets", "➗ Relations and Functions", "📉 Trigonometric Functions",
            "🛤️ Principle of Mathematical Induction", "♾️ Complex Numbers and Quadratic Equations",
            "📈 Linear Inequalities", "➗ Permutations and Combinations", "📊 Binomial Theorem",
            "📐 Sequences and Series", "➕ Straight Lines", "📏 Conic Sections",
            "🌀 Introduction to Three-dimensional Geometry",
            "📊 Limits and Derivatives", "📊 Mathematical Reasoning", "📐 Statistics", "🎲 Probability",

            # Class 12
            "🔗 Relations and Functions", "📈 Inverse Trigonometric Functions", "🔀 Matrices",
            "➕ Determinants", "📏 Continuity and Differentiability", "📉 Applications of Derivatives",
            "📊 Integrals", "📈 Applications of Integrals", "📊 Differential Equations", "📏 Vectors",
            "📐 Three-dimensional Geometry", "🔢 Linear Programming", "🎲 Probability"
        ]

        # Add chapter buttons
        for chapter in chapters:
            chapter_button = QPushButton(chapter)
            chapter_button.setFixedHeight(60)
            chapter_button.setFont(QFont("Poppins", 14, QFont.Weight.Medium))
            chapter_button.setStyleSheet("""
                QPushButton {
                    background-color: #222d3f;
                    color: white;
                    border-radius: 15px;
                    padding: 10px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #007BFF;
                    color: white;
                }
            """)
            scroll_layout.addWidget(chapter_button)

        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)

        # Back Button
        back_button = QPushButton("⬅️ Back to KEAM", self)
        back_button.setFixedSize(QSize(200, 50))
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
        back_button.clicked.connect(lambda: self.stack_widget.setCurrentIndex(1))  # Back to KEAM Widget
        layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)


class ChemistryWidget(QWidget):
    def __init__(self, stack_widget):
        super().__init__()
        self.stack_widget = stack_widget  # Store stack reference

        # Main layout
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(40, 20, 40, 20)

        # Title and Caption Labels
        title_label = QLabel("🧪 Chemistry Chapters")
        caption_label = QLabel("19 Chapters | 9 11th | 10 12th")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        caption_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Poppins", 24, QFont.Weight.Bold))
        caption_label.setFont(QFont("Poppins", 14, QFont.Weight.DemiBold))
        title_label.setStyleSheet("color: #ffffff; padding: 10px;")
        caption_label.setStyleSheet("color: #ffffff; padding: 10px;")
        layout.addWidget(title_label)
        layout.addWidget(caption_label)

        # Scrollable List
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none; background: transparent;")
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(10)

        # Chemistry Chapters (Class 11 & 12, avoiding deleted ones)
        chapters = [
            # Class 11
            "🧪 Some Basic Concepts of Chemistry", "⚖️ Structure of Atom",
            "🔗 Classification of Elements and Periodicity",
            "⚛️ Chemical Bonding and Molecular Structure", "🌡️ States of Matter", "🧪 Thermodynamics",
            "🔁 Equilibrium", "⚡ Redox Reactions", "🧫 Hydrogen",
            "🧱 The s-Block Elements (Alkali and Alkaline Earth Metals)",
            "🔬 Some p-Block Elements", "🛠️ Organic Chemistry – Some Basic Principles and Techniques",
            "🧪 Hydrocarbons", "🔄 Environmental Chemistry",

            # Class 12
            "💎 Solid State", "💧 Solutions", "⚡ Electrochemistry", "🔥 Chemical Kinetics", "♨️ Surface Chemistry",
            "🧬 General Principles and Processes of Isolation of Elements", "🔬 The p-Block Elements",
            "🧲 The d- and f-Block Elements", "🧪 Coordination Compounds", "🧑‍🔬 Haloalkanes and Haloarenes",
            "🧪 Alcohols, Phenols and Ethers", "🧬 Aldehydes, Ketones and Carboxylic Acids",
            "🧫 Organic Compounds Containing Nitrogen", "🩺 Biomolecules, Polymers and Chemistry in Everyday Life"
        ]

        # Add chapter buttons
        for chapter in chapters:
            chapter_button = QPushButton(chapter)
            chapter_button.setFixedHeight(60)
            chapter_button.setFont(QFont("Poppins", 14, QFont.Weight.Medium))
            chapter_button.setStyleSheet("""
                QPushButton {
                    background-color: #222d3f;
                    color: white;
                    border-radius: 15px;
                    padding: 10px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #007BFF;
                    color: white;
                }
            """)
            scroll_layout.addWidget(chapter_button)

        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)

        # Back Button
        back_button = QPushButton("⬅️ Back to KEAM", self)
        back_button.setFixedSize(QSize(200, 50))
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
        back_button.clicked.connect(lambda: self.stack_widget.setCurrentIndex(1))  # Back to KEAM Widget
        layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)


class KeamContentWidget(QWidget):
    def __init__(self, stack_widget, go_back_callback):
        """
        A widget displaying KEAM content with subject buttons to switch pages.

        :param stack_widget: The QStackedWidget instance to switch pages.
        :param go_back_callback: Function to call when the back button is clicked.
        """
        super().__init__()

        self.stack_widget = stack_widget  # Store the QStackedWidget reference

        # Layout setup
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setSpacing(80)

        self.greeting_bar = QWidget()
        self.greeting_bar.setStyleSheet("background-color: #1a1a1a;")
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

        self.layout.addWidget(self.greeting_bar)

        # Subject Buttons
        self.physics_button = self.create_card_button(QIcon("resources/icons/icon/phy_sub_button.png"),
                                                      self.show_physics_page)
        self.chemistry_button = self.create_card_button(QIcon("resources/icons/icon/chem_sub_button.png"),
                                                        self.show_chemistry_page)
        self.maths_button = self.create_card_button(QIcon("resources/icons/icon/math_sub_button.png"), self.show_maths_page)

        self.layout.addWidget(self.physics_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.chemistry_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.maths_button, alignment=Qt.AlignmentFlag.AlignCenter)

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
        button.clicked.connect(function)  # Connect button click to function
        button.setFixedSize(QSize(805, 188))
        button.setIcon(QIcon(icon))
        button.setIconSize(QSize(1000, 180))
        button.setStyleSheet("""
            QPushButton {
                background: none;
                border-radius: 45px;
                padding: 10px;
                border: none;
            }
            QPushButton:hover {
                border: 2px solid #007BFF; /* Blue border on hover */
            }
        """)
        return button

    def show_physics_page(self):
        """Switch to the Physics page in QStackedWidget."""
        self.stack_widget.setCurrentIndex(2)  # Change this index based on actual positioning

    def show_chemistry_page(self):
        """Switch to the Chemistry page in QStackedWidget."""
        self.stack_widget.setCurrentIndex(3)  # Change this index based on actual positioning

    def show_maths_page(self):
        """Switch to the Maths page in QStackedWidget."""
        self.stack_widget.setCurrentIndex(4)  # Change this index based on actual positioning


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
        gradient.setColorAt(0.0, QColor("#191919"))
        gradient.setColorAt(1.0, QColor("#1d1d1d"))
        # gradient.setColorAt(2.0, QColor("#2D3436"))
        # gradient.setColorAt(3.0, QColor("#202020"))

        palette.setBrush(QPalette.ColorRole.Window, QBrush(gradient))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(25, 25, 25, 25)

        # ======== Greeting Bar (Fixed) ========
        self.greeting_bar = QWidget()
        self.greeting_bar.setStyleSheet("background-color: #1a1a1a;")
        self.greeting_bar.setFixedHeight(120)
        self.greeting_bar_layout = QVBoxLayout(self.greeting_bar)
        self.greeting_bar_layout.setContentsMargins(0, 0, 0, 0)

        self.title_label = LargeTitleLabel(f"👋 Hey, {name}")
        self.title_label.setFont(QFont("Poppins", 35, QFont.Weight.DemiBold))
        self.title_label.setStyleSheet("color: #ffffff; background-color: #1a1a1a;")

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
        self.home_widget = QWidget()
        self.page2 = QWidget()
        self.keam_phy = QWidget()
        self.keam_chem = QWidget()
        self.keam_math = QWidget()

        # Page 1 layout
        layout1 = QVBoxLayout()
        self.home = DashboardWidget(self)
        layout1.addWidget(self.home)
        self.home_widget.setLayout(layout1)

        # Page 2 layout
        layout2 = QVBoxLayout()
        layout2.addStretch(1)
        self.keam_widget = KeamContentWidget(self.stacked_widget, self.go_back)
        layout2.addWidget(self.keam_widget, Qt.AlignmentFlag.AlignTop)
        self.page2.setLayout(layout2)

        layout3 = QVBoxLayout()
        layout3.addStretch(1)
        self.keam_phy_widget = PhysicsWidget(self.stacked_widget)
        layout3.addWidget(self.keam_phy_widget, Qt.AlignmentFlag.AlignTop)
        self.keam_phy.setLayout(layout3)

        layout4 = QVBoxLayout()
        layout4.addStretch(1)
        self.keam_chem_widget = ChemistryWidget(self.stacked_widget)
        layout4.addWidget(self.keam_chem_widget, Qt.AlignmentFlag.AlignTop)
        self.keam_phy.setLayout(layout4)

        layout5 = QVBoxLayout()
        layout5.addStretch(1)
        self.keam_math_widget = MathsWidget(self.stacked_widget)
        layout5.addWidget(self.keam_math_widget, Qt.AlignmentFlag.AlignTop)
        self.keam_phy.setLayout(layout5)

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.home_widget)
        self.stacked_widget.addWidget(self.page2)
        self.stacked_widget.addWidget(self.keam_phy_widget)
        self.stacked_widget.addWidget(self.keam_chem_widget)
        self.stacked_widget.addWidget(self.keam_math_widget)
        self.stacked_widget.addWidget(QuestionListWidget(self.stacked_widget))
        self.stacked_widget.addWidget(QuizWidget(self.stacked_widget))

        for i in range(self.stacked_widget.count()):
            print(f"Index {i}: {self.stacked_widget.widget(i).__class__.__name__}")

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
