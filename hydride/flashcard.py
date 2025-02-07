import json
import os

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QDialog, QLabel,
    QLineEdit, QTextEdit, QHBoxLayout, QGridLayout, QScrollArea
)


class FlashcardWidget(QWidget):
    SAVE_PATH = "resources/data/flashcards/flashcards.json"

    def __init__(self):
        super().__init__()
        self.flashcards = []  # Store flashcards as (question, answer)
        self.layout = QVBoxLayout(self)

        self.GRID_ROWS = 1000000
        self.GRID_COLS = 5

        # Flashcards container (Grid Layout)
        self.flashcards_layout = QGridLayout()
        self.flashcards_layout.setSpacing(10)  # Space between flashcards

        self.setObjectName("flashcards")

        # Wrap the grid layout inside a scroll area
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #222; /* Darker shade */
                border: none;
            }
            QScrollBar:vertical {
                background: #333;
                width: 10px;
            }
            QScrollBar::handle:vertical {
                background: #555;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #777;
            }
        """)

        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #333;
            }
        """)
        self.scroll_area.setWidgetResizable(True)  # Allow the area to resize dynamically
        self.scroll_area.setWidget(self.create_flashcards_container())

        self.layout.addWidget(self.scroll_area)

        # Add Flashcard Button (Bottom-Right)
        self.add_button = QPushButton("⚡ Add Flashcard")
        self.add_button.setFixedSize(QSize(180, 50))
        self.add_button.setFont(QFont("Poppins", 12, QFont.Weight.Bold))
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)

        # Align button to bottom-right
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.add_button)
        self.layout.addLayout(btn_layout)

        self.add_button.clicked.connect(self.open_add_dialog)

        self.load_flashcards()

    def create_flashcards_container(self):
        """ Creates a QWidget to hold the flashcards and add it to the scroll area """
        flashcards_container = QWidget()
        flashcards_container.setStyleSheet("background-color: #272727; border: none;")  # Dark background
        flashcards_container.setLayout(self.flashcards_layout)
        return flashcards_container

    def open_add_dialog(self):
        """ Opens a dialog to enter a question and answer """
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Flashcard")
        dialog.setFixedSize(400, 300)

        layout = QVBoxLayout(dialog)

        # Question Field
        question_label = QLabel("Question:")
        question_label.setFont(QFont("Poppins", 11))
        layout.addWidget(question_label)
        question_input = QLineEdit()
        question_input.setFont(QFont("Poppins", 10))
        layout.addWidget(question_input)

        # Answer Field
        answer_label = QLabel("Answer:")
        answer_label.setFont(QFont("Poppins", 11))
        layout.addWidget(answer_label)
        answer_input = QTextEdit()
        answer_input.setFont(QFont("Poppins", 10))
        answer_input.setFixedHeight(80)
        layout.addWidget(answer_input)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        add_btn = QPushButton("Add")
        cancel_btn = QPushButton("Cancel")

        # Style buttons
        add_btn.setFont(QFont("Poppins", 10, QFont.Weight.Bold))
        cancel_btn.setFont(QFont("Poppins", 10))
        add_btn.setStyleSheet("background-color: #28a745; color: white; padding: 6px; border-radius: 6px;")
        cancel_btn.setStyleSheet("background-color: #dc3545; color: white; padding: 6px; border-radius: 6px;")

        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(add_btn)
        layout.addLayout(btn_layout)

        # Button Actions
        def add_flashcard():
            question = question_input.text().strip()
            answer = answer_input.toPlainText().strip()
            if question and answer:
                self.create_flashcard(question, answer)
                self.save_flashcards()
                dialog.accept()  # Close dialog

        add_btn.clicked.connect(add_flashcard)
        cancel_btn.clicked.connect(dialog.reject)

        dialog.exec()  # Show modal dialog

    def wrap_text(self, text, max_length=20):
        """ Inserts line breaks every `max_length` characters to simulate word wrapping """
        words = text.split()
        wrapped_text = ""
        line = ""

        for word in words:
            while len(word) > max_length:  # If a single word is too long, break it
                wrapped_text += word[:max_length] + "\n"
                word = word[max_length:]

            if len(line) + len(word) > max_length:
                wrapped_text += line.strip() + "\n"
                line = ""

            line += word + " "

        wrapped_text += line.strip()
        return wrapped_text

    def create_flashcard(self, question, answer):
        """ Creates a flashcard and places it in a 3x3 grid """
        if len(self.flashcards) >= self.GRID_ROWS * self.GRID_COLS:
            print("Grid full. Can't add more flashcards.")
            return

        card_button = QPushButton()
        card_button.setFixedSize(QSize(200, 150))
        card_button.setFont(QFont("Poppins", 12))
        card_button.setStyleSheet("""
            QPushButton {
                background-color: #333;
                color: white;
                border-radius: 12px;
                font-size: 14px;
                padding: 10px;
                text-align: center;
                border: 2px solid #007BFF;
            }
            QPushButton:hover {
                background-color: #444;
            }
        """)

        formatted_question = self.wrap_text(question)
        formatted_answer = self.wrap_text(answer)
        card_button.setText(f"❓ {formatted_question}")

        def toggle_text():
            """ Switches between question and answer """
            if card_button.text().startswith("❓"):
                card_button.setText(f"✅ {formatted_answer}")
            else:
                card_button.setText(f"❓ {formatted_question}")

        card_button.clicked.connect(toggle_text)

        # Determine correct grid placement
        index = len(self.flashcards)
        row = index // self.GRID_COLS
        col = index % self.GRID_COLS
        self.flashcards_layout.addWidget(card_button, row, col)

        self.flashcards.append((question, answer))

    def load_flashcards(self):
        """ Loads flashcards from the JSON file and ensures no duplicates """
        file_path = self.SAVE_PATH
        if not os.path.exists(file_path):
            self.flashcards = []
            return

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read().strip()
                self.flashcards = json.loads(content) if content else []
        except (json.JSONDecodeError, FileNotFoundError):
            self.flashcards = []

        # Clear the grid layout before adding new flashcards
        for i in reversed(range(self.flashcards_layout.count())):
            widget = self.flashcards_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Reset the list and recreate flashcards
        flashcards_copy = self.flashcards[:]
        self.flashcards.clear()

        for question, answer in flashcards_copy:
            self.create_flashcard(question, answer)

    def save_flashcards(self):
        """ Saves flashcards to JSON file """
        os.makedirs(os.path.dirname(self.SAVE_PATH), exist_ok=True)
        with open(self.SAVE_PATH, "w", encoding="utf-8") as file:
            json.dump(self.flashcards, file, indent=4)




