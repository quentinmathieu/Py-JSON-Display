from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt
import os, sys, pyperclip, json,html
import klembord


# requirements : pyQt6, pyperclip, klembord



class MyGUI(QMainWindow):

    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("gui.ui", self)
        self.setFixedSize(800,700)
        self.move(50,50)
        self.show()
        self.setWindowTitle('Training')
        # self.setWindowFlags(Qt.WindowType.FramelessWindowHint|Qt.WindowType.WindowSystemMenuHint)
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

                #display category name
                label = QLabel("\n{}".format(categoriesIndex))
                label.setWordWrap(True)
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet("font-size:24px;color:#153754;font-weight:600;font-family: 'Comic Sans';")
                categoryLayout.addWidget(label)
                category = globalCourses[categoriesIndex]
                for course in category:
                    #add Btn for each course
                    courseBtn = QPushButton(text=course["nom"],parent=self)
                    courseBtn.setStyleSheet("background-color: qlineargradient(x1: 0, y1:0, x2: 1, y2:1, stop: 0 #206a95, stop: 1 #153754); border-radius:15;color: white; font-weight:600; font-size:15px;padding :10px")
                    courseBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                    courseBtn.setFixedHeight(100)

                    # trigger copy to clipboard on click
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
        klembord.init()
        for course in globalCourses[categoryName]:
            
            
            if course['nom'] == courseName:

                # add description to the clipboard var
                clipboard = course['description']
                
                for file in course['files']:
                   # add path's files to the clipboard var
                   clipboard += file['name']+" \n"
        # set the clipboard with all html support (thx https://github.com/OzymandiasTheGreat/klembord)
        klembord.set_with_rich_text('', clipboard.replace("\n","<br>"))

    def DwwmTab(self):
        self.loadCourses("JSON\\DL.json", (self.DwwmScrollArea))
        self.loadCourses("JSON\\DL.json", (self.RanScrollArea))
        

def main():
    app = QApplication([])
    window = MyGUI()
    app.exec()


if __name__ == '__main__':
    main() 