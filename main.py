from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import os, sys, json
from datetime import datetime
import ffmpeg
import klembord


# requirements : pyQt6, klembord, ffmpeg-python

class ConcatenateThread(QThread):
        finished = pyqtSignal(str)
        error = pyqtSignal(str)

        def __init__(self, concat_file_path, output_file, myGui):
            super().__init__()
            self.concat_file_path = concat_file_path
            self.output_file = output_file
            self.myGui = myGui

        def run(self):
            try:
                #try concatenate
                ffmpeg.input(self.concat_file_path, format='concat', safe=0).output(self.output_file, c='copy').run()

                #notif user
                self.myGui.setStatusInterface(True)
                self.myGui.videoInfos.setText("Videos concatenated and saved as \n"+self.output_file.replace('\\',"/"))
                output_message = "Concatenation completed successfully."

                # Clean up temporary files
                os.remove(self.concat_file_path)
                
                self.finished.emit(output_message)
            except Exception as e:
                self.error.emit(str(e))


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
        self.DwwmTab()

        #enable D&D
        self.setAcceptDrops(True)

        # add clear & concat & concat/compress action's btn
        self.clearBtn.clicked.connect(lambda: self.clearList())
        self.concatBtn.clicked.connect(lambda: self.on_click())
        self.compressBtn.clicked.connect(lambda: self.crompressVideos())
        self.delListBtn.clicked.connect(lambda: self.deleteFromList())
        
        
        self.shortcut = QShortcut(QKeySequence(Qt.Key.Key_Ampersand),self)
        self.shortcut.activated.connect(self.firstTab)
        self.shortcut = QShortcut(QKeySequence(Qt.Key.Key_Eacute),self)
        self.shortcut.activated.connect(self.secondTab)
        self.shortcut = QShortcut(QKeySequence(Qt.Key.Key_QuoteDbl),self)
        self.shortcut.activated.connect(self.thirdTab)
        self.shortcut = QShortcut(QKeySequence(Qt.Key.Key_Apostrophe),self)
        self.shortcut.activated.connect(self.fourthTab)
        self.shortcut = QShortcut(QKeySequence(Qt.Key.Key_Escape),self)
        self.shortcut.activated.connect(self.escape)

    def firstTab(self):
        self.tabWidget.setCurrentIndex(0)
        self.showNormal()
    def secondTab(self):
        self.tabWidget.setCurrentIndex(1)
        self.showNormal()
    def thirdTab(self):
        self.tabWidget.setCurrentIndex(2)
        self.showNormal()
    def fourthTab(self):
        self.tabWidget.setCurrentIndex(2)
        self.showFullScreen()
    def escape(self):
        self.showNormal()
    

    
    def loadCourses(self, jsonFile, scrollArea, type):
        
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
                coursesLayout = QGridLayout()
                count = 0
                for course in category:
                    #add Btn for each course*
                    if (type in course['type']):
                        courseBtn = QPushButton(text=course["nom"],parent=self)
                        if "OPT" in course['type']:
                            courseBtn.setStyleSheet("background-color: qlineargradient(x1: 0, y1:0, x2: 1, y2:1, stop: 0 #A47500, stop: 1 #8C5000); border-radius:10;color: white; font-weight:600; font-size:15px;padding :10px")
                        else:
                            courseBtn.setStyleSheet("background-color: qlineargradient(x1: 0, y1:0, x2: 1, y2:1, stop: 0 #206a95, stop: 1 #153754); border-radius:10;color: white; font-weight:600; font-size:15px;padding :10px")
                        courseBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                        courseBtn.setFixedHeight(60)

                        # trigger copy to clipboard on click
                        courseBtn.clicked.connect(lambda : self.copyBuffer(globalCourses))
                        courseBtn.setSizePolicy(QSizePolicy.Policy.Preferred,QSizePolicy.Policy.Preferred)
                        coursesLayout.addWidget(courseBtn,  count, 0)
                        # coursesLayout.addWidget(courseBtn,  count//2, count%2)
                        count+=1
                coursesWidget = QWidget()
                coursesWidget.setLayout(coursesLayout)
                categoryWidget = QWidget()
                categoryWidget.setLayout(categoryLayout)
                categoryLayout.addWidget(coursesWidget)
                categoryWidget.setStyleSheet("background-color: white; border-radius:5; margin:0 10 10 10")
                categoryWidget.setContentsMargins(0, 0, 0, 30)
                if count > 0:
                    scrollLayout.addWidget(categoryWidget)
                # break
                if(scrollArea == self.RanScrollArea):
                    break
        scrollArea.setWidget(scrollWidget)
    
    def copyBuffer(self, globalCourses):
        
        categoryName = self.sender().parent().parent().findChild(QLabel).text()
        categoryName = categoryName.replace("\n","")
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
        self.loadCourses("JSON\\DL.json", (self.DwwmScrollArea), "DWWM")
        self.loadCourses("JSON\\DL.json", (self.RanScrollArea), "RAN")

    
    def on_click(self):
        self.setStatusInterface(False)
        self.videoInfos.setText("Prosessing...")

        # concat all the file paths in a txt file
        file_paths = [self.filesList.item(x).text() for x in range(self.filesList.count())]

        

        if len(file_paths) < 2:
            self.setStatusInterface(True)
            self.videoInfos.setText("Select at least 2 videos to concatenate.")
            return

        codec = None
        for file_path in file_paths:
            # Use ffmpeg to get codec information of the videos
            try:
                probe = ffmpeg.probe(file_path)
            except Exception as error:
                self.setStatusInterface(True)
                self.videoInfos.setText("An exception occurred:"+str(error))
                return 
            video_info = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')
            if codec is None:
                codec = video_info['codec_name']
            elif codec != video_info['codec_name']:
                self.setStatusInterface(True)
                self.videoInfos.setText("Videos have different codecs.")
                return

        # Filter videos by codec
        filtered_files = [f for f in file_paths if ffmpeg.probe(f)['streams'][0]['codec_name'] == codec]

        if len(filtered_files) < 2:
            self.videoInfos.setText("No videos with the same codec found.")
            return


        # Get the directory of the last file for the ouput path
        last_file_dir = os.path.dirname(file_paths[-1])

        # Generate the concat demuxer file
        concat_content = [f"file '{file_path}'" for file_path in filtered_files]
        concat_file_path =     output_file = os.path.join(last_file_dir, "concat.txt") 

        with open(concat_file_path, "w") as concat_file:
            concat_file.write('\n'.join(concat_content))


        # Get current timestamp to create output filename to the same directory as the last input file
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = os.path.join(last_file_dir, f"output_{current_time}.mp4") 

        self.concatThread = ConcatenateThread(concat_file_path, output_file, self)
        # self.concatThread.finished.connect(self.concatenationFinished)
        # self.concatThread.error.connect(self.concatenationError)
        self.concatThread.start()

       
        


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        self.setStatusInterface(True)
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        files.sort()
        
        for f in files:
            if (f.lower().endswith(('.mts', '.mp4', '.avi','.mov','.mkv'))):
                self.filesList.addItem(f)

    def clearList(self):
        self.setStatusInterface(True)
        self.filesList.clear()

    def deleteFromList(self):
        self.setStatusInterface(True)
        listItems=self.filesList.selectedItems()
        if not listItems: return        
        for item in listItems:
            self.filesList.takeItem(self.filesList.row(item))


    def setStatusInterface(self, status):
        self.clearBtn.setEnabled(status)
        self.concatBtn.setEnabled(status)
        self.compressBtn.setEnabled(status)
        self.delListBtn.setEnabled(status)
        self.compressSlider.setEnabled(status)
        self.filesList.setEnabled(status)
        self.dropArea.setEnabled(status)

        self.setAcceptDrops(status)
        self.videoInfos.setText("")

    def crompressVideos(self):
        self.setStatusInterface(True)
        self.videoInfos.setText("WIP")  

def main():
    try :
        # Add ffmpeg to the PATH
        ffmpegPath= os.path.dirname(os.path.realpath(__file__))+"\\ffmpeg\\bin"
        os.environ['PATH'] = ffmpegPath
    except Exception as error:
        print("An exception occurred:"+ str(error))
    app = QApplication(sys.argv)
    window = MyGUI()
    app.exec()


if __name__ == '__main__':
    main() 