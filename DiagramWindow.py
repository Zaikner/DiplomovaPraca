from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QPushButton, QCheckBox, QLabel, QVBoxLayout, QWidget, QMainWindow, QDialog, QScrollBar, \
    QScrollArea
from PyQt5.QtCore import QTimer, Qt, QEventLoop

class DiagramWindow(QDialog):
    def __init__(self):
        super(DiagramWindow, self).__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setWindowTitle('Diagram window')
        self.resize(1080, 1080)
        self.option = ''
        self.show()

    def show_diagram(self):

        # Scroll Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Load Image
        self.image_label = QLabel(self)
        # self.image_label.setScaledContents(True)  # Resize image to fit label
        self.load_image("output.png")  # Put the path of your image here
        # self.diagram = QLabel(self)
        self.labelDiagramOutput = QLabel("Diagram output:", self)
        self.labelDiagramOutput.setFont(QFont("Arial", 13, QFont.Bold))
        self.labelDiagramOutput.setStyleSheet("color: blue; background-color: lightgray")
        # self.diagram.setPixmap(QPixmap("output.png"))
        # self.diagram.show()
        # self.layout.addWidget(self.labelDiagramOutput)
        # self.layout.addWidget(self.diagram)


        self.button_close = QPushButton("Close window", self)
        self.button_close.clicked.connect(self.closeWindow)
        self.button_close.setFont(QFont("Arial", 13, QFont.Bold))
        self.button_close.setStyleSheet("background: red; color:white;")
        self.layout.addWidget(self.scroll_area)
        self.scroll_area.setWidget(self.image_label)
        self.layout.addWidget(self.button_close)


        self.show()

    def scrollValueChanged(self, value):
        print("Scroll value changed:", value)
    def load_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap)

    def closeEvent(self, event):
        event.ignore()  # Ignore the close event

    def closeWindow(self,state):
        self.destroy()
