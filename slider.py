import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QSlider, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class ImageSliderApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Slider App")
        self.setGeometry(1080, 1080, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Scroll Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Load Image
        self.image_label = QLabel(self)
        self.image_label.setScaledContents(True)  # Resize image to fit label
        self.load_image("output.png")  # Put the path of your image here

        self.layout.addWidget(self.scroll_area)
        self.scroll_area.setWidget(self.image_label)

    def load_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap)

    def slider_changed(self, value):
        # Adjust image according to slider value
        pass  # You need to implement the adjustment based on your specific use case


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageSliderApp()
    window.show()
    sys.exit(app.exec_())