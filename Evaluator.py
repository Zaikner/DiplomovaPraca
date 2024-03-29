import time
from datetime import datetime
from sklearn.metrics import f1_score
import spacy
import itertools
from DiplomovaPraca.Configuration import Configuration
from DiplomovaPraca.ConversionPipeline import ConversionPipeline
from DiplomovaPraca.Evaluate import Evaluate
from DiplomovaPraca.utilities import readFile


class Evaluator:
    lastMetadata = {}

    def evaluate_all_metrics(self, source):
        f1 = Evaluate().evaluate_messages(source, "output.puml")
        f2 = Evaluate().evaluate_life_lines(source, "output.puml")
        f3 = Evaluate().evaluate_whole_words(source, "output.puml")
        f4 = Evaluate().evaluate_syntax_similarity(source, "output.puml")
        print('source:'+str(source))
        print('Messages F1 score was: ' + str(f1))
        print('Life lines F1 score was: ' + str(f2))
        print('Whole F1 score was: ' + str(f3))
        print('Text similarity F1 score was: ' + str(f4))
        return [f1, f2, f3, f4]

    def evaluate_everything(self, text, target, project=False, steps=False):
        self.purge_meta_data()
        project_options = [False, project]
        coreference_options = [True, False]
        step_options = [False, steps]
        engine_options = ['spacy', 'stanza']
        mode_options = ['POS', 'DP']
        models_options = ["en_core_web_lg", "en_core_web_md", "en_core_web_sm"]
        processor_options_spacy = self.make_all_combinations(["tagger", "parser", "lemmatizer"])
        processor_options_stanza = self.make_all_combinations(['tokenize', 'mwt', 'pos', 'lemma', 'depparse'])

        for e in engine_options:
            if e == 'spacy':
                processor_options = processor_options_spacy
                processor_options = [['all']]
            else:
                processor_options = processor_options_stanza
            for model in models_options:
                for processors in processor_options:
                    for c in coreference_options:
                        for s in step_options:
                            for p in project_options:
                                for m in mode_options:
                                    conf = Configuration()
                                    conf.engine = e
                                    conf.mode = m
                                    conf.coreference = c
                                    conf.steps = s
                                    conf.project = p
                                    conf.processors = processors
                                    conf.model = model

                                    res = ConversionPipeline(('').join(text), conf)
                                    self.lastMetadata['Date'] = datetime.now()
                                    self.lastMetadata['project'] = p
                                    self.lastMetadata['coreference'] = c
                                    self.lastMetadata['step'] = s
                                    self.lastMetadata['engine'] = e
                                    self.lastMetadata['mode'] = m
                                    self.lastMetadata['processors'] = processors
                                    self.lastMetadata['model'] = model
                                    if (res == False):
                                        self.lastMetadata['success'] = False
                                    else:
                                        self.lastMetadata['success'] = True

                                        results = self.evaluate_all_metrics(target)

                                        self.lastMetadata['results_messages'] = results[0]
                                        self.lastMetadata['results_lifelines'] = results[1]
                                        self.lastMetadata['results_whole'] = results[2]
                                        self.lastMetadata['results_similarity'] = results[3]

                                    self.write_meta_data()
                                    if m is 'DP':
                                        return

    def write_meta_data(self):
        with open('metaData.txt', 'a') as file:
            file.write('\n')
            file.write('\n')
            file.write('\n')
            file.write("Date: " + str(self.lastMetadata['Date']) + '\n')
            file.write("Project present: " + str(self.lastMetadata['project']) + '\n')
            file.write("Coreference enabled: " + str(self.lastMetadata['coreference']) + '\n')
            file.write("Step enabled: " + str(self.lastMetadata['step']) + '\n')
            file.write("NLP engine: " + str(self.lastMetadata['engine']) + '\n')
            file.write("Model: " + str(self.lastMetadata['model']) + '\n')
            file.write('Processor options: [' + ", ".join(self.lastMetadata['processors']) + ']\n')
            file.write("Pipeline method: " + str(self.lastMetadata['mode']) + '\n')

            if (self.lastMetadata['success'] != False):
                file.write('Messages F1 score: ' + str(self.lastMetadata['results_messages']) + '\n')
                file.write('Life lines F1 score: ' + str(self.lastMetadata['results_lifelines']) + '\n')
                file.write('Whole F1 score: ' + str(self.lastMetadata['results_whole']) + '\n')
                file.write('Text similarity F1 score: ' + str(self.lastMetadata['results_similarity']) + '\n')
            else:
                file.write('Run of this configuration was not successful')

    def purge_meta_data(self):
        with open('metaData.txt', 'w') as file:
            print('Metadata purged')

    def make_all_combinations(self, options):
        combinations = []
        for i in range(len(options), 0, -1):
            [combinations.append(j) for j in itertools.combinations(options, i)]

        return combinations
