import sys
import tkinter as tk

from PyQt5.QtCore import QTimer, Qt, QEventLoop
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QTextEdit, QCheckBox, \
    QMainWindow

from DiplomovaPraca.Configuration import Configuration
from DiplomovaPraca.ConversionPipeline import ConversionPipeline
from DiplomovaPraca.Drawer import Drawer
from DiplomovaPraca.ErrorWindow import ErrorWindow
from DiplomovaPraca.ProjectDictionary import ProjectDictionary
from DiplomovaPraca.StepWindow import StepWindow
from DiplomovaPraca.utilities import readFile, readFilePlain


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.conf = Configuration()
        self.start = True
        self.setWindowTitle("Transform Use Case to UML")
        self.move(0, 0)
        self.resize(1080, 1080)
        # Create widgets
        self.labelUseCase = QLabel("Enter the use case:.", self)
        self.labelUseCase.setFont(QFont("Arial", 16, QFont.Bold))
        self.labelUseCase.setStyleSheet("color: blue; background-color: lightgray")

        self.useCase = QTextEdit(self)
        self.useCase.insertPlainText(''.join(readFilePlain('Dataset/UseCase0.txt')))
        self.projectSubject = QLineEdit(self)
        # TODO:urobit to tak, ze ak je prazdne tak placehorder
        self.projectSubject.setText("(1:[example]);(2:[other_example])")
        self.projectObject = QLineEdit(self)
        self.projectObject.setText("(1:[example1, example2]);(2:[other_example])")
        self.projectRelation = QLineEdit(self)
        self.projectRelation.setText("(1:[example]);(2:[other_example])")
        self.projectSubjectLabel = QLabel("Enter dictionary subjects:",self)
        self.projectSubjectLabel.setFont(QFont("Arial", 16, QFont.Bold))
        self.projectSubjectLabel.setStyleSheet("color: blue; background-color: lightgray")
        self.projectSubjectLabel.hide()
        self.projectSubject.hide()

        self.projectObjectLabel = QLabel("Enter dictionary objects:", self)
        self.projectObjectLabel.setFont(QFont("Arial", 16, QFont.Bold))
        self.projectObjectLabel.setStyleSheet("color: blue; background-color: lightgray")
        self.projectObjectLabel.hide()
        self.projectObject.hide()

        self.projectRelationLabel = QLabel("Enter dictionary relations:", self)
        self.projectRelationLabel.setFont(QFont("Arial", 16, QFont.Bold))
        self.projectRelationLabel.setStyleSheet("color: blue; background-color: lightgray")
        self.projectRelationLabel.hide()
        self.projectRelation.hide()

        # self.textOutput = QTextEdit(self)
        # self.textOutput.setReadOnly(True)

        # self.labelTextOutput = QLabel("Text output:", self)
        # self.labelTextOutput.setFont(QFont("Arial", 16, QFont.Bold))
        # self.labelTextOutput.setStyleSheet("color: blue; background-color: lightgray")

        self.labelDiagramOutput = QLabel("Diagram output:", self)
        self.labelDiagramLoading = QLabel("Diagram is being created...:", self)
        self.labelDiagramLoading.hide()
        self.labelDiagramOutput.setFont(QFont("Arial", 16, QFont.Bold))
        self.labelDiagramOutput.setStyleSheet("color: blue; background-color: lightgray")
        self.transform_button = QPushButton("Transform to UML", self)
        self.transform_button.clicked.connect(self.start_pipeline)


        # Create a QLabel widget and set the pixmap as its content
        self.diagram = QLabel(self)

        self.modeLabel = QLabel("NLP method:", self)
        self.modeLabel.setFont(QFont("Arial", 16, QFont.Bold))
        self.modeLabel.setStyleSheet("color: blue; background-color: lightgray")
        self.posCheckBox = QCheckBox('Part of speech')
        self.posCheckBox.setChecked(True)
        self.conf.mode = 'POS'
        self.oieCheckBox = QCheckBox('Open information extraction')
        self.dpCheckBox = QCheckBox('Dependency parsing')
        self.dpCheckBox.stateChanged.connect(self.dp_checkbox)
        self.posCheckBox.stateChanged.connect(self.pos_checkbox)
        self.oieCheckBox.stateChanged.connect(self.oie_checkbox)

        self.libLabel = QLabel("NLP library:", self)
        self.libLabel.setFont(QFont("Arial", 16, QFont.Bold))
        self.libLabel.setStyleSheet("color: blue; background-color: lightgray")
        self.stanzaCheckBox = QCheckBox('Stanza')
        self.spacyCheckBox = QCheckBox('Spacy')
        self.spacyCheckBox.setChecked(True)
        self.spacyCheckBox.stateChanged.connect(self.spacy_checkbox)
        self.stanzaCheckBox.stateChanged.connect(self.stanza_checkbox)
        self.conf.engine = 'spacy'


        self.otherLabel = QLabel("Other options:", self)
        self.otherLabel.setFont(QFont("Arial", 16, QFont.Bold))
        self.otherLabel.setStyleSheet("color: blue; background-color: lightgray")
        self.stepsCheckBox = QCheckBox('Enable stepping')
        self.stepsCheckBox.stateChanged.connect(self.steps_checkbox)
        self.coreferenceCheckBox = QCheckBox('Coreferences')
        self.coreferenceCheckBox.stateChanged.connect(self.coreference_checkbox)
        self.fragmentsCheckBox = QCheckBox('Allow fragments automatic detection')
        self.fragmentsCheckBox.stateChanged.connect(self.fragment_checkbox)
        self.fragmentsKeywordsCheckBox = QCheckBox('Allow fragments definition though keywords')
        self.fragmentsKeywordsCheckBox.stateChanged.connect(self.fragment_keywords_checkbox)
        self.projectCheckBox = QCheckBox('Project dictionary')
        self.projectCheckBox.stateChanged.connect(self.set_project)
        #
        #
        #processor_options_spacy = self.make_all_combinations(["tagger", "parser", "lemmatizer"])
        #
        #processor_options_stanza = self.make_all_combinations(['tokenize', 'mwt', 'pos', 'lemma', 'depparse'])

        # !!! doplnit project !!
        # Set up the layout

        # self.labelTextOutput.hide()
        # self.textOutput.hide()
        self.labelDiagramOutput.hide()
        self.diagram.hide()

        layout = QVBoxLayout(self)

        layout.addWidget(self.modeLabel)
        layout.addWidget(self.posCheckBox)
        layout.addWidget(self.oieCheckBox)
        layout.addWidget(self.dpCheckBox)

        layout.addWidget(self.libLabel)
        layout.addWidget(self.stanzaCheckBox)
        layout.addWidget(self.spacyCheckBox)

        layout.addWidget(self.otherLabel)
        layout.addWidget(self.stepsCheckBox)
        layout.addWidget(self.coreferenceCheckBox)
        layout.addWidget(self.fragmentsCheckBox)
        layout.addWidget(self.fragmentsKeywordsCheckBox)
        layout.addWidget(self.projectCheckBox)
        layout.addWidget(self.projectSubjectLabel)
        layout.addWidget(self.projectSubject)
        layout.addWidget(self.projectRelationLabel)
        layout.addWidget(self.projectRelation)
        layout.addWidget(self.projectObjectLabel)
        layout.addWidget(self.projectObject)

        layout.addWidget(self.labelUseCase)
        layout.addWidget(self.useCase)
        layout.addWidget(self.transform_button)
        # layout.addWidget(self.labelTextOutput)
        # layout.addWidget(self.textOutput)
        layout.addWidget(self.labelDiagramOutput)
        layout.addWidget(self.diagram)
        layout.addWidget(self.labelDiagramLoading)

    def set_project(self,state):
        # Handle checkbox state change
        if state == 2:  # Checked state
            self.projectObject.show()
            self.projectObjectLabel.show()
            self.projectSubject.show()
            self.projectSubjectLabel.show()
            self.projectRelation.show()
            self.projectRelationLabel.show()

        else:  # Unchecked state
            self.projectObject.hide()
            self.projectObjectLabel.hide()
            self.projectSubject.hide()
            self.projectSubjectLabel.hide()
            self.projectRelation.hide()
            self.projectRelationLabel.hide()

    def start_pipeline(self):
        # Handle checkbox state change
        #     self.labelTextOutput.show()
        #     self.textOutput.show()
            self.labelDiagramOutput.show()
            self.diagram.show()

            self.labelDiagramLoading.show()
            print(self.useCase.toPlainText())
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.pipe)  # Connect the timeout signal to the function
            self.timer.start(500)  # Timer fires after 2000 milliseconds (2 seconds)




    def stanza_checkbox(self,state):
        if state == 2:
            self.conf.engine = 'stanza'
            self.spacyCheckBox.setChecked(False)
        else:
            self.conf.engine = ''
        # self.stanzaCheckBox.setCheckState(Qt.Checked)



    def spacy_checkbox(self,state):
        if state == 2:
            self.conf.engine = 'spacy'
            self.stanzaCheckBox.setChecked(False)
        else:
            self.conf.engine = ''

    def pos_checkbox(self,state):
        if state == 2:
            self.conf.mode = 'POS'
            self.dpCheckBox.setChecked(False)
            self.oieCheckBox.setChecked(False)
        # else:
        #     self.conf.mode = ''

    def dp_checkbox(self,state):
        if state == 2:
            self.conf.mode = 'DP'
            print('prepol na dp')
            self.posCheckBox.setChecked(False)
            self.oieCheckBox.setChecked(False)
        # else:
        #     print('rovno aj vypol')
        #     self.conf.mode = ''



    def oie_checkbox(self,state):
        if state == 2:
            self.conf.mode = 'OIE'
            self.dpCheckBox.setChecked(False)
            self.posCheckBox.setChecked(False)
        # else:
        #     self.conf.mode = ''



    def coreference_checkbox(self,state):
        if state == 2:
            self.conf.coreference = True
        else:
            self.conf.coreference = False

    def fragment_checkbox(self,state):
        if state == 2:
            self.conf.fragments = True
        else:
            self.conf.fragments = False

    def fragment_keywords_checkbox(self, state):
        if state == 2:
            self.conf.keywords = True
        else:
            self.conf.keywords = False



    def steps_checkbox(self,state):
        if state == 2:
            self.conf.steps = True
        else:
            self.conf.steps = False

    def project_text(self):
        return




    def pipe(self):
        self.original = [l.strip()[l.find('.')+1:] for l in self.useCase.toPlainText().split('\n')]
        self.text = ''.join(self.original)
        if self.conf.mode != '' and self.start and self.text != '':
            self.init_project()
            print(self.conf.project.list_all_subjects())
            print(self.conf.project.list_all_objects())
            print(self.conf.project.list_all_relations())
            self.start = False
            self.diagram.hide()
            # self.textOutput.insertPlainText('Diagram is being created!\n')
            # self.textOutput.insertPlainText('Conversion pipeline run with following configuration:\n')
            # self.textOutput.insertPlainText('\nProject: ' + self.conf.project.print_project())
            # self.textOutput.insertPlainText('\nCoreference: ' + str(self.conf.coreference))
            # self.textOutput.insertPlainText('\nSteps: ' + str(self.conf.steps))
            # self.textOutput.insertPlainText('\nNLP engine: ' + str(self.conf.engine))
            # self.textOutput.insertPlainText('\nProcessors: [' + ", ".join(self.conf.processors) + ']')
            # self.textOutput.insertPlainText('\nMode: ' + str(self.conf.mode))
            # self.textOutput.insertPlainText('\nEnable fragments: ' + str(self.conf.fragments))
            # self.textOutput.repaint()
            if (self.conf.steps):
                sol = {}
                sol['fragments'] = []
                i = 0
                for sentence in self.original:
                    if sentence != '':
                        i+=1;
                        original = self.conf.mode
                        self.conf.mode = 'POS';
                        pos = ConversionPipeline(sentence, self.conf).run_without_steps()
                        # TODO:OIE
                        # self.conf.mode = 'OIE';
                        # oie = ConversionPipeline(sentence, self.conf).run_without_steps(sentence)
                        oie_message = ''
                        if self.conf.engine == 'spacy':
                            oie_message = 'NOT IMPLEMENTED IN SPACY'
                        else:
                            oie_message = 'NOT IMPLEMENTED YET'
                        self.conf.mode = 'DP'
                        dp = ConversionPipeline(sentence, self.conf).run_without_steps()
                        self.conf.mode = original

                        self.step_window = StepWindow()
                        self.step_window.show()
                        loop = QEventLoop()

                        # Connect the aboutToQuit signal of the second window to exit the loop when it is closed
                        self.step_window.accepted.connect(loop.quit)
                        self.step_window.rejected.connect(loop.quit)
                        sol[i] = {}
                        self.step_window.generate_options(sentence,pos[1],dp[1],oie_message,loop)
                        loop.exec_()
                        sol[i]['objects'] = self.step_window.option['objects']
                        sol[i]['subjects'] = self.step_window.option['subjects']
                        sol[i]['relations'] = self.step_window.option['relations']
                self.step_window.hide()
                d = Drawer(sol)
                d.create_PlantUml()
            else:
                self.start = ConversionPipeline(('').join(self.text), self.conf).run()
            self.text = ''
            self.labelDiagramLoading.hide()
            self.diagram.setPixmap(QPixmap("output.png"))
            self.diagram.show()
        elif(self.text == ''):
            self.error1 = ErrorWindow()
            self.error1.error('Use case is empty')
        elif(self.start == False):
            self.error2 = ErrorWindow()
            self.error2.error('Previous pipeline is running')
        elif (self.conf.mode ==''):
            print('Tu to vypol')
            print(self.text)
            print(self.start)
            print(self.conf.mode)
            self.error3 = ErrorWindow()
            self.error3.error('NLP method was not set')
        elif (self.conf.engine == ''):
            self.error4 = ErrorWindow()
            self.error4.error('NLP library was not set')
        self.timer.stop()

    def init_project(self):
        self.projectDictionary = ProjectDictionary()
        self.projectDictionary.init_sentences(len(self.original))

        items = self.projectObject.text().split(';')
        for item in items:
            number = int(item[1:item.find(':')])
            possibilities = [i.strip() for i in item[item.find(':')+2:len(item)-2].split(',')]
            self.projectDictionary.assign_object_to_sentence(number,possibilities)

        items = self.projectSubject.text().split(';')
        for item in items:
            number = int(item[1:item.find(':')])
            possibilities = [i.strip() for i in item[item.find(':') + 2:len(item) - 2].split(',')]
            self.projectDictionary.assign_subject_to_sentence(number, possibilities)

        items = self.projectRelation.text().split(';')
        for item in items:
            number = int(item[1:item.find(':')])
            possibilities = [i.strip() for i in item[item.find(':') + 2:len(item) - 2].split(',')]
            self.projectDictionary.assign_relation_to_sentence(number, possibilities)

        self.conf.project = self.projectDictionary
