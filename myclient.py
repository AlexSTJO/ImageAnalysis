import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLineEdit, QMessageBox
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QPixmap
from PyQt5.QtCore import Qt, QMimeData
from script import analyze_pixel_intensity


class Client(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Viewer")
        self.setGeometry(200, 200, 400, 400)

        self.label = QLabel("Drop Image Here", self)
        self.label.setAlignment(Qt.AlignCenter)

        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(10)
        self.button_layout.addStretch()

        multiplication_button = QPushButton("×")
        division_button = QPushButton("÷")
        self.button_layout.addWidget(multiplication_button)
        self.button_layout.addWidget(division_button)
        self.button_layout.addStretch()

        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText("Enter numbers here")
        self.text_input.setVisible(False)
        self.button_widget = QWidget()
        self.button_widget.setLayout(self.button_layout)
        self.button_widget.setVisible(False)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button_widget)
        layout.addWidget(self.text_input)

        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.setAcceptDrops(True)

        multiplication_button.clicked.connect(self.multiply)
        division_button.clicked.connect(self.divide)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    file_path = url.toLocalFile()
                    if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                        event.accept()
                        return
        event.ignore()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            event.accept()
            self.file_path = event.mimeData().urls()[0].toLocalFile()
            pixmap = QPixmap(self.file_path)
            self.label.setPixmap(pixmap.scaled(self.label.size(), Qt.AspectRatioMode.KeepAspectRatio))
            self.label.setText("")
            self.button_widget.setVisible(True)
            self.text_input.setVisible(True)
        else:
            event.ignore()

    def multiply(self):
        if self.text_input.text().strip():
            # Perform multiplication operation here
            number = str(self.text_input.text())
            result = analyze_pixel_intensity(self.file_path, "*", number)
            QMessageBox.warning(self, "Success", f"{result}.")
        else:
            QMessageBox.warning(self, "Input Required", "Please enter a number.")

    def divide(self):
        if self.text_input.text().strip():
            # Perform division operation here
            number = str(self.text_input.text())
            result = analyze_pixel_intensity(self.file_path, "/", number)
            QMessageBox.warning(self, "Success", f"{result}.")
        else:
            QMessageBox.warning(self, "Input Required", "Please enter a number.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Client()
    window.show()
    sys.exit(app.exec_())