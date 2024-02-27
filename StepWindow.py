from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPushButton, QCheckBox, QLabel, QVBoxLayout, QWidget, QMainWindow, QDialog


class StepWindow(QDialog):
    def __init__(self):
        super(StepWindow, self).__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setWindowTitle('Step window')
        self.resize(300, 300)
        self.option = ''
        self.show()

    def generate_options(self,sentence,pos_option,dp_option,oie_option,loop):
        self.loop = loop
        self.pos_option = pos_option
        self.dp_option = dp_option
        self.oie_option = oie_option
        self.sentence =  QLabel(sentence, self)
        self.sentence.setFont(QFont("Arial", 12, QFont.Bold))
        self.sentence.setStyleSheet("color: blue; background-color: lightgray")
        self.posLabel= QLabel("Part of Speech", self)
        self.posLabel.setFont(QFont("Arial", 10, QFont.Bold))
        self.posLabel.setStyleSheet("color: blue; background-color: lightgray")
        self.posCheckBox = QCheckBox(pos_option['subjects'] + '-->' + pos_option['relations'] + '-->' + pos_option['objects'])
        self.dpLabel = QLabel("Dependency parsing", self)
        self.dpLabel.setFont(QFont("Arial", 10, QFont.Bold))
        self.dpLabel.setStyleSheet("color: blue; background-color: lightgray")
        self.dpCheckBox = QCheckBox(dp_option['subjects'] + '-->' + dp_option['relations'] + '-->' + dp_option['objects'])
        self.oieLabel = QLabel("Open information extraction", self)
        self.oieLabel.setFont(QFont("Arial", 10, QFont.Bold))
        self.oieLabel.setStyleSheet("color: blue; background-color: lightgray")
        self.oieCheckBox = QCheckBox(oie_option)
        if self.oie_option == 'NOT IMPLEMENTED IN SPACY':
            self.oieCheckBox.setCheckable(False)
        # self.choose_button = QPushButton("Confirm your choice", self)
        # self.choose_button.clicked.connect(self.choose)
        self.posCheckBox.stateChanged.connect(self.pos)
        self.dpCheckBox.stateChanged.connect(self.dp)
        self.oieCheckBox.stateChanged.connect(self.oie)


        self.layout.addWidget(self.sentence)
        self.layout.addWidget(self.posLabel)
        self.layout.addWidget(self.posCheckBox)
        self.layout.addWidget(self.dpLabel)
        self.layout.addWidget(self.dpCheckBox)
        self.layout.addWidget(self.oieLabel)
        self.layout.addWidget(self.oieCheckBox)
        # self.layout.addWidget(self.choose_button)

        self.show()

    def pos(self):
        self.option = self.pos_option
        self.loop.quit()



    def oie(self):
        # if self.oie_option != 'NOT IMPLEMENTED IN SPACY':
            self.option = self.oie_option
            self.loop.quit()


    def dp(self):
        self.option = self.dp_option
        self.loop.quit()

