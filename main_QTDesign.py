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
        self.setWindowTitle('Training')
        # self.setWindowFlags(Qt.WindowType.FramelessWindowHint|Qt.WindowType.WindowSystemMenuHint)

        # self.centralwidget.setStyleSheet("background-color: rgba(0, 120, 185, 60)")
        # #14232A
        self.setStyleSheet(
        """
        QWidget{ margin:0; background : #F1F1F1; border-left: 0px;}
        QScrollBar{background : none}
        QMainWindow{border-radius: 10px;background-color: transparent}
        
        """)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
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
                categoryLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label = QLabel("\n{}".format(categoriesIndex))
                
                # disable horizontal scroll
                label.setWordWrap(True)
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet("font-size:24px;color:#153754;font-weight:600;font-family: 'Comic Sans';")
                categoryLayout.addWidget(label)
                category = globalCourses[categoriesIndex]
                for course in category:
                    courseBtn = QPushButton(text=course["nom"],parent=self)
                    courseBtn.setStyleSheet("background-color: qlineargradient(x1: 0, y1:0, x2: 1, y2:1, stop: 0 #206a95, stop: 1 #153754); border-radius:15;color: white; font-weight:600; font-size:15px;padding :10px")
                    # stylesheet = "QWidget {background-color: qlineargradient(x1: 0, x2: 1, stop: 0 red, stop: 1 blue)}"

                    courseBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                    courseBtn.setFixedHeight(100)

                    test = ""
                    
                    for file in course['files']:
                        test += file['name']
                    courseBtn.clicked.connect(lambda : self.copyBuffer(globalCourses))
                    categoryLayout.addWidget(courseBtn)
                categoryWidget = QWidget()
                categoryWidget.setLayout(categoryLayout)
                categoryWidget.setStyleSheet("background-color: white; border-radius:5; margin:0 10 30 10")
                categoryWidget.setContentsMargins(0, 0, 0, 30)
                scrollLayout.addWidget(categoryWidget)
                # break
                if(scrollArea == self.RanScrollArea):
                    break
        scrollArea.setWidget(scrollWidget)
    
    def copyBuffer(self, globalCourses):
        
        categoryName = self.sender().parent().findChild(QLabel).text()
        categoryName = categoryName.replace("==","").replace("\n","")
        
        courseName = self.sender().text()

        for course in globalCourses[categoryName]:
            
            if course['nom'] == courseName:
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