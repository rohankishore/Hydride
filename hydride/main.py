import json

from hydride.core import window
# coding:utf-8
import sys
# import qdarktheme
from PyQt6.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open("resources/data/json/init.json", "r") as config_file:
        _config = json.load(config_file)
    if _config["onboarding"]:
        w = window.Window()
        w.show()
    else:
        onboarding_dialog = window.OnboardingScreen()
        onboarding_dialog.exec()
        w = Window()
        w.show()

    app.exec()
