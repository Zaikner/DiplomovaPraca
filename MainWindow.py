import sys
import tkinter as tk

from PyQt5.QtCore import QTimer, Qt, QEventLoop
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QTextEdit, QCheckBox, \
    QMainWindow, QScrollBar, QScrollArea

from DiplomovaPraca.Configuration import Configuration
from DiplomovaPraca.ConversionPipeline import ConversionPipeline
from DiplomovaPraca.DiagramWindow import DiagramWindow
from DiplomovaPraca.Drawer import Drawer
from DiplomovaPraca.ErrorWindow import ErrorWindow
from DiplomovaPraca.ProjectDictionary import ProjectDictionary
from DiplomovaPraca.StepWindow import StepWindow
from DiplomovaPraca.utilities import readFile, readFilePlain


class MainWindow(QScrollArea):
    def __init__(self):
        super().__init__()
        self.stop = None
        self.conf = Configuration()
        self.start = True
        self.setWindowTitle("Transform Use Case to UML")
        self.move(0, 0)
        self.resize(1100, 1100)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        # Create widgets
        self.labelUseCase = QLabel("Enter the use case:.", self)
        self.labelUseCase.setFont(QFont("Arial", 13, QFont.Bold))
        self.labelUseCase.setStyleSheet("color: blue; background-color: lightgray")
        self.useCase = QTextEdit(self)
        self.useCase.insertPlainText(''.join(readFilePlain('Dataset/UseCase0.txt')))
        self.projectSubject = QLineEdit(self)
        self.projectSubject.setMaxLength(200)
        # TODO:urobit to tak, ze ak je prazdne tak placehorder
        self.projectSubject.setText("(1:[example]);(2:[other_example])")
        self.projectObject = QLineEdit(self)
        self.projectObject.setMaxLength(200)
        self.projectObject.setText("(1:[example1, example2]);(2:[other_example])")
        self.projectRelation = QLineEdit(self)
        self.projectRelation.setMaxLength(200)
        self.projectRelation.setText("(1:[example]);(2:[other_example])")
        self.projectSubjectLabel = QLabel("Enter dictionary subjects:",self)
        self.projectSubjectLabel.setFont(QFont("Arial", 13, QFont.Bold))
        self.projectSubjectLabel.setStyleSheet("color: blue; background-color: lightgray")
        self.projectSubjectLabel.hide()
        self.projectSubject.hide()

        self.projectObjectLabel = QLabel("Enter dictionary objects:", self)
        self.projectObjectLabel.setFont(QFont("Arial", 13, QFont.Bold))
        self.projectObjectLabel.setStyleSheet("color: blue; background-color: lightgray")
        self.projectObjectLabel.hide()
        self.projectObject.hide()

        self.projectRelationLabel = QLabel("Enter dictionary relations:", self)
        self.projectRelationLabel.setFont(QFont("Arial", 13, QFont.Bold))
        self.projectRelationLabel.setStyleSheet("color: blue; background-color: lightgray")
        self.projectRelationLabel.hide()
        self.projectRelation.hide()

        # self.systemEdit = QLineEdit(self)
        # self.systemEdit.setText("System")
        # self.systemLabel = QLabel("Enter system name(ATM machine, Delivery application,etc..):", self)
        # self.systemLabel.setFont(QFont("Arial", 13, QFont.Bold))
        # self.systemLabel.setStyleSheet("color: blue; background-color: lightgray")

        # self.textOutput = QTextEdit(self)
        # self.textOutput.setReadOnly(True)

        # self.labelTextOutput = QLabel("Text output:", self)
        # self.labelTextOutput.setFont(QFont("Arial", 13, QFont.Bold))
        # self.labelTextOutput.setStyleSheet("color: blue; background-color: lightgray")

        self.labelFragmentPattern = QLabel("Fragment patterns:", self)
        self.labelFragmentPattern.setFont(QFont("Arial", 13, QFont.Bold))
        self.labelFragmentPattern.setStyleSheet("color: blue; background-color: lightgray")
        self.labelFragmentPattern.hide()
        self.fragmentPattern  = QLineEdit(self)
        self.fragmentPattern.setMaxLength(200)
        self.fragmentPattern.setText("LOOP:[For each...do];OPT:[IF...then, In case of...then];ALT:[IF...otherwise];PAR:[simultaneously];")
        self.fragmentPattern.hide()
        self.labelDiagramOutput = QLabel("Diagram output:", self)
        self.labelDiagramLoading = QLabel("Diagram is being created...:", self)
        self.labelDiagramLoading.setFont(QFont("Arial", 13, QFont.Bold))
        self.labelDiagramLoading.setStyleSheet("color: Red; background-color: lightgray")
        self.labelDiagramLoading.hide()
        self.labelDiagramError = QLabel("Diagram is being created...:", self)
        self.labelDiagramError.setFont(QFont("Arial", 13, QFont.Bold))
        self.labelDiagramError.setStyleSheet("color: Red; background-color: lightgray")
        self.labelDiagramError.hide()
        self.labelOpt1 = QLabel("", self)
        self.labelOpt1.setFont(QFont("Arial", 13, QFont.Bold))
        self.labelOpt1.setStyleSheet("color: Red; background-color: lightgray")
        self.labelOpt1.hide()
        self.labelOpt2 = QLabel("", self)
        self.labelOpt2.setFont(QFont("Arial", 13, QFont.Bold))
        self.labelOpt2.setStyleSheet("color: Red; background-color: lightgray")
        self.labelOpt2.hide()
        self.labelDiagramOutput.setFont(QFont("Arial", 13, QFont.Bold))
        self.labelDiagramOutput.setStyleSheet("color: blue; background-color: lightgray")
        self.transform_button = QPushButton("Transform to UML", self)
        self.transform_button.clicked.connect(self.start_pipeline)

        self.patternLabel = QLabel("Used software pattern:", self)
        self.patternLabel.setFont(QFont("Arial", 13, QFont.Bold))
        self.patternLabel.setStyleSheet("color: blue; background-color: lightgray")

        self.noPatternBox = QCheckBox('No pattern')
        self.noPatternBox.setChecked(True)
        self.noPatternBox.stateChanged.connect(self.noPattern)

        self.mvcPatternBox = QCheckBox('MVC pattern')
        self.mvcPatternBox.stateChanged.connect(self.mvc)
        # Create a QLabel widget and set the pixmap as its content
        self.diagram = QLabel(self)

        self.modeLabel = QLabel("NLP method:", self)
        self.modeLabel.setFont(QFont("Arial", 13, QFont.Bold))
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
        self.libLabel.setFont(QFont("Arial", 13, QFont.Bold))
        self.libLabel.setStyleSheet("color: blue; background-color: lightgray")
        self.stanzaCheckBox = QCheckBox('Stanza')
        self.spacyCheckBox = QCheckBox('Spacy')
        self.spacyCheckBox.setChecked(True)
        self.spacyCheckBox.stateChanged.connect(self.spacy_checkbox)
        self.stanzaCheckBox.stateChanged.connect(self.stanza_checkbox)
        self.conf.engine = 'spacy'


        self.otherLabel = QLabel("Other options:", self)
        self.otherLabel.setFont(QFont("Arial", 13, QFont.Bold))
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
        self.parametersCheckBox = QCheckBox('Enable parameters in function calls')
        self.parametersCheckBox.stateChanged.connect(self.set_parameters)
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
        mainlayout = QVBoxLayout(self)

        mainlayout.addWidget(self.scroll_area)
        layoutWidget = QWidget(self)
        layoutWidget.setLayout(layout)
        self.scroll_area.setWidget(layoutWidget)
        self.scroll_area.resize(1080,1080)
        layout.addWidget(self.modeLabel)
        layout.addWidget(self.posCheckBox)
        layout.addWidget(self.dpCheckBox)
        layout.addWidget(self.oieCheckBox)
        layout.addWidget(self.libLabel)
        layout.addWidget(self.stanzaCheckBox)
        layout.addWidget(self.spacyCheckBox)

        layout.addWidget(self.otherLabel)
        layout.addWidget(self.stepsCheckBox)
        layout.addWidget(self.coreferenceCheckBox)
        layout.addWidget(self.parametersCheckBox)
        layout.addWidget(self.fragmentsCheckBox)
        layout.addWidget(self.fragmentsKeywordsCheckBox)
        layout.addWidget(self.projectCheckBox)
        layout.addWidget(self.projectSubjectLabel)
        layout.addWidget(self.projectSubject)
        layout.addWidget(self.projectRelationLabel)
        layout.addWidget(self.projectRelation)
        layout.addWidget(self.projectObjectLabel)
        layout.addWidget(self.projectObject)
        layout.addWidget(self.patternLabel)
        layout.addWidget(self.noPatternBox)
        layout.addWidget(self.mvcPatternBox)
        layout.addWidget(self.labelFragmentPattern)
        layout.addWidget(self.fragmentPattern)
        # layout.addWidget(self.systemLabel)
        # layout.addWidget(self.systemEdit)
        layout.addWidget(self.labelUseCase)
        layout.addWidget(self.useCase)
        layout.addWidget(self.transform_button)
        # layout.addWidget(self.labelTextOutput)
        # layout.addWidget(self.textOutput)
        layout.addWidget(self.labelDiagramOutput)
        layout.addWidget(self.diagram)
        layout.addWidget(self.labelDiagramLoading)
        layout.addWidget(self.labelDiagramError)
        layout.addWidget(self.labelOpt1)
        layout.addWidget(self.labelOpt2)

        self.setWidget(self.scroll_area)
    def set_project(self,state):
        # Handle checkbox state change
        if state == 2:  # Checked state
            self.conf.project = True
            self.projectObject.show()
            self.projectObjectLabel.show()
            self.projectSubject.show()
            self.projectSubjectLabel.show()
            self.projectRelation.show()
            self.projectRelationLabel.show()

        else:  # Unchecked state
            self.conf.project = None
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
        #     self.labelDiagramOutput.show()
            self.diagram.hide()
            self.labelDiagramError.hide()
            self.labelOpt1.hide()
            self.labelOpt2.hide()
            self.labelDiagramLoading.show()
            # self.conf.system = self.systemEdit.text().strip()
            print(self.useCase.toPlainText())
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.pipe)  # Connect the timeout signal to the function
            self.timer.start(500)  # Timer fires after 2000 milliseconds (2 seconds)


    def mvc(self,state):
        if state == 2:
            self.conf.pattern = 'mvc'
            self.noPatternBox.setChecked(False)
        else:
            self.conf.pattern = None

    def noPattern(self,state):
        if state == 2:
            self.conf.pattern = None
            self.mvcPatternBox.setChecked(False)
        else:
            self.conf.pattern = 'mvc'

    def stanza_checkbox(self,state):
        if state == 2:
            self.conf.engine = 'stanza'
            self.spacyCheckBox.setChecked(False)

        # self.stanzaCheckBox.setCheckState(Qt.Checked)



    def spacy_checkbox(self,state):
        if state == 2:
            self.conf.engine = 'spacy'
            self.stanzaCheckBox.setChecked(False)


    def set_parameters(self,state):
        self.conf.parameters = not self.conf.parameters

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
        self.conf.coreference = not self.conf.coreference

    def fragment_checkbox(self,state):
        self.conf.fragments = not self.conf.fragments

    def fragment_keywords_checkbox(self, state):
        if state == 2:
            self.fragmentPattern.show()
            self.labelFragmentPattern.show()
        else:
            self.fragmentPattern.hide()
            self.labelFragmentPattern.hide()
        # self.conf.keywords = not  self.conf.keywords


    def steps_checkbox(self,state):
        self.conf.steps = not  self.conf.steps

    def project_text(self):
        return

    def pipe(self):
        i = 0
        self.exit = False
        self.original = []
        sp = self.useCase.toPlainText().lower().split('\n')
        while i < 50 and i < len(sp) and sp[i]!='':
            l = sp[i]
            i+=1
            try:
                if int(l.strip()[:l.find('.')]) != i:
                    self.exit = True

                    self.labelDiagramError.setText(
                        'Invalid sentence numbering! Readjust numbering. Make it in order with no number left out or duplicated.')
                    self.labelDiagramLoading.hide()

                    self.labelDiagramError.show()
            except:
                self.exit = True

                self.labelDiagramError.setText(
                    'Invalid sentence numbering! Readjust numbering. Make it in order with no number left out or duplicated.')
                self.labelDiagramLoading.hide()

                self.labelDiagramError.show()
            sent = l.strip()[l.find('.')+1:]
            if len(sent) > 100:
                sent = sent[:100]
            self.original.append(sent)
        # self.original = [l.strip()[l.find('.')+1:] for l in self.useCase.toPlainText().split('\n')]
        self.text = ''.join(self.original)

        #TODO:Kontrola vstupov
        print('Kontrola zacala')
        if self.fragmentsKeywordsCheckBox.isChecked() and self.fragmentPattern.text().strip()!='':
            if ':' not in self.fragmentPattern.text() or self.fragmentPattern.text().count(':') != (self.fragmentPattern.text().count(';')):
                self.exit = True
                self.labelDiagramError.setText('Invalid fragment pattern. Valid fragment is LOOP/ALT/PAR/OPT:[pattern1,patter2 first part .. pattern2 second part];')
                self.labelDiagramLoading.hide()

                self.labelDiagramError.show()
        self.conf.fragmentPattern = {}
        if self.fragmentsKeywordsCheckBox.isChecked():
            self.all_posible_fragments = ['alt', 'opt', 'par', 'loop']
            possibilities = self.fragmentPattern.text().split(';')
            for pos in possibilities[:-1]:
                print(possibilities)
                print(self.fragmentPattern.text().split())
                pair = pos.split(':')
                if pair[0].lower() not in self.all_posible_fragments and not self.exit:
                    self.exit = True
                    self.labelDiagramError.setText("Invalid loop definition: " + pair[0]+' Valid pattern is LOOP/ALT/PAR/OPT:[pattern1,patter2 first part .. pattern2 second part];')
                    self.labelDiagramLoading.hide()

                    self.labelDiagramError.show()
                elif not self.exit:
                    if self.conf.fragmentPattern is None:
                        self.conf.fragmentPattern = {}
                    self.conf.fragmentPattern[pair[0]] = pair[1][1:-1].split(',')


        print('Kontrola presla')
        if self.conf.mode != '' and self.start and self.text != '' and not self.exit:
            self.diagram.hide()
            if self.conf.project is not None:
                self.init_project()


            self.start = False

            if (self.conf.steps):
                sol = {}
                sol['fragments'] = []
                i = 0
                self.stop = False
                for sentence in self.original:
                    if sentence != '' and not self.stop:
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
                        self.stop = self.step_window.quit
                        if not self.stop:
                            sol[i]['objects'] = self.step_window.option['objects']
                            sol[i]['subjects'] = self.step_window.option['subjects']
                            sol[i]['relations'] = self.step_window.option['relations']
                            # TODO: error handling with steps
                            self.errorMess = ['',0,'']
                self.step_window.hide()
                if not self.stop and len(self.conf.users.items()) != 0:
                    d = Drawer(sol,self.conf)
                    d.create_PlantUml()
                else:
                    self.errorMess = ['stepping error',0,0]
            else:
                self.errorMess = ConversionPipeline(('').join(self.text), self.conf).run()
            if len(self.conf.users.items()) == 0:
                self.labelDiagramError.setText("No human user recognized")
                self.labelDiagramLoading.hide()
                print(self.errorMess)
                self.labelDiagramError.show()
            elif self.errorMess[0] == 'stepping error':
                self.labelDiagramError.setText("During stepping has occured error")
                self.labelDiagramLoading.hide()
                print(self.errorMess)
                self.labelDiagramError.show()
            elif self.errorMess[0] == 'subject error':
                self.labelDiagramError.setText('No subject was created at sentence number '+str(self.errorMess[1]))
                self.labelOpt1.setText('Relation:'+str(self.errorMess[2]['relations']))
                self.labelOpt2.setText('Objects:' + str(self.errorMess[2]['objects']))
                self.labelOpt1.show()
                self.labelOpt2.show()
                self.labelDiagramLoading.hide()
                print(self.errorMess)
                self.labelDiagramError.show()
            elif self.errorMess[0] == 'object error':
                self.labelDiagramError.setText('No object was created at sentence number ' +str(self.errorMess[1]))
                print(self.errorMess)
                self.labelOpt1.setText('Subjects:' + str(self.errorMess[2]['subjects']))
                self.labelOpt2.setText('Relation:' + str(self.errorMess[2]['relations']))
                self.labelOpt1.show()
                self.labelOpt2.show()
                self.labelDiagramLoading.hide()
                self.labelDiagramError.show()
            elif self.errorMess[0] == 'relation error':
                self.labelDiagramError.setText('No relation was created at sentence number '+str(self.errorMess[1]))
                self.labelOpt1.setText('Subjects:' + str(self.errorMess[2]['subjects']))
                self.labelOpt2.setText('Objects:' + str(self.errorMess[2]['objects']))
                self.labelOpt1.show()
                self.labelOpt2.show()
                self.labelDiagramLoading.hide()
                print(self.errorMess)
                self.labelDiagramError.show()
            else:
                self.labelDiagramLoading.hide()
                print("vytlacil")
                self.diagramWindow = DiagramWindow()
                self.diagramWindow.show_diagram()
                # self.diagram.setPixmap(QPixmap("output.png"))
                # self.diagram.show()

            self.text = ''
            self.start = True
        elif(self.text == '' and not self.exit):
            self.error1 = ErrorWindow()
            self.error1.error('Use case is empty')
        elif(self.start == False and not self.exit):
            self.error2 = ErrorWindow()
            self.error2.error('Previous pipeline is running')
        elif (self.conf.mode =='' and not self.exit):
            print('Tu to vypol')
            print(self.text)
            print(self.start)
            print(self.conf.mode)
            self.error3 = ErrorWindow()
            self.error3.error('NLP method was not set')
        elif (self.conf.engine == '' and not self.exit):
            self.error4 = ErrorWindow()
            self.error4.error('NLP library was not set')
        self.timer.stop()
        self.conf.users = {}
        self.conf.project = None
        self.conf.fragmentsKeywords = None

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
