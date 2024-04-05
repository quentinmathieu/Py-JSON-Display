from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import os, sys, json, webbrowser
from datetime import datetime
import ffmpeg
import klembord
import psutil


# requirements : pyQt6, klembord, ffmpeg-python, psutil

class ConcatenateThread(QThread):
        finished = pyqtSignal(str)
        error = pyqtSignal(str)

        def __init__(self, concat_file_path, output_file, myGui, crf = 0):
            super().__init__()
            self.concat_file_path = concat_file_path
            self.output_file = output_file
            self.myGui = myGui
            self.crf = crf

        def run(self):
            try:
                if self.crf>0:
                    ffmpeg.input(self.concat_file_path, format='concat', safe=0).output(self.output_file, vcodec='libx264', crf=self.crf).run()
                    self.myGui.videoInfos.setText("Videos concatenated and saved as \n"+self.output_file.replace('\\',"/"))
                else:
                    ffmpeg.input(self.concat_file_path, format='concat', safe=0).output(self.output_file, c='copy').run()
                    self.myGui.videoInfos.setText("Videos concatenated and saved as \n"+self.output_file.replace('\\',"/"))
                    

                # Clean up temporary files
                os.remove(self.concat_file_path)
                self.myGui.setStatusInterface(True)
                self.finished.emit("ok")
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
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        self.saveJson()
        self.json='JSON\\DL.json'
        self.checkboxes = {"DWWM":self.checkDwwm, "OPTDWWM":self.checkOptDwwm, "RAN":self.checkRan,"OPTRAN":self.checkOptRan, "CDA":self.checkCda, "OPTDCA":self.checkOptCda, "CDARAN":self.checkCdaRan, "OPTCDARAN":self.checkOptCdaRan}
        self.DwwmTab()
        
        # add clear & concat & concat/compress action's btn
        self.clearBtn.clicked.connect(lambda: self.clearList())
        self.concatBtn.clicked.connect(lambda: self.on_click())
        self.compressBtn.clicked.connect(lambda: self.crompressVideos())
        self.delListBtn.clicked.connect(lambda: self.deleteFromList())

        
        self.delCat.clicked.connect(lambda: self.deleteItemFromList(self.categoriesList, "category","delete"))
        self.addCatBtn.clicked.connect(lambda: self.addItemToList(self.categoriesList, self.lineCategoryAdd, "category","add"))
        self.RefreshBtn2.clicked.connect(lambda: self.restart())
        self.RefreshBtn.clicked.connect(lambda: self.restart())
        
        self.addCourseToCat.clicked.connect(lambda: self.addItemToList(self.listCoursesByCat, self.lineCourseAdd, "course","add"))
        self.delCourseFromCat.clicked.connect(lambda: self.deleteItemFromList(self.listCoursesByCat,"course","delete"))
        self.listCoursesByCat.model().rowsMoved.connect(lambda: self.updateJson({"field":"course", "action":"move", "type":"course"}))
        self.listCoursesByCat.itemSelectionChanged.connect(self.editCourse)


        self.categoriesList.itemSelectionChanged.connect(self.showCatCourses)
        self.categoriesList.model().rowsMoved.connect(lambda: self.updateJson({"field":"category", "action":"move", "type":"category"}))

        
        self.editCourseBtn.clicked.connect(self.changeTabEdit)
        self.deleteFileBtn.clicked.connect(lambda:self.delFileCourse(self.filesEdit,"files"))
        
        self.deleteCorrectionBtn.clicked.connect(lambda:self.delFileCourse(self.correctionsEdit,"correction_files"))
        
        self.addFileBtn.clicked.connect(lambda:self.addFileCourse(self.nameFileAdd, self.pathFileAdd,"files", self.filesEdit))
        
        self.addCorrectionBtn.clicked.connect(lambda:self.addFileCourse(self.nameCorrectionAdd, self.pathCorrectionAdd,"correction_files", self.correctionsEdit))

        # diffrents tab shortcuts
        self.shortcut = QShortcut(QKeySequence('Ctrl+a'),self)
        self.shortcut.activated.connect(lambda: self.changeTab(0))
        self.shortcut = QShortcut(QKeySequence('Ctrl+z'),self)
        self.shortcut.activated.connect(lambda: self.changeTab(1))  
        self.shortcut = QShortcut(QKeySequence('Ctrl+e'),self)
        self.shortcut.activated.connect(lambda: self.changeTab(2))
        self.shortcut = QShortcut(QKeySequence('Ctrl+r'),self)
        self.shortcut.activated.connect(lambda: self.changeTab(3))
        self.shortcut = QShortcut(QKeySequence('Ctrl+t'),self)
        self.shortcut.activated.connect(lambda: self.changeTab(4))
        self.shortcut = QShortcut(QKeySequence('Ctrl+tab'),self)
        self.shortcut.activated.connect(lambda: self.changeTab(5))
        self.shortcut = QShortcut(QKeySequence(Qt.Key.Key_Escape),self)
        self.shortcut.activated.connect(lambda: self.changeTab(0))
    
    def saveJson(self):
        # Save the JSON file each a day
        todaySave = ('JSON\\save\\save_{}.json'.format(datetime.today().strftime('%Y-%m-%d')))
        if not os.path.isfile(todaySave):
            os.system('copy JSON\\DL.json JSON\\save\\save_{}.json'.format(datetime.today().strftime('%Y-%m-%d')))
    
    def editCourse(self):
        try:
            #Disconnect every listener to avoid multiple call methods on category switch
            if  len(self.courseNameEdit.text())>0:
                self.courseNameEdit.textChanged.disconnect()
                self.descriptionEdit.textChanged.disconnect()
                for box in self.checkboxes:
                    self.checkboxes[box].stateChanged.disconnect()
            self.coursesTab.setEnabled(True)
            cat = self.categoriesList.selectedItems()[0].text()
            
            # get course info or lock the interface
            try:
                course = self.listCoursesByCat.selectedItems()[0].text()
            except:
                self.courseNameEdit.textChanged.connect(self.updateCourse)
                self.descriptionEdit.textChanged.connect(self.updateCourse)
                for box in self.checkboxes:
                    self.checkboxes[box].stateChanged.connect(self.updateCourse)
                self.coursesTab.setEnabled(False)
                return
            
            # fill the field's values with JSON datas
            for courseIndex in self.globalCourses[cat]:
                if courseIndex["nom"]==course:
                    course=courseIndex
                    break
            self.courseNameEdit.setText(course["nom"])
            self.descriptionEdit.setPlainText(course["description"])
            
            # uncheck all type in UI
            for typeIndex in self.checkboxes:
                self.checkboxes[typeIndex].setCheckState(Qt.CheckState.Unchecked)
            # check course's types in UI 
            for type in course['type']:
                self.checkboxes[type].setCheckState(Qt.CheckState.Checked)

            #  If there are files and corrections files display them
            try:
                self.filesEdit.clear()
                for file in course["files"]:
                    self.filesEdit.addItem(file["name"])
            except:
                False
            try:
                self.correctionsEdit.clear()
                for correction in course["correction_files"]:
                    self.correctionsEdit.addItem(correction["name"])
            except:
                False
            
            # put connect listeners on fields and checkboxes
            self.courseNameEdit.textChanged.connect(self.updateCourse)
            self.descriptionEdit.textChanged.connect(self.updateCourse)
            for box in self.checkboxes:
                self.checkboxes[box].stateChanged.connect(self.updateCourse)
        except:
            self.coursesTab.setEnabled(False)
        
    def delFileCourse(self, list, property):
        courseName = self.listCoursesByCat.selectedItems()[0].text()
        cat=self.categoriesList.selectedItems()[0].text()

        listItems=list.selectedItems()
        if not listItems: return
        for item in listItems:
            list.takeItem(list.row(item))
        
        files=[]
        for courseIndex in self.globalCourses[cat]:
            if courseName==courseIndex['nom']:
                for file in courseIndex[property]:
                    if listItems[0].text()!=file['name']:
                        files.append(file)
                courseIndex[property]=files

        with open(self.json, 'w', encoding='utf8') as json_file:
            json.dump(self.globalCourses,json_file, ensure_ascii=False, indent=2)
            
    def addFileCourse(self, nameField, pathField, property, list):
        courseName = self.listCoursesByCat.selectedItems()[0].text()
        cat=self.categoriesList.selectedItems()[0].text()
        
        newFile = {"name":nameField.text(), "path":pathField.text()}
        for courseIndex in self.globalCourses[cat]:
            if courseName==courseIndex['nom']:
                courseIndex[property].append(newFile)
        list.addItem(nameField.text())
        nameField.setText("")
        pathField.setText("")
        with open(self.json, 'w', encoding='utf8') as json_file:
            json.dump(self.globalCourses,json_file, ensure_ascii=False, indent=2)
        
    def updateCourse(self):
        courseName = self.listCoursesByCat.selectedItems()[0].text()
        types=[]
        for box in self.checkboxes:
            if (self.checkboxes[box].isChecked()):
                types.append(box)
            
        cat=self.categoriesList.selectedItems()[0].text()
        for courseIndex in self.globalCourses[cat]:
            if courseName==courseIndex['nom']:
                courseIndex['nom'] = self.courseNameEdit.text()
                courseIndex['description'] = self.descriptionEdit.toPlainText()
                courseIndex['type']=types
                self.listCoursesByCat.selectedItems()[0].setText(self.courseNameEdit.text())
        with open(self.json, 'w', encoding='utf8') as json_file:
            json.dump(self.globalCourses,json_file, ensure_ascii=False, indent=2)
            
        

    def showCatCourses(self):
        if  len(self.courseNameEdit.text())>0:
            self.listCoursesByCat.itemSelectionChanged.disconnect()
        self.listCoursesByCat.clear()
        category = self.categoriesList.selectedItems()[0].text()
        try:
            for course in self.globalCourses[category]:
                self.listCoursesByCat.addItem(course['nom'])
            self.listCoursesByCat.setCurrentRow(0)
        except:
            False
        self.listCoursesByCat.itemSelectionChanged.connect(lambda:self.editCourse())
        self.editCourse()
    
    def deleteItemFromList(self, list,type,action):
        remove = list.selectedItems()[0].text()

        self.setStatusInterface(True)
        listItems=list.selectedItems()
        if not listItems: return
        for item in listItems:
            list.takeItem(list.row(item))
        self.updateJson({"type":type,"action":action, "field":remove})
            
    def updateJson(self, array):
        newCat = array['field'] if array["type"]=="category" and array["action"]=="add" else False
        newCourse = array['field'] if array["type"]=="course" and array["action"]=="add" else False
        
        newJsonIndex = []
        for index in range(self.categoriesList.count()):
            newJsonIndex.append(self.categoriesList.item(index).text())
           
        newJson = {} 
        for cat in newJsonIndex:
            try:
                newJson[cat] = self.globalCourses[cat]
            except:
                if (newCat):
                    newJson[newCat]= []
        
        try:
            cat= self.categoriesList.selectedItems()[0].text() if array["type"]=="course" and (array["action"]=="delete" or array["action"]=="move")  else False
            if cat != False:
                categoryContent = []
                for index in range(self.listCoursesByCat.count()):
                    for course in newJson[cat]:
                        if course['nom']==self.listCoursesByCat.item(index).text() and course['nom'] != array['field']:
                            categoryContent.append(course)
            newJson[cat] = categoryContent
        except:
            False
        try:
            cat= self.categoriesList.selectedItems()[0].text() if array["type"]=="course" and array["action"]=="add" else False
            newJson[cat].append({"nom":newCourse, "description":"", "files":[],"correction_files":[], "type": ["DWWM","CDA","CDARAN","RAN"]}) 
        except:
            False
        self.globalCourses = newJson

        with open(self.json, 'w', encoding='utf8') as json_file:
            json.dump( newJson,json_file, ensure_ascii=False, indent=2)
        
    def restart(self):
        os.execl(sys.executable, '"{}"'.format(sys.executable), *sys.argv)
        exit()
        
    def addItemToList(self, list, field, type, action):
        for index in range(list.count()):
            if field.text() == list.item(index).text():
                return False
        list.addItem(field.text())
        self.updateJson({"type":type,"action":action, "field":field.text()})
        field.setText("")
        list.setCurrentRow(list.count()-1)
        
    def changeTab(self, tabNum, size = "normal"):
        self.tabWidget.setCurrentIndex(tabNum)
        if size == "normal":
            self.showNormal()
        else:
            self.showFullScreen() 
            
    def changeTabEdit(self):
        self.tabWidgetEdit.setCurrentIndex(1)

    def loadCourses(self, jsonFile, scrollArea, type):
        
        scrollWidget = QWidget()
        scrollWidget.setStyleSheet("margin:0 0 50 0")
        scrollLayout = QVBoxLayout(scrollWidget)
        with open(jsonFile, encoding='utf-8') as jsonFile:
            self.globalCourses = json.load(jsonFile)
            for categoriesIndex in self.globalCourses:
                categoryLayout = QVBoxLayout()
                categoryLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                if type == "DWWM":
                    self.categoriesList.addItem(categoriesIndex)
                    self.categoriesList.setCurrentRow(0)
                    self.showCatCourses()
                    try:
                        self.listCoursesByCat.setCurrentRow(0)
                    except:
                        False

                #display category name
                label = QLabel("\n{}".format(categoriesIndex))
                label.setWordWrap(True)
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet("font-size:24px;color:#153754;font-weight:600;font-family: 'Comic Sans';")
                categoryLayout.addWidget(label)
                category = self.globalCourses[categoriesIndex]
                coursesLayout = QGridLayout()
                count = 0
                try:
                    for course in category:
                        #add Btn for each course*
                        if (type in course['type'] or ("OPT"+type) in course['type']):
                            courseBtn = QPushButton(text=course["nom"],parent=self)
                            if ("OPT"+type) in course['type']:
                                courseBtn.setStyleSheet("background-color: qlineargradient(x1: 0, y1:0, x2: 1, y2:1, stop: 0 #A47500, stop: 1 #8C5000); border-radius:10;color: white; font-weight:600; font-size:15px;padding :10px")
                            else:
                                courseBtn.setStyleSheet("background-color: qlineargradient(x1: 0, y1:0, x2: 1, y2:1, stop: 0 #206a95, stop: 1 #153754); border-radius:10;color: white; font-weight:600; font-size:15px;padding :10px")
                            courseBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                            courseBtn.setFixedHeight(60)

                            # trigger copy to clipboard on click
                            courseBtn.clicked.connect(lambda : self.copyBuffer())
                            courseBtn.setSizePolicy(QSizePolicy.Policy.Preferred,QSizePolicy.Policy.Preferred)
                            # coursesLayout.addWidget(courseBtn,  count, 0)
                            coursesLayout.addWidget(courseBtn,  count//3, count%3)
                            count+=1
                except:
                    False
                coursesWidget = QWidget()
                coursesWidget.setLayout(coursesLayout)
                categoryWidget = QWidget()
                categoryWidget.setLayout(categoryLayout)
                categoryLayout.addWidget(coursesWidget)
                categoryWidget.setStyleSheet("background-color: white; border-radius:5; margin:0 10 10 10")
                categoryWidget.setContentsMargins(0, 0, 0, 30)
                if count > 0:
                    scrollLayout.addWidget(categoryWidget)
        scrollArea.setWidget(scrollWidget)
   
    
    def copyBuffer(self):
        categoryName = self.sender().parent().parent().findChild(QLabel).text()
        categoryName = categoryName.replace("\n","")
        courseName = self.sender().text()
        klembord.init()
        for course in self.globalCourses[categoryName]:
            
            
            if course['nom'] == courseName:
                try:
                    # add description to the clipboard var
                    clipboard = course['description']+'\n'
                except:
                    clipboard = "\n"
                modifiers = QApplication.keyboardModifiers()
                try:
                    for file in course['files']:
                    # add path's files to the clipboard var
                        clipboard += " <a href='"+file['path']+"'>"+"🗎"+"</a>"
                        if modifiers == Qt.KeyboardModifier.ControlModifier:                 
                            webbrowser.open(file['path'], new=2, autoraise=True)
                except:
                    False
                try:
                    if modifiers == Qt.KeyboardModifier.ControlModifier:
                        for correction in course['correction_files']:
                            webbrowser.open(correction['path'], new=2, autoraise=True)
                except:
                    False

        # set the clipboard with all html support (thx https://github.com/OzymandiasTheGreat/klembord)
        klembord.set_with_rich_text('', clipboard.replace("\n","<br>")) 

    def DwwmTab(self):
        self.loadCourses(self.json, (self.DwwmScrollArea), "DWWM")
        self.loadCourses(self.json, (self.RanScrollArea), "RAN")
        self.loadCourses(self.json, (self.cdaScrollArea), "CDA")
        self.loadCourses(self.json, (self.cdaRanScrollArea), "CDARAN")
        self.editCourse()

    
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
        concat_file_path =  os.path.join(last_file_dir, "concat.txt") 

        with open(concat_file_path, "w") as concat_file:
            concat_file.write('\n'.join(concat_content))


        # Get current timestamp to create output filename to the same directory as the last input file
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = os.path.join(last_file_dir, f"output_{current_time}.mp4") 

        self.concatThread = ConcatenateThread(concat_file_path, output_file, self)
        self.stopBtn.clicked.connect(lambda: self.stop())
        self.concatThread.start()

    def crompressVideos(self):
        self.setStatusInterface(False)
        self.videoInfos.setText("Prosessing...")
        file_paths = [self.filesList.item(x).text() for x in range(self.filesList.count())]
        

        if len(file_paths) < 1:
            self.setStatusInterface(True)
            self.videoInfos.setText("Select at least 1 video to convert.")
            return

        # Filter videos by codec
        filtered_files = [f for f in file_paths]

        # Get the directory of the last file for the ouput path
        last_file_dir = os.path.dirname(file_paths[-1])

        # Generate the concat demuxer file
        concat_content = [f"file '{file_path}'" for file_path in filtered_files]
        concat_file_path = os.path.join(last_file_dir, "concat.txt") 
        
        with open(concat_file_path, "w") as concat_file:
            concat_file.write('\n'.join(concat_content))
        
        # Get current timestamp to create output filename to the same directory as the last input file
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = os.path.join(last_file_dir, f"output_{current_time}_compress.mp4") 
        self.concatThread = ConcatenateThread(concat_file_path, output_file, self, self.compressSlider.value())
        self.stopBtn.clicked.connect(lambda: self.stop())
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
        invers = False if status else True
        self.clearBtn.setEnabled(status)
        self.concatBtn.setEnabled(status)
        self.compressBtn.setEnabled(status)
        self.delListBtn.setEnabled(status)
        self.compressSlider.setEnabled(status)
        self.filesList.setEnabled(status)
        self.dropArea.setEnabled(status)
        self.stopBtn.setEnabled(invers)

        self.setAcceptDrops(status)

    def stop(self):
        #stop concat / compress
        PROCNAME = "ffmpeg.exe"

        
        for proc in psutil.process_iter():
            # check whether the process name matches
            if proc.name() == PROCNAME:
                proc.kill()
        self.setStatusInterface(True)
        self.videoInfos.setText("CANCELED")

 

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