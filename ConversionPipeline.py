from nltk.corpus import wordnet as wn
from stanza.server import CoreNLPClient
import stanza
import requests

from DiplomovaPraca.Drawer import Drawer
import spacy.cli

from DiplomovaPraca.utilities import init_tokens


class ConversionPipeline:

    def __init__(self, text, configuration):
        self.text = text
        self.configuration = configuration
        self.phrases = {}
        self.tokens = init_tokens()

        print('Conversion pipeline run with following configuration:')
        print('Project: '+str(configuration.project))
        print('Coreference: '+str(configuration.coreference))
        print('Steps: '+str(configuration.steps))
        print('NLP engine: ' + str(configuration.engine))
        print('Processors: [' + ", ".join(self.configuration.processors) + ']')
        print('Mode: '+str(configuration.mode))

        if self.configuration.steps:
            res = self.run_with_steps(text)
            if (res!=False):
                d = Drawer(res)
                d.create_PlantUml()

        else:
            res = self.run_without_steps(text)

            if (res != False):
                d = Drawer(res)
                d.create_PlantUml()

    def replace_phrases(self, sentence):
        number_of_phrases = len(self.phrases)
        if sentence.count('\"') % 2 != 0:
            raise 'Number of quotes in sentence is wrong'

        word = ""
        add = False
        for c in sentence:
            if c == '\"' and len(word) == 0:
                add = True
            elif c == '\"' and len(word) != 0:
                add = False
                word += c
                num_of_token = 0
                stop = False
                while not stop and num_of_token <= len(self.tokens):
                    token = self.tokens[num_of_token]
                    if not self.token_is_used(token):
                        self.phrases[token] = word
                        print(word + " was replaced by " + token)
                        stop = True
                    else:
                        num_of_token += 1
                        print(token + " cant be used, because it occurs in text")
                word = ""

            if add:
                word += c

        for token in self.phrases.keys():
            sentence = sentence.replace(self.phrases[token],token)
        print(sentence)
        return sentence

    def replace_tokens(self,sentence):
        for token in self.phrases.keys():
            sentence = sentence.replace(token,self.phrases[token])
        return sentence

    def token_is_used(self, token):
        for key in self.phrases.keys():
            if key == token or token in self.text:
                return True
        return False

    def run_without_steps(self, text):
        print(text)
        sentences = text.strip().split('.')
        if len(sentences[-1]) == 0:
            sentences = sentences[:len(sentences) - 1]
        self.solutions = {}
        num = 0
        for i in range(len(sentences)):
            sentences[i] = self.replace_phrases(sentences[i])

        if self.configuration.engine == 'stanza':

            self.nlp = stanza.Pipeline(lang='en', processors=self.configuration.processors)
            text = ". ".join(sentences)
            doc = self.nlp(text)
            sentences = doc.sentences

        for sentence in sentences:
            result = []
            if self.configuration.engine == 'spacy':
                if self.configuration.processors == ['all']:
                    self.nlp = spacy.load(self.configuration.model)
                else:
                    self.nlp = spacy.load(self.configuration.model, enable=self.configuration.processors)

                if self.configuration.mode == 'POS':
                    result = self.partOfSpeechPipelineSpacy(sentence)
                elif self.configuration.mode == 'DP':
                    result = self.dependencyTreePipelineSpacy(sentence)
                elif self.configuration.mode == 'OIE':
                    return False;

            elif self.configuration.engine == 'stanza':

                if self.configuration.mode == 'POS':
                    result = self.partOfSpeechPipeline(sentence)
                elif self.configuration.mode == 'DP':
                    result = self.dependencyTreePipeline(sentence)
                elif self.configuration.mode == 'OIE':
                    result = self.openInformationExtractionPipeline(sentence)

            else:
                return 'Wrong processor'
            num += 1

            for i in range(1, 4):
                result[i] = self.replace_tokens(result[i]).replace('\"', "")

            self.solutions[num] = {}
            self.solutions[num]['subjects'] = result[1]
            self.solutions[num]['objects'] = result[3]
            self.solutions[num]['relations'] = result[2]

        print('tu to printim')
        print(self.solutions)

        # if (self.configuration.coreference):
        #     #TODO: REFACTOR
        #     all = []
        #     total = 0
        #     self.solveCoReference('subjects')
        #     self.solveCoReference('objects')
        #     self.solveCoReference('relations')
        print('tu to printim zas')
        print(self.solutions)
        return self.solutions

    #     for sentence in sentences:
    #         print(self.partOfSpeechPipelineSpacy(sentence))
    # 
    #     num = 0
    #     self.solutions = {}
    #     for sent in doc.sentences:
    #         num += 1
    #         self.solutions[num] = {}
    #         self.solutions[num]['subjects'] = {}
    #         self.solutions[num]['objects'] = {}
    #         self.solutions[num]['relations'] = {}
    #         if (self.mode in ['all', 'OIE']):
    #             res = self.openInformationExtractionPipeline(sent)
    #             found = False
    #             if self.project != None:
    #                 for sub in self.project.subjects:
    #                     if sub in sentences[num - 1]:
    #                         self.solutions[num]['subjects']['OIE'] = sub
    #                         found = True
    # 
    #             if not found:
    #                 self.solutions[num]['subjects']['OIE'] = res[1]
    # 
    #             found = False
    #             if self.project != None:
    #                 for rel in self.project.relations:
    #                     if rel in sentences[num - 1]:
    #                         self.solutions[num]['relations']['OIE'] = rel
    #                         found = True
    # 
    #             if not found:
    #                 self.solutions[num]['relations']['OIE'] = res[2]
    # 
    #             found = False
    #             if self.project != None:
    #                 for obj in self.project.objects:
    #                     if obj in sentences[num - 1]:
    #                         self.solutions[num]['objects']['OIE'] = obj
    #                         found = True
    # 
    #             if not found:
    #                 self.solutions[num]['objects']['OIE'] = res[3]
    #             resp = 'OIE: ' + self.solutions[num]['subjects']['OIE'] + '-->' + self.solutions[num]['relations'][
    #                 'OIE'] + '-->' + self.solutions[num]['objects']['OIE']
    # 
    #             print(resp)
    #         if (self.mode in ['all', 'DP']):
    #             res = self.dependencyTreePipeline(sent)
    #             found = False
    #             if self.project != None:
    #                 for sub in self.project.subjects:
    #                     if sub in sentences[num - 1]:
    #                         self.solutions[num]['subjects']['Dependency parsing'] = sub
    #                         found = True
    # 
    #             if not found:
    #                 self.solutions[num]['subjects']['Dependency parsing'] = res[1]
    # 
    #             found = False
    #             if self.project != None:
    #                 for rel in self.project.relations:
    #                     if rel in sentences[num - 1]:
    #                         self.solutions[num]['relations']['Dependency parsing'] = rel
    #                         found = True
    # 
    #             if not found:
    #                 self.solutions[num]['relations']['Dependency parsing'] = res[2]
    # 
    #             found = False
    #             if self.project != None:
    #                 for obj in self.project.objects:
    #                     if obj in sentences[num - 1]:
    #                         self.solutions[num]['objects']['Dependency parsing'] = obj
    #                         found = True
    # 
    #             if not found:
    #                 self.solutions[num]['objects']['Dependency parsing'] = res[3]
    # 
    #             resp = 'Dependency parsing: ' + self.solutions[num]['subjects']['Dependency parsing'] + '-->' + \
    #                    self.solutions[num]['relations'][
    #                        'Dependency parsing'] + '-->' + self.solutions[num]['objects']['Dependency parsing']
    # 
    #             print(resp)
    #         if (self.mode in ['all', 'POS']):
    #             res = self.partOfSpeechPipeline(sent)
    #             found = False
    #             if self.project != None:
    #                 for sub in self.project.subjects:
    #                     if sub in sentences[num - 1]:
    #                         self.solutions[num]['subjects']['POS'] = sub
    #                         found = True
    # 
    #             if not found:
    #                 self.solutions[num]['subjects']['POS'] = res[1]
    # 
    #             found = False
    #             if self.project != None:
    #                 for rel in self.project.relations:
    #                     if rel in sentences[num - 1]:
    #                         self.solutions[num]['relations']['POS'] = rel
    #                         found = True
    # 
    #             if not found:
    #                 self.solutions[num]['relations']['POS'] = res[2]
    # 
    #             found = False
    #             if self.project != None:
    #                 for obj in self.project.objects:
    #                     if obj in sentences[num - 1]:
    #                         self.solutions[num]['objects']['POS'] = obj
    #                         found = True
    # 
    #             if not found:
    #                 self.solutions[num]['objects']['POS'] = res[3]
    # 
    #             resp = 'POS: ' + self.solutions[num]['subjects']['POS'] + '-->' + self.solutions[num]['relations'][
    #                 'POS'] + '-->' + self.solutions[num]['objects']['POS']
    #             print(resp)
    # 
    #     print(self.solutions)
    #     if (self.coreference):
    #         all = []
    #         for i in range(1, num + 1):
    #             for j in self.solutions[i]['subjects'].values():
    #                 all.append(j)
    # 
    #         # print('tu')
    #         # print(all)
    #         self.solveCoReference(all)
    # 
    #     return self.solutions
    # 
    # def run_with_steps(self, text):
    #     nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma,depparse')
    #     doc = nlp(text)
    # 
    #     num = 0
    #     self.solutions = {}
    #     for sent in doc.sentences:
    #         num += 1
    #         possibilities = {}
    #         self.solutions[num] = {}
    #         self.solutions[num]['subjects'] = {}
    #         self.solutions[num]['objects'] = {}
    #         self.solutions[num]['relations'] = {}
    #         possibilities['subjects'] = {}
    #         possibilities['objects'] = {}
    #         possibilities['relations'] = {}
    #         if (self.mode in ['all', 'OIE']):
    #             res = self.openInformationExtractionPipeline(sent)
    #             resp = 'OIE : ' + res[1] + '-->' + res[2] + '-->' + res[3]
    #             possibilities['subjects']['OIE'] = res[1]
    #             possibilities['relations']['OIE'] = res[2]
    #             possibilities['objects']['OIE'] = res[3]
    #         if (self.mode in ['all', 'DP']):
    #             res = self.dependencyTreePipeline(sent)
    #             resp = 'Dependency parsing : ' + res[1] + '-->' + res[2] + '-->' + res[3]
    #             possibilities['subjects']['Dependency parsing'] = res[1]
    #             possibilities['relations']['Dependency parsing'] = res[2]
    #             possibilities['objects']['Dependency parsing'] = res[3]
    #         if (self.mode in ['all', 'POS']):
    #             res = self.partOfSpeechPipeline(sent)
    #             resp = 'POS: ' + res[1] + '-->' + res[2] + '-->' + res[3]
    #             possibilities['subjects']['POS'] = res[1]
    #             possibilities['relations']['POS'] = res[2]
    #             possibilities['objects']['POS'] = res[3]
    # 
    #         choice = 0
    # 
    #         while choice not in [1, 2, 3]:
    #             try:
    #                 print('1. ' + possibilities['subjects']['OIE'])
    #                 print('2. ' + possibilities['subjects']['Dependency parsing'])
    #                 print('3. ' + possibilities['subjects']['POS'])
    #                 choice = int(input('Choose your subject, write number of your choice:'))
    #                 if choice not in [1, 2, 3]:
    #                     print('YOU SHOULD WROTE ONE NUMBER 1,2 OR 3 !')
    #             except:
    #                 print('YOU SHOULD WROTE ONE NUMBER 1,2 OR 3 !')
    # 
    #         if (choice == 1):
    #             print('YOU HAVE CHOSEN ' + possibilities['subjects']['OIE'] + ' AS SUBJECT!')
    #             self.solutions[num]['subjects'] = possibilities['subjects']['OIE']
    #         if (choice == 2):
    #             print('YOU HAVE CHOSEN ' + possibilities['subjects']['Dependency parsing'] + ' AS SUBJECT!')
    #             self.solutions[num]['subjects'] = possibilities['subjects']['Dependency parsing']
    #         if (choice == 3):
    #             print('YOU HAVE CHOSEN ' + possibilities['subjects']['POS'] + ' AS SUBJECT!')
    #             self.solutions[num]['subjects'] = possibilities['subjects']['POS']
    #         choice = 0
    #         while choice not in [1, 2, 3]:
    #             try:
    #                 print('1. ' + possibilities['relations']['OIE'])
    #                 print('2. ' + possibilities['relations']['Dependency parsing'])
    #                 print('3. ' + possibilities['relations']['POS'])
    #                 choice = int(input('Choose your relation, write number of your choice:'))
    #                 if choice not in [1, 2, 3]:
    #                     print('YOU SHOULD WROTE ONE NUMBER 1,2 OR 3 !')
    #             except:
    #                 print('YOU SHOULD WROTE ONE NUMBER 1,2 OR 3 !')
    # 
    #         if (choice == 1):
    #             print('YOU HAVE CHOSEN ' + possibilities['relations']['OIE'] + ' AS RELATION!')
    #             self.solutions[num]['relations'] = possibilities['relations']['OIE']
    #         if (choice == 2):
    #             print('YOU HAVE CHOSEN ' + possibilities['relations']['Dependency parsing'] + ' AS RELATION!')
    #             self.solutions[num]['relations'] = possibilities['relations']['Dependency parsing']
    #         if (choice == 3):
    #             print('YOU HAVE CHOSEN ' + possibilities['relations']['POS'] + ' AS RELATION!')
    #             self.solutions[num]['relations'] = possibilities['relations']['POS']
    #         choice = 0
    #         while choice not in [1, 2, 3]:
    #             try:
    #                 print('1. ' + possibilities['objects']['OIE'])
    #                 print('2. ' + possibilities['objects']['Dependency parsing'])
    #                 print('3. ' + possibilities['objects']['POS'])
    #                 choice = int(input('Choose your object, write number of your choice:'))
    #                 if choice not in [1, 2, 3]:
    #                     print('YOU SHOULD WROTE ONE NUMBER 1,2 OR 3 !')
    #             except:
    #                 print('YOU SHOULD WROTE ONE NUMBER 1,2 OR 3 !')
    # 
    #         if (choice == 1):
    #             print('YOU HAVE CHOSEN ' + possibilities['objects']['OIE'] + ' AS OBJECT!')
    #             self.solutions[num]['objects'] = possibilities['objects']['OIE']
    #         if (choice == 2):
    #             print('YOU HAVE CHOSEN ' + possibilities['objects']['Dependency parsing'] + ' AS OBJECT!')
    #             self.solutions[num]['objects'] = possibilities['objects']['Dependency parsing']
    #         if (choice == 3):
    #             print('YOU HAVE CHOSEN ' + possibilities['objects']['POS'] + ' AS OBJECT!')
    #             self.solutions[num]['objects'] = possibilities['objects']['POS']
    # 
    #     print(self.solutions)
    #     if (self.coreference):
    #         all = []
    #         for i in range(1, num + 1):
    #             print(self.solutions[i]['subjects'])
    #             all.append(self.solutions[i]['subjects'])
    # 
    #         print('tu')
    #         print(all)
    #         print(self.solveCoReference(all))
    #     return resp
    #


    def openInformationExtractionPipeline(self, sent):
        # text = (' ').join([word.lemma for sent in doc.sentences for word in sent.words])
        subjects = ''
        objects = ''
        relations = ''

        with CoreNLPClient(annotators=self.configuration.processors,
                           memory='3G') as client:

            url = 'http://localhost:9000/api/v1/extract'
            data = {'data': 'ano', 'format': 'json'}
            r = requests.post(url, json=data)

            #     openie_triples = []
            #     for triple in r.json()['data']:
            #         openie_triples.append((triple['subject'], triple['relation'], triple['object']))
            #     print(openie_triples)
            #     print('spustil')
            ann = client.annotate(self.text)
            #
            for sentence in ann.sentence:
                # print(sentence.openieTriple)
                for triple in sentence.openieTriple:
                    print('TRIPLE!')
                    # print(triple)
                    print('<subject>' + triple.subject + '</subject>')

                    if len(triple.subject) > len(subjects) or len(subjects) == 0:
                        subjects = triple.subject

                    print('<relation>' + triple.relation + '</relation>')

                    if len(triple.relation) < len(relations) or len(relations) == 0:
                        relations = triple.relation

                    print('<object>' + triple.object + '</object>')

                    if len(triple.object) > len(objects) or len(objects) == 0:
                        objects = triple.object
        #
        #   # treba vybrať najdlhši subject najdlhši object a ralaciu, ktorá ich dokáže spojit
        # print('Subject: ' + subjects)
        # print('Relations: ' + relations)
        # print('Object: ' + objects)

        return [True, ' '.join(subjects), ' '.join(relations), ' '.join(objects)]

    def partOfSpeechPipeline(self, sent):

        subjects = []
        objects = []
        relations = []
        secondVerb = False
        firstVerb = False

        for word in sent.words:
            print(word.text)
            print('<xpos>' + word.xpos + '/xpos>')
            print('<npos>' + word.xpos + '/npos>')
            if (objects == [] and subjects != []):
                if ('VB' in word.xpos):
                    relations.append(word.text)
                    firstVerb = True
                if (('JJ' in word.xpos or 'RB' in word.xpos or 'IN' in word.xpos) and not firstVerb):
                    relations.append(word.text)

            if (objects != []):
                if ('VB' in word.xpos):
                    secondVerb = True

            if (relations == []):
                if ('NN' in word.xpos or 'JJ' in word.xpos or 'RB' in word.xpos or 'IN' in word.xpos):
                    subjects.append(word.text)

            if (relations != [] and not secondVerb):
                if ('NN' in word.xpos):
                    objects.append(word.text)
                if (('JJ' in word.xpos or 'RB' in word.xpos or 'IN' in word.xpos) and firstVerb):
                    objects.append(word.text)
        return [True, ' '.join(subjects), ' '.join(relations), ' '.join(objects)]
    # 
    def partOfSpeechPipelineSpacy(self, text):
        subjects = []
        objects = []
        relations = []
        print('text je:'+text)
        doc = self.nlp(text)

        for token in doc:
            print(str(token))
            print(str(token.pos_))

            if token.pos_ == 'VERB' and objects == []:
                relations.append(str(token))
            #     print(relations)
            #     print('Add ' + str(token) + ' because ' + token.pos_ + ' to relations')
            elif token.pos_ == 'VERB' and objects != []:
                objects.append(str(token))
                # print(objects)
                # print('Add ' + str(token) + ' because ' + token.pos_ + ' to relations')
            elif token.pos_ in ['NOUN', 'ADP','ADV'] and subjects != [] and relations != []:
                objects.append(str(token))
                # print(objects)
                # print('Add ' + str(token) + ' because ' + token.pos_ + ' to objects')
            elif token.pos_ in ['NOUN', 'ADP','PROPN']:
                subjects.append(str(token))
                # print(subjects)
                # print('Add ' + str(token) + ' because ' + token.pos_ + ' to subjects')

        # print(subjects)
        # print(relations)
        # print(objects)
        return [True, ' '.join(subjects), ' '.join(relations), ' '.join(objects)]
    #

    def dependencyTreePipelineSpacy(self, text):
        subjects = []
        objects = []
        relations = []
        doc = self.nlp(text)
        for token in doc:
           was_before = True
           if token.dep_ == 'ROOT':
               print(token.text + ' je root')
               num_of_children = len([t for t in token.children])
               if (num_of_children == 2):
                   [subjects.append(tt.text) for tt in [t for t in token.children][0].subtree]
                   [objects.append(tt.text) for tt in [t for t in token.children][1].subtree]
                   relations.append(token.text)
               else:
                   [subjects.append(tt.text) for tt in [t for t in token.children][0].subtree]
                   # relations.append(token.text)
                   for i in range(1,num_of_children-1):
                       word = [t for t in token.children][i].text
                       print('Spracovavam ' + word)
                       print(relations)
                       if text.find(word) < text.find(token.text) and was_before:
                           relations.append(word)
                           print('pridal slovo '+word)
                       elif  text.find(word) > text.find(token.text) and was_before:
                           was_before = False
                           relations.append(token.text)
                           relations.append(word)
                           print('appendol token vo fore')
                           print('pridal slovo ' + word)
                       else:
                           relations.append(word)
                           print('muckol slovo ' + word)
                   if was_before:
                       relations.append(token.text)
                       print('appendol token')
                       print('priklincoval slovo ' + token.text)

                   [objects.append(tt.text) for tt in [t for t in token.children][-1].subtree]

        return [True, ' '.join(subjects), ' '.join(relations), ' '.join(objects)]
    def dependencyTreePipeline(self, sent):
        subjects = []
        objects = []
        relations = []

        relation_id = 0
        subject_id = 0
        object_id = 0

        for word in sent.words:
            if word.deprel == 'root':
                relation_id = word.id

        for word in sent.words:
            if (word.head == relation_id
                and 'subj' not in word.deprel
                and 'ob' not in word.deprel
                and word.deprel not in ('punct')) \
                    or word.deprel == 'root':
                relations.append(word.text)

        for word in sent.words:
            if word.head == relation_id and 'subj' in word.deprel:
                subject_id = word.id

        for word in sent.words:
            if (word.head == subject_id or word.id == subject_id) and word.deprel not in ('punct'):
                subjects.append(word.text)

        for word in sent.words:
            if word.head == relation_id and 'ob' in word.deprel:
                object_id = word.id

        for word in sent.words:
            if (word.head == object_id or word.id == object_id) and word.deprel not in ('punct'):
                objects.append(word.text)

        return [True, ' '.join(subjects), ' '.join(relations), ' '.join(objects)]

    def synonyms(self, text):
        syn = []
        for sublist in wn.synonyms(text):
            for i in sublist:
                syn.append(i)
        return syn

    def solveCoReference(self, type):
        words = []
        numbers = [0]
        for i in range(1, len(self.solutions)+ 1):
            n = 0
            for j in self.solutions[i][type].split():
                words.append(j)
                n+=1
            numbers.append(n)

        for i in range(len(words)):
            word1 = words[i].lower()
            for j in range(len(words)):
                word2 = words[j].lower()
                if word1 in self.synonyms(word2) and word2 in self.synonyms(word1):
                    if (len(self.synonyms(word2)) < len(self.synonyms(word1))):
                        words[i] = word1
                        words[j] = word1
                    else:
                        words[i] = word2
                        words[j] = word2

                    # print(word1 + 'je synonymum s ' + word2)
            # print('aspon zapol')
            # print(word1)
            # print(self.synonyms(word1))
        n = 0
        for i in range(1, len(self.solutions) + 1):

            self.solutions[i][type] = []
            while(numbers[i]!=0):
                numbers[i]-=1
                self.solutions[i][type].append(words[n])
                n+=1
            self.solutions[i][type] = ' '.join(self.solutions[i][type])
        return words
