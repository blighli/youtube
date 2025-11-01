from PyQt6.QtWidgets import QApplication, QWidget

def main():
    app = QApplication([])
    window = QWidget()
    window.setWindowTitle("Hello from youtube!")
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
