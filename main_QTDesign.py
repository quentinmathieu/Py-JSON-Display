from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt
import os, sys, pyperclip, json

# requirements : pyQt6, pyperclip



class MyGUI(QMainWindow):

    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("gui.ui", self)
        self.setFixedSize(800,700)
        self.move(50,50)
        self.show()
        self.setStyleSheet(
        """
        QWidget{ margin:0; background : #eeeee4} 
        QScrollBar{background : none}
        QMainWindow{border-radius: 10px;background-color: transparent }

        QScrollBar::handle:vertical {
        min-height: 10px;
        }
       
        """)
        self.DwwmTab()
    
    def loadCourses(self, jsonFile, scrollArea):
        scrollWidget = QWidget()
        scrollLayout = QVBoxLayout(scrollWidget)
        with open(jsonFile) as jsonFile:
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
                    # print(course["nom"])
                    # exit()
                    for prop in course:
                        label = QLabel("prop : {}\nvalue:{}\n".format(prop, course[prop]))
                        label.setWordWrap(True)
                        categoryLayout.addWidget(label)
                #     break
                # break
                categoryWidget = QWidget()
                categoryWidget.setLayout(categoryLayout)
                categoryWidget.setStyleSheet("background-color: white; border-radius:5; margin:0 10 30 10")
                scrollLayout.addWidget(categoryWidget)
        scrollArea.setWidget(scrollWidget)
      
    def DwwmTab(self):
        # scrollArea.setStyleSheet("background-color: #faa307")
        self.loadCourses("DL.json", (self.DwwmScrollArea))
        self.loadCourses("DL.json", (self.RanScrollArea))
        
        #trigger the login function on click
        # self.pushButton.clicked.connect(self.login)

        # trigger sait function on click
        # self.pushButton_2.clicked.connect(lambda : self.sayit(self.textEdit_3.toPlainText()))

def main():
    app = QApplication([])
    window = MyGUI()
    window.DwwmTab()
    app.exec()


if __name__ == '__main__':
    main() 