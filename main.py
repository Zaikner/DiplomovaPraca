from DiplomovaPraca.Configuration import Configuration
from DiplomovaPraca.ConversionPipeline import ConversionPipeline
from DiplomovaPraca.Evaluator import Evaluator
from DiplomovaPraca.utilities import readFile


conf = Configuration()
conf.engine = 'spacy'
conf.mode = 'DP'
conf.coreference = True
conf.mode = 'POS'
#pipe = ConversionPipeline(('').join(readFile('Dataset/UseCase0.txt')),conf)
#Evalute().evaluate("Dataset/PlantUml0F.txt","output.puml")
Evaluator().evaluate_everything('Dataset/UseCase0.txt',"Dataset/PlantUml0F.txt")
