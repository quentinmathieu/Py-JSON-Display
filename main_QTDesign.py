# -*- coding: utf-8 -*-
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
        # self.centralwidget.setStyleSheet("background-color: rgba(0, 120, 185, 60)")
        # #14232A
        self.setStyleSheet(
        """
        QWidget{ margin:0; background : #F1F1F1; border-left: 0px;}
        QScrollBar{background : none}
        QMainWindow{border-radius: 10px;background-color: transparent}
        
        """)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.tabWidget.setStyleSheet("border:0px")
        self.DwwmTab()
    
    def loadCourses(self, jsonFile, scrollArea):
        scrollWidget = QWidget()
        scrollWidget.setStyleSheet("margin:0 0 50 0")
        scrollLayout = QVBoxLayout(scrollWidget)
        with open(jsonFile, encoding='utf-8') as jsonFile:
            globalCourses = json.load(jsonFile)
            for categoriesIndex in globalCourses:
                categoryLayout = QVBoxLayout()
                label = QLabel("========================\n{}\n========================\n".format(categoriesIndex))
                
                # disable horizontal scroll
                label.setWordWrap(True)
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                categoryLayout.addWidget(label)
                category = globalCourses[categoriesIndex]
                for course in category:
                    courseBtn = QPushButton(text=course["nom"],parent=self)
                    test = ""
                    
                    for file in course['files']:
                        test += file['name']
                    courseBtn.clicked.connect(lambda : self.copyBuffer(globalCourses))
                    categoryLayout.addWidget(courseBtn)
                categoryWidget = QWidget()
                categoryWidget.setLayout(categoryLayout)
                categoryWidget.setStyleSheet("background-color: white; border-radius:5; margin:0 10 30 10")
                scrollLayout.addWidget(categoryWidget)
                # break
        scrollArea.setWidget(scrollWidget)
    
    def copyBuffer(self, globalCourses):
        
        categoryName = self.sender().parent().findChild(QLabel).text()
        categoryName = categoryName.replace("==","").replace("\n","")
        
        courseName = self.sender().text()

        for course in globalCourses[categoryName]:
            
            if course['nom'] == courseName:
                print(course['description'].encode('utf-8').decode('utf-8'))
                description = course['description']
                clipboard = description
                for file in course['files']:
                   clipboard += file['name']+"\n"
        pyperclip.copy(clipboard)

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
    app.exec()


if __name__ == '__main__':
    main() 