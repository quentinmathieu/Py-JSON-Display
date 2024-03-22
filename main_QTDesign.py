from PyQt5.QtWidgets import *
from PyQt5 import uic

class MyGUI(QMainWindow):

    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("form.ui", self)
        self.show()

        #trigger the login function on click
        self.pushButton.clicked.connect(self.login)

        # trigger sait function on click
        self.pushButton_2.clicked.connect(lambda : self.sayit(self.textEdit_3.toPlainText()))


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