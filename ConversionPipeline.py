from nltk.corpus import wordnet as wn
from stanza.server import CoreNLPClient
import stanza
import requests

from DiplomovaPraca.Drawer import Drawer
import spacy.cli

from DiplomovaPraca.Fragment import Fragment
from DiplomovaPraca.utilities import init_tokens

class ConversionPipeline:

    def __init__(self, text, configuration):
        self.text = text
        self.sentences = []
        self.fragments = []
        self.lastFragment = None
        self.configuration = configuration
        self.phrases = {}
        self.tokens = init_tokens()

        self.sentences = text.strip().split('.')
        if len(self.sentences[-1]) == 0:
            self.sentences = self.sentences[:len(self.sentences) - 1]

        print('Conversion pipeline run with following configuration:')
        print('Project: '+str(configuration.project))
        print('Coreference: '+str(configuration.coreference))
        print('Steps: '+str(configuration.steps))
        print('NLP engine: ' + str(configuration.engine))
        print('Processors: [' + ", ".join(self.configuration.processors) + ']')
        print('Mode: '+str(configuration.mode))

    def run(self):
        if not self.configuration.steps:
            res = self.run_without_steps()

            if (res != False):
                d = Drawer(res)
                d.create_PlantUml()

    def replace_phrases(self, sentence):
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

    def remove_fragment_keywords(self):
        new_senteces = []
        for sentence in self.sentences:
            if not '|' in sentence:
                new_senteces.append(sentence)
            self.sentences = new_senteces

    def detect_fragments(self):
        i = 1
        new_senteces = []
        for sentence in self.sentences:
            if '|' in sentence:
                print('nasiel fragment')
                print(sentence.split('|'))
                # if len(sentence.split()) == 2:
                fragment = sentence.split('|')[1].strip()
                if fragment.lower() == 'alt':
                    self.lastFragment = Fragment('alt',len(self.fragments),i)
                    self.fragments.append(self.lastFragment)
                    print('Alt fragment')
                elif fragment.lower() == 'par':
                    self.lastFragment = Fragment('par', len(self.fragments), i)
                    self.fragments.append(self.lastFragment)
                    print('Par fragment')
                elif fragment.lower() == 'opt':
                    self.lastFragment = Fragment('opt', len(self.fragments), i)
                    self.fragments.append(self.lastFragment)
                    print('opt fragment')
                elif fragment.lower() == 'seq':
                    self.lastFragment = Fragment('seq', len(self.fragments), i)
                    self.fragments.append(self.lastFragment)
                    print('seq fragment')
                elif fragment.lower() == 'end':
                    num = 0
                    stop = False;
                    while num < len(self.fragments) and not stop:
                        if not self.fragments[num].ended:
                            print('Prvy nestopnuty'+self.fragments[num].type)
                            self.fragments[num].ended = True
                            self.fragments[num].end_sentence = i
                            stop = True;
                            print('Prvy nestopnuty' +str(i))
                        num+=1
                    print('tu to ukoncit')
                else:
                    print('WRONG fragment')
                    print(sentence)
            else:
                i += 1
                new_senteces.append(sentence)
            self.sentences = new_senteces



    def run_without_steps(self):
        if self.configuration.keywords:
            self.detect_fragments()
        else:
            self.remove_fragment_keywords()

        self.solutions = {}
        self.solutions['fragments'] = self.fragments
        num = 0
        for i in range(len(self.sentences)):
            self.sentences[i] = self.replace_phrases(self.sentences[i])

        if self.configuration.engine == 'stanza':

            self.nlp = stanza.Pipeline(lang='en', processors=self.configuration.processors)
            text = ". ".join(self.sentences)
            doc = self.nlp(text)
            sentences = doc.sentences

        for sentence in self.sentences:
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
                    result = self.partOfSpeechPipelineStanza(sentence)
                elif self.configuration.mode == 'DP':
                    result = self.dependencyTreePipelineStanza(sentence)
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

        # if (self.configuration.coreference):
        #     #TODO: REFACTOR
        #     all = []
        #     total = 0
        #     self.solveCoReference('subjects')
        #     self.solveCoReference('objects')
        #     self.solveCoReference('relations')
        # print('COREFERENCIE NEFUNGUJU')
        # print(self.solutions)
        return self.solutions


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

    def partOfSpeechPipelineStanza(self, sent):

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
    def dependencyTreePipelineStanza(self, sent):
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
