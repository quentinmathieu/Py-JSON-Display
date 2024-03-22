from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt
import json
import os


def main():
    app = QApplication([])
    window = QWidget()
    window.setGeometry(50, 100, 800, 700)
    # window.setWindowFlag(Qt.WindowType.FramelessWindowHint|Qt.WindowType.WindowMaximizeButtonHint)
    window.setWindowTitle("Programm")
    
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
            categoryWidget.setStyleSheet("background-color: white; border-radius:10px")
            scrollLayout.addWidget(categoryWidget)
    scrollWidget.setStyleSheet("margin:0;")
    # Set the widget inside the scroll area
    scrollArea.setWidget(scrollWidget)
    
    # Create a layout for the main window
    mainLayout = QVBoxLayout(window)

    
    # Add the scroll area to the main layout
    mainLayout.addWidget(scrollArea)
    mainLayout.setContentsMargins(0, 0, 0, 0)
    
    window.setStyleSheet(
        """
        QWidget{ background-color: #faa307;margin:0;} 
        QScrollBar{height: 0; width: 0;}
        QMainWindow{border-radius: 10px;background-color: transparent }
        
        """
    )
    window.setLayout(mainLayout)
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
