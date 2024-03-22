from PyQt6.QtWidgets import *
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import json
import os


def main():
    print(os.listdir())
    app = QApplication([])
    window = QWidget()
    window.setGeometry(50, 100, 800, 700)
    window.setWindowTitle("Title!")
    window.setStyleSheet("border-width: 0px; border-style: solid")
    
    # add a scroll area that is resizable
    scrollArea = QScrollArea()
    scrollArea.setWidgetResizable(True)
    
    # add a widget that contains the scroll area
    scrollWidget = QWidget()
    scrollLayout = QVBoxLayout(scrollWidget)
    
    with open("DL.json") as jsonFile:
        globalCourses = json.load(jsonFile)
        for categoriesIndex in globalCourses:
            categoryLayout = QVBoxLayout()
            label = QLabel("=========================\n{}\n=========================\n".format(categoriesIndex))
            
            # disable horizontal scroll
            label.setWordWrap(True)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            categoryLayout.addWidget(label)
            category = globalCourses[categoriesIndex]
            for course in category:
                for prop in course:
                    label = QLabel("prop : {}\nvalue:{}\n".format(prop, course[prop]))
                    label.setWordWrap(True)
                    categoryLayout.addWidget(label)
            #     break
            # break
            categoryWidget = QWidget()
            categoryWidget.setLayout(categoryLayout)
            categoryWidget.setStyleSheet("background-color: white;")
            scrollLayout.addWidget(categoryWidget)
    
    # Set the widget inside the scroll area
    scrollArea.setWidget(scrollWidget)
    
    # Create a layout for the main window
    mainLayout = QVBoxLayout(window)
    scrollArea.setStyleSheet("background-color: #faa805;")

    
    # Add the scroll area to the main layout
    mainLayout.addWidget(scrollArea)
    
    window.setLayout(mainLayout)
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
