from PyQt6.QtWidgets import QWidget, QMainWindow, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import QProcess, QTimer
from PyQt6.QtGui import QIcon
from . import assets_path
import os
import re

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.handle_output)
        self.process.readyReadStandardError.connect(self.handle_error)
        self.process.finished.connect(self.on_download_finished)
        self.download_dir = os.path.abspath("video")
        self.current_url = ""
        self.is_playlist = False
        self.playlist_dir = ""
        self.check_output = ""
        self.is_downloading = False
        self.initUI()


    def initUI(self):
        self.setWindowIcon(QIcon(assets_path.get('assets//youtube.ico')))
        self.setWindowTitle("Hello from youtube!")
        self.setGeometry(100, 100, 800, 600)

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        self.urlEdit =QLineEdit()
        self.urlEdit.setPlaceholderText("Enter Youtube URL here")
        self.urlEdit.returnPressed.connect(self.onNewUrlEntered)

        self.openButton = QPushButton()
        self.openButton.setText("Video")
        self.openButton.clicked.connect(self.on_open_video_folder)

        self.updateButton = QPushButton()
        self.updateButton.setText("Update yt-dlp")
        self.updateButton.clicked.connect(self.onUpdateYtDlp)

        hBoxTop = QHBoxLayout()
        hBoxTop.addWidget(self.urlEdit)
        hBoxTop.addWidget(self.openButton)
        hBoxTop.addWidget(self.updateButton)
        self.textEdit = QTextEdit()
        self.textEdit.setPlainText("Welcome to the Youtube GUI application!")

        vBox = QVBoxLayout()
        vBox.addLayout(hBoxTop)
        vBox.addWidget(self.textEdit)
        centralWidget.setLayout(vBox)

    def onUpdateYtDlp(self):
        command = "yt-dlp.exe -U"
        self.textEdit.append(f"Running command: {command}")
        self.process.start("yt-dlp.exe", ["-U"])

    def on_open_video_folder(self):
        video_dir = os.path.abspath("video")
        os.makedirs(video_dir, exist_ok=True)
        os.startfile(video_dir)


    def onNewUrlEntered(self):
        if self.is_downloading:
            self.textEdit.append("Please wait for current download to finish")
            return
        url = self.urlEdit.text()
        if not url.strip():
            return
        self.current_url = url
        self.is_downloading = True
        self.textEdit.append(f"Checking URL: {url}")

        # First check if this is a playlist
        self.check_process = QProcess()
        self.check_process.readyReadStandardOutput.connect(self.handle_check_output)
        self.check_process.finished.connect(self.on_playlist_check_finished)
        self.check_process.start("yt-dlp.exe", ["--flat-playlist", "--print", "%(playlist_count)s", url])

    def handle_check_output(self):
        data = self.check_process.readAllStandardOutput().data().decode(encoding="utf-8", errors='replace')
        self.check_output = data.strip()
        self.check_process.deleteLater()
        self.check_process = None

    def on_playlist_check_finished(self):
        url = self.current_url
        output = getattr(self, 'check_output', '').strip()

        # If output is a number > 1, it's a playlist
        try:
            count = int(output)
            self.is_playlist = count > 1
        except (ValueError, AttributeError):
            self.is_playlist = False

        if self.is_playlist:
            self.textEdit.append(f"Detected playlist with {output} videos")
            self.start_playlist_download(url)
        else:
            self.textEdit.append("Single video detected")
            self.start_single_download(url)

    def start_playlist_download(self, url):
        # Create temp directory for playlist
        self.playlist_dir = os.path.join(self.download_dir, "playlist_temp")
        os.makedirs(self.playlist_dir, exist_ok=True)

        self.textEdit.append(f"Downloading playlist to: {self.playlist_dir}")
        # Use playlist_index to maintain order
        self.process.start("yt-dlp.exe", [
            "-P", self.playlist_dir,
            "-o", "%(playlist_index)02d - %(title)s.%(ext)s",
            url
        ])
        self.urlEdit.clear()

    def start_single_download(self, url):
        self.textEdit.append(f"Running command: yt-dlp.exe {url}")
        self.process.start("yt-dlp.exe", [url])
        self.urlEdit.clear()

    def on_download_finished(self, *_):
        if self.is_playlist and self.playlist_dir and os.path.exists(self.playlist_dir):
            QTimer.singleShot(500, self.process_playlist_files)
        else:
            self.is_downloading = False

    def process_playlist_files(self):
        self.textEdit.append("Processing playlist files...")

        # Get all video files in the playlist directory
        video_extensions = {'.mp4', '.mkv', '.webm', '.avi', '.mov', '.flv', '.wmv', '.m4v'}
        files = []
        for f in os.listdir(self.playlist_dir):
            ext = os.path.splitext(f)[1].lower()
            if ext in video_extensions:
                files.append(f)

        # Sort by filename (which includes playlist_index from yt-dlp)
        files.sort()

        if not files:
            self.textEdit.append("No video files found in playlist directory")
            return

        # Get the first video's name (without sequence number) for renaming directory
        first_file = files[0]
        # Extract title from "01 - Title.ext" format
        match = re.match(r"\d+\s*-\s*(.+)\.\w+", first_file)
        if match:
            new_dir_name = match.group(1)
        else:
            new_dir_name = os.path.splitext(first_file)[0]

        # Clean filename characters for directory name
        new_dir_name = re.sub(r'[<>:"/\\|?*]', '_', new_dir_name)
        new_dir_path = os.path.join(self.download_dir, new_dir_name)

        # Rename files to remove the sequence prefix (or keep it based on user preference)
        # User wants: "根据下载的先后顺序，在文件名前面加上序号"
        # The files already have sequence numbers from yt-dlp, but we need to ensure they're correct
        for i, f in enumerate(files, 1):
            ext = os.path.splitext(f)[1]
            old_path = os.path.join(self.playlist_dir, f)

            # Create new filename with sequence number
            new_filename = f"{i:02d} - {os.path.splitext(f)[0].split(' - ', 1)[1] if ' - ' in f else f}"
            new_path = os.path.join(self.playlist_dir, new_filename + ext)

            if old_path != new_path:
                os.rename(old_path, new_path)
                self.textEdit.append(f"Renamed: {new_filename}")

        # Rename directory to first video's name
        if os.path.exists(new_dir_path):
            # Add suffix if directory already exists
            suffix = 1
            while os.path.exists(new_dir_path):
                new_dir_path = os.path.join(self.download_dir, f"{new_dir_name} ({suffix})")
                suffix += 1

        os.rename(self.playlist_dir, new_dir_path)
        self.playlist_dir = ""
        self.is_playlist = False
        self.is_downloading = False
        self.textEdit.append(f"Playlist saved to: {new_dir_path}")

    def handle_output(self):
        data = self.process.readAllStandardOutput().data().decode(encoding="gbk", errors='replace')
        self.textEdit.append(data)
        # Scroll to the end
        self.textEdit.verticalScrollBar().setValue(
            self.textEdit.verticalScrollBar().maximum()
        )

    def handle_error(self):
        data = self.process.readAllStandardError().data().decode(encoding="gbk", errors='replace')
        self.textEdit.append(f"Error: {data}")
        # Scroll to the end
        self.textEdit.verticalScrollBar().setValue(
            self.textEdit.verticalScrollBar().maximum()
        )