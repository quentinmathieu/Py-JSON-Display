from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt
import json
import os

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
        
        """
        )
        scrollArea = self.scrollArea
        # scrollArea.setStyleSheet("background-color: #faa307")
        scrollWidget = QWidget()
        scrollLayout = QVBoxLayout(scrollWidget)
    
        with open("DL.json") as jsonFile:
            globalCourses = json.load(jsonFile)
            for categoriesIndex in globalCourses:
                categoryLayout = QVBoxLayout()
                label = QLabel("=========================\n{}\n=========================\n".format(categoriesIndex))
                
                # disable horizontal scroll
                label.setWordWrap(True)
                # label.setAlignment(Qt.AlignmentFlag.AlignTop)
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
                categoryWidget.setStyleSheet("background-color: white; border-radius:5; margin:0 10 30 10")
                scrollLayout.addWidget(categoryWidget)
        scrollArea.setWidget(scrollWidget)
        #trigger the login function on click
        # self.pushButton.clicked.connect(self.login)

        # trigger sait function on click
        # self.pushButton_2.clicked.connect(lambda : self.sayit(self.textEdit_3.toPlainText()))


    # enable writing in the textbox if the credentials are right 
    def login(self):
        

        # check the credentials
        if self.lineEdit.text() == "test" and self.lineEdit_2.text() == "password" : 
            self.textEdit_3.setEnabled(True)
            self.pushButton_2.setEnabled(True)
        else : 
            message = QMessageBox()
            message.setText("Error")
            message.exec()


    # display the text from the textbox
    def sayit(self, msg):
        message = QMessageBox()
        message.setText(msg)
        message.exec()



def main():
    app = QApplication([])
    window = MyGUI()
    app.exec()


if __name__ == '__main__':
    main() 