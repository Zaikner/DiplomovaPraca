import sys

from PyQt5.QtWidgets import QApplication

from DiplomovaPraca.Configuration import Configuration
from DiplomovaPraca.ConversionPipeline import ConversionPipeline
from DiplomovaPraca.Evaluator import Evaluator
from DiplomovaPraca.utilities import readFile
from MainWindow import MainWindow

app = QApplication(sys.argv)
MainWindow = MainWindow()
MainWindow.show()
#pipe = ConversionPipeline(('').join(readFile('Dataset/UseCase0.txt')),conf)
#Evalute().evaluate("Dataset/PlantUml0F.txt","output.puml")

sys.exit(app.exec_())

