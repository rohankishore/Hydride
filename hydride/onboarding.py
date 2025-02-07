# coding:utf-8

import json

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QWidget
from PyQt6.QtWidgets import QPushButton, QCheckBox, QLineEdit, QStackedWidget, QDialog
from qfluentwidgets import (PushButton)

CONFIG_FILE = "resources/data/json/init.json"

with open(CONFIG_FILE, "r") as config_file:
    _config = json.load(config_file)

name = _config["name"]
field = _config["field"]


def load_config():
    try:
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"onboarding": False, "name": "", "field": ""}


def save_config(data):
    with open(CONFIG_FILE, "w") as file:
        json.dump(data, file, indent=4)


class OnboardingScreen(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome to test")
        self.setFixedSize(600, 400)
        self.setStyleSheet("background-color: #1b1f2b; border-radius: 15px;")

        self.config = load_config()
        self.layout = QVBoxLayout(self)
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)

        self.name_screen = self.create_name_screen()
        self.field_screen = self.create_field_screen()

        self.stack.addWidget(self.name_screen)
        self.stack.addWidget(self.field_screen)

    def create_name_screen(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)

        # Left Side - Input Section
        left_side = QVBoxLayout()
        label = QLabel("Enter your name:")
        label.setFont(QFont("Poppins", 14))
        label.setStyleSheet("color: white;")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Your name")
        self.name_input.setStyleSheet("""
            background: #222d3f; color: white; border-radius: 10px; 
            padding: 10px; font-size: 14px;
        """)

        button = QPushButton("Next")
        button.setStyleSheet("""
            QPushButton { background: #3a82f7; color: white; border-radius: 8px; padding: 8px; font-size: 14px; }
            QPushButton:hover { background: #5590ff; }
        """)
        button.clicked.connect(lambda: self.next_slide(1))

        left_side.addWidget(label)
        left_side.addWidget(self.name_input, Qt.AlignmentFlag.AlignCenter)
        left_side.addStretch(1)
        left_side.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Right Side - Banner Image
        image_label = QLabel()
        pixmap = QPixmap("resources/icons/banners/banner1.png")  # Vertical banner
        image_label.setPixmap(pixmap.scaled(200, 350, Qt.AspectRatioMode.KeepAspectRatio))
        image_label.setStyleSheet("border-radius: 10px;")

        layout.addLayout(left_side)
        layout.addWidget(image_label)

        return widget

    def create_field_screen(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)

        # Left Side - Input Section
        left_side = QVBoxLayout()
        label = QLabel(("Select your field:" + "\n"))
        label.setFont(QFont("Poppins", 19))
        label.setStyleSheet("color: white;")

        self.engineering_checkbox = QCheckBox("Engineering")
        self.medical_checkbox = QCheckBox("Medical")

        self.engineering_checkbox.setStyleSheet("color: white; font-size: 14px;")
        self.medical_checkbox.setStyleSheet("color: white; font-size: 14px;")

        self.engineering_checkbox.clicked.connect(lambda: self.medical_checkbox.setChecked(False))
        self.medical_checkbox.clicked.connect(lambda: self.engineering_checkbox.setChecked(False))

        button = PushButton("Finish")
        button.setStyleSheet("""
            QPushButton { background: #3a82f7; color: white; border-radius: 8px; padding: 8px; font-size: 14px; }
            QPushButton:hover { background: #5590ff; }
        """)
        button.clicked.connect(self.finish_onboarding)

        left_side.addWidget(label)
        left_side.addWidget(self.engineering_checkbox)
        left_side.addWidget(self.medical_checkbox)
        left_side.addStretch(1)
        left_side.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Right Side - Banner Image
        image_label = QLabel()
        pixmap = QPixmap("resources/icons/banners/banner2.png")  # Vertical banner
        image_label.setPixmap(pixmap.scaled(250, 400, Qt.AspectRatioMode.KeepAspectRatio))
        image_label.setStyleSheet("border-radius: 10px;")

        layout.addLayout(left_side)
        layout.addWidget(image_label)

        return widget

    def next_slide(self, index):
        self.stack.setCurrentIndex(index)

    def finish_onboarding(self):
        name = self.name_input.text()
        field = "Engineering" if self.engineering_checkbox.isChecked() else "Medical"

        self.config.update({"onboarding": True, "name": name, "field": field})
        save_config(self.config)
        self.close()
