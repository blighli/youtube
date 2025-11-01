from PyQt6.QtWidgets import QWidget, QMainWindow, QTextEdit, QLineEdit, QVBoxLayout
from PyQt6.QtCore import QProcess
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.process = QProcess()
        #self.process.setProgram("yt-dlp.exe")
        self.process.readyReadStandardOutput.connect(self.handle_output)
        self.process.readyReadStandardError.connect(self.handle_error)
        self.initUI()


    def initUI(self):
        self.setWindowTitle("Hello from youtube!")
        self.setGeometry(100, 100, 800, 600)

        cenralWidget = QWidget()
        self.setCentralWidget(cenralWidget)

        self.urlEdit =QLineEdit()
        self.urlEdit.setPlaceholderText("Enter Youtube URL here")
        self.urlEdit.returnPressed.connect(self.onNewUrlEntered)
        
        self.textEdit = QTextEdit()
        self.textEdit.setPlainText("Welcome to the Youtube GUI application!")

        vBox = QVBoxLayout()
        vBox.addWidget(self.urlEdit)
        vBox.addWidget(self.textEdit)
        cenralWidget.setLayout(vBox)

    def onNewUrlEntered(self):
        command = self.urlEdit.text()
        self.process.start(command)
        self.urlEdit.clear()

    def handle_output(self):
        data = self.process.readAllStandardOutput().data().decode()
        self.textEdit.append(data)

    def handle_error(self):
        data = self.process.readAllStandardError().data().decode()
        self.textEdit.append(f"Error: {data}")