from PyQt6.QtWidgets import QWidget, QMainWindow, QTextEdit, QLineEdit, QVBoxLayout
from PyQt6.QtCore import QProcess
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.process = QProcess()
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
        command = f"yt-dlp.exe {self.urlEdit.text()}"
        self.textEdit.append(f"Running command: {command}")
        self.process.start("yt-dlp.exe", [self.urlEdit.text()])
        self.urlEdit.clear()

    def handle_output(self):
        try:
            # Try UTF-8 first
            data = self.process.readAllStandardOutput().data().decode('utf-8', errors='ignore')
            self.textEdit.append(data)
            # Scroll to the end
            self.textEdit.verticalScrollBar().setValue(
                self.textEdit.verticalScrollBar().maximum()
            )
        except UnicodeDecodeError:
            # Fallback to system default encoding
            data = self.process.readAllStandardOutput().data().decode('cp1252', errors='ignore')
            self.textEdit.append(data)
            # Scroll to the end
            self.textEdit.verticalScrollBar().setValue(
                self.textEdit.verticalScrollBar().maximum()
            )

    def handle_error(self):
        try:
            data = self.process.readAllStandardError().data().decode('utf-8', errors='ignore')
            self.textEdit.append(f"Error: {data}")
            # Scroll to the end
            self.textEdit.verticalScrollBar().setValue(
                self.textEdit.verticalScrollBar().maximum()
            )
        except UnicodeDecodeError:
            data = self.process.readAllStandardError().data().decode('cp1252', errors='ignore')
            self.textEdit.append(f"Error: {data}")
            # Scroll to the end
            self.textEdit.verticalScrollBar().setValue(
                self.textEdit.verticalScrollBar().maximum()
            )