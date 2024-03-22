from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import json
import os

class MyGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        # self.setGeometry(50, 100, 800, 700)
        # self.setWindowTitle("Title!")
        self.setStyleSheet("border-width: 0px; border-style: solid")
        self.wid = QWidget(self)

        # add a scroll area that is resizable
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
      
        # add a widget that contains the scroll area
        scrollWidget = QWidget()
        scrollLayout = QVBoxLayout(scrollWidget)
        with open("DL.json") as jsonFile:
            self.globalCourses = json.load(jsonFile)
            for categoriesIndex in self.globalCourses:
                categoryLayout = QVBoxLayout()
                label = QLabel("=========================\n{}\n=========================\n".format(categoriesIndex))
                
                # disable horizontal scroll
                label.setWordWrap(True)
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                categoryLayout.addWidget(label)
                category = self.globalCourses[categoriesIndex]
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
        self.scrollArea.setWidget(scrollWidget)
        
        # Create a layout for the main self
        mainLayout = QVBoxLayout()
        # self.scrollArea.setStyleSheet("background-color: #faa805;")

        # Add the scroll area to the main layout
        mainLayout.addWidget(self.scrollArea)
        self.wid.setLayout(mainLayout)
        self.show()
        
    #     # #trigger the login function on click
    #     # self.pushButton.clicked.connect(self.login)

    #     # # trigger sait function on click
    #     # self.pushButton_2.clicked.connect(lambda : self.sayit(self.textEdit_3.toPlainText()))


    # # enable writing in the textbox if the credentials are right 
    # def login(self):
        

    #     # check the credentials
    #     if self.lineEdit.text() == "test" and self.lineEdit_2.text() == "password" : 
    #         self.textEdit_3.setEnabled(True)
    #         self.pushButton_2.setEnabled(True)
    #     else : 
    #         message = QMessageBox()
    #         message.setText("Error")
    #         message.exec()


    # # display the text from the textbox
    # def sayit(self, msg):
    #     message = QMessageBox()
    #     message.setText(msg)
    #     message.exec()



def main():
    app = QApplication([])
    window = MyGUI()
    app.exec()


if __name__ == '__main__':
    main() 