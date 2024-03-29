import time

import nltk
from nltk.corpus import wordnet as wn
from stanza.server import CoreNLPClient
import stanza
import requests

from DiplomovaPraca.Drawer import Drawer
import spacy.cli

from DiplomovaPraca.Fragment import Fragment
from DiplomovaPraca.User import User
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
        self.numberOfSentences = 0

        self.sentences = text.strip().split('.')
        if len(self.sentences[-1]) == 0:
            self.sentences = self.sentences[:len(self.sentences) - 1]

        print('Conversion pipeline run with following configuration:')
        print('Project: ' + str(configuration.project))
        print('Coreference: ' + str(configuration.coreference))
        print('Steps: ' + str(configuration.steps))
        print('NLP engine: ' + str(configuration.engine))
        print('Processors: [' + ", ".join(self.configuration.processors) + ']')
        print('Mode: ' + str(configuration.mode))

    def run(self):
        start = time.time()
        if not self.configuration.steps:
            res = self.run_without_steps()
            print("Run took "+str(time.time()-start))
            for num in range(1, len(res)):
                if len(res[num]['subjects']) == 0:
                    return ['subject error', num, res[num]]
                if len(res[num]['relations']) == 0:
                    return ['relation error', num, res[num]]
                if len(res[num]['objects']) == 0:
                    return ['object error', num, res[num]]

            if (res != False and len(self.configuration.users.items()) != 0):
                d = Drawer(res, self.configuration)
                d.create_PlantUml()
                return ['ok', 0]

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
            sentence = sentence.replace(self.phrases[token], token)
        return sentence

    def replace_tokens(self, sentence):
        for token in self.phrases.keys():
            sentence = sentence.replace(token, self.phrases[token])
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
        print('zacal detecovat')
        i = 1
        new_senteces = []
        for sentence in self.sentences:
            if '|' in sentence:
                print('nasiel fragment')
                print(sentence.split('|'))
                # if len(sentence.split()) == 2:
                fragment = sentence.split('|')[1].strip()
                if fragment.lower() == 'alt':
                    self.lastFragment = Fragment('alt', len(self.fragments), i)
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
                            print('Prvy nestopnuty' + self.fragments[num].type)
                            self.fragments[num].ended = True
                            self.fragments[num].end_sentence = i
                            stop = True;
                            print('Prvy nestopnuty' + str(i))
                        num += 1
                    print('tu to ukoncit')
                else:
                    print('WRONG fragment')
                    print(sentence)
            else:
                i += 1
                new_senteces.append(sentence)
            self.sentences = new_senteces

    def run_without_steps(self):
        self.validPattern = True


        if self.configuration.fragments:
            self.detect_fragments()
        else:
            self.remove_fragment_keywords()

        self.solutions = {}
        self.solutions['fragments'] = self.fragments
        num = 0
        for i in range(len(self.sentences)):
            self.sentences[i] = self.replace_phrases(self.sentences[i])

        if self.configuration.engine == 'stanza':
            if self.configuration.processors == ['all']:
                self.nlp = stanza.Pipeline(lang='en', processors=['tokenize', 'mwt', 'pos', 'lemma', 'depparse'])
            else:
                self.nlp = stanza.Pipeline(lang='en', processors=self.configuration.processors)
            text = ". ".join(self.sentences)
            doc = self.nlp(text)
            self.original_sentences = self.sentences
            self.sentences = doc.sentences

        for sentence in self.sentences:

            print(sentence)
            print('prehladal')
            if self.configuration.fragmentPattern is not None:
                for key in self.configuration.fragmentPattern.keys():
                    for value in self.configuration.fragmentPattern[key]:
                        print('kontroluje value '+ value)
                        if key in ['LOOP', 'OPT']:
                            if value.strip().lstrip().rstrip().split('...')[0] in sentence and value.strip().lstrip().rstrip().split('...')[1] in sentence:

                                sentence_split = value.split('...')
                                sentence = sentence.replace(sentence_split[0].strip().lstrip().rstrip(),'')
                                label = sentence.split(sentence_split[1].strip().lstrip().rstrip())[0]
                                sentence =sentence.split(sentence_split[1].strip().lstrip().rstrip())[1].lstrip()
                                fragment = Fragment(key, len(self.fragments), num+1)
                                fragment.text = label
                                self.fragments.append(fragment)
                                print(sentence)
                                print('NASIEL FRAGMENT ' + key)
                        elif key in ['PAR', 'ALT']:
                            print('do magic')
                        # if key in ['OPT']:
                        #     if value.strip().lstrip().rstrip().split('...')[0] in sentence and value.strip().lstrip().rstrip().split('...')[1] in sentence:
                        #         # TODO: opravit
                        #         stop_words = value.split('...')
                        #         sentence = sentence.replace(stop_words[0])
                        #         sentence_split = sentence.split(stop_words[1])
                        #         sentence = sentence_split[1].strip().lstrip().rstrip()
                        #         fragment = Fragment(key, len(self.fragments), num + 1)
                        #         fragment.text = sentence_split[0]
                        #         # self.fragments.append(fragment)
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
            self.solutions[num]['subjects'] = result[1].strip()

            if  self.is_user(result[1].strip()):
                self.configuration.users[num] = User(result[1].strip(),num)
                print('pridal usera '+ self.configuration.users[num].text)
            self.solutions[num]['objects'] = result[3].strip()
            self.solutions[num]['relations'] = result[2].strip()
            self.solutions[num]['main_relation'] = result[0].strip()

            # TODO: tu sa ide riesit project
            # TODO: dat nejake zabezpecenie, ak to pouzijem, odstran to
            if self.configuration.engine == 'stanza':
                orig_sentence = self.original_sentences[num-1]
            else:
                orig_sentence = "".join(sentence);
            if self.configuration.project != None:
                print('aspon zapol projekt')
                for phrase in self.configuration.project.data[num]['subject']:
                    if phrase in orig_sentence:
                        print('rozoznal subjekt')
                        self.solutions[num]['subjects'] = phrase

                for phrase in self.configuration.project.data[num]['relation']:
                    if phrase in orig_sentence:
                        print('rozoznal subjekt')
                        self.solutions[num]['relations'] = phrase

                for phrase in self.configuration.project.data[num]['object']:
                    if phrase in orig_sentence:
                        print('rozoznal subjekt')
                        self.solutions[num]['objects'] = phrase
                # if self.configuration.project.data[num]['relation'] in orig_sentence:
                #     print('rozoznal relation')
                #     self.solutions[num]['relation'] = self.configuration.project.data[num]['relation']
                # if self.configuration.project.data[num]['object'] in orig_sentence:
                #     print('rozoznal object')
                #     self.solutions[num]['object'] = self.configuration.project.data[num]['object']

            self.numberOfSentences = num
        if (self.configuration.coreference):
            self.solveCoReference('subjects')
            self.solveCoReference('objects')
            self.solveCoReference('relations')

        return self.solutions

    def is_user(self, word):
        word = nltk.WordNetLemmatizer().lemmatize(word.lower())

        synsets = wn.synsets(word)

        for synset in synsets:
            hypernyms = synset.hypernyms()
            for hypernym in hypernyms:
                if 'person' in hypernym.lexname() and 'animal':
                    return True
        return False

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
        main_relation = ''

        for word in sent.words:
            if word.upos == 'VERB' and 'VERB' not in [t.upos for t in relations]:
                relations.append(word)
                main_relation = word.text
                print('Add ' + str(word.text) + ' because ' + word.text + ' to relations')
            elif word.upos == 'VERB' and 'VERB' in [t.upos for t in relations]:
                objects.append(word)
                print('Add ' + str(word.text) + ' because ' + word.upos + ' to relations')
            elif word.upos in ['NOUN', 'ADP', 'ADV','ADJ'] and subjects != [] and relations != []:
                objects.append(word)
                print('Add ' + str(word.text) + ' because ' + word.upos + ' to objects')
            elif word.upos not in ['ADP', 'ADV', 'ADJ'] and relations == [] and subjects != []:
                subjects.append(word)
                print('Add ' + str(word.text) + ' because ' + word.upos + ' to subjects')
            elif word.upos in ['ADP', 'ADV', 'ADJ'] and 'VERB' not in [t.upos for t in relations] and subjects != []:
                relations.append(word)
                print('Add ' + str(word.text) + ' because ' + word.upos + ' to relations')
            elif relations == []:
                subjects.append(word)
                print('Add ' + str(word.text) + ' because ' + word.upos + ' to subjects')

        return [main_relation, ' '.join([str(token.text) for token in subjects]),
                ' '.join([str(token.lemma) for token in relations]), ' '.join([str(token.text) for token in objects])]


    #
    def partOfSpeechPipelineSpacy(self, text):
        subjects = []
        objects = []
        relations = []
        main_relation = ''
        print('text je:' + text)
        doc = self.nlp(text)

        for token in doc:
            print(str(token))
            print(str(token.pos_))

            if token.pos_ == 'VERB' and 'VERB' not in [t.pos_ for t in relations]:
                relations.append(token)
                main_relation = token.text
                print('Add ' + str(token) + ' because ' + token.pos_ + ' to relations')
            elif token.pos_ == 'VERB' and 'VERB' in [t.pos_ for t in relations]:
                objects.append(token)
                print('Add ' + str(token) + ' because ' + token.pos_ + ' to relations')
            elif token.pos_ in ['NOUN', 'ADP', 'ADV','ADJ'] and subjects != [] and relations != []:
                objects.append(token)
                print('Add ' + str(token) + ' because ' + token.pos_ + ' to objects')
            elif token.pos_ not in ['ADP', 'ADV', 'ADJ'] and relations == [] and subjects != []:
                subjects.append(token)
                print('Add ' + str(token) + ' because ' + token.pos_ + ' to subjects')
            elif token.pos_ in ['ADP', 'ADV', 'ADJ'] and 'VERB' not in [t.pos_ for t in relations] and subjects != []:
                relations.append(token)
                print('Add ' + str(token) + ' because ' + token.pos_ + ' to relations')
            elif relations == []:
                subjects.append(token)
                print('Add ' + str(token) + ' because ' + token.pos_ + ' to subjects')
        return [main_relation, ' '.join([str(token) for token in subjects]),
                ' '.join([str(token.lemma_) for token in relations]), ' '.join([str(token) for token in objects])]

    #

    def dependencyTreePipelineSpacy(self, text):
        subjects = []
        objects = []
        relations = []
        main_relation = ''
        doc = self.nlp(text)
        for token in doc:
            was_before = True
            print('Token je ' + token.text)
            print('Jeho deti su ' + str([t.text for t in token.subtree]))
            if token.dep_ == 'ROOT':
                main_relation = token.lemma_
                print(token.lemma_ + ' je root')
                print('Jeho deti su:' + str([t for t in token.children]))
                print('Jeho deti su:' + str([t.dep_ for t in token.children]))
                print('Jeho deti su:' + str([spacy.explain(t.dep_) for t in token.children]))
                print('Jeho subtree je'+ str([t for t in token.subtree]))
                num_of_children = len([t for t in token.children])
                object_start = num_of_children - 1  # point from which only object will be created
                found = False
                for child in reversed([t for t in token.children]):
                    if child.dep_ != 'dobj' and child.dep_ != 'prep' and not found:
                        object_start -= 1
                        print('odcital' + child.text)
                    elif child.dep_ == 'dobj' or child.dep_ == 'prep':
                        found = True;

                if (num_of_children == 2):
                    relations.append(token.lemma_)
                    [subjects.append(tt.text) for tt in [t for t in token.children][0].subtree]
                    [objects.append(tt.text) for tt in [t for t in token.children][1].subtree]

                else:
                    [subjects.append(tt.text) for tt in [t for t in token.children][0].subtree]
                    # relations.append(token.text)
                    for i in range(1, object_start):
                        print('deti predchadzajuceho slova')
                        # print('Jeho deti su:' + str([tt.text for tt in [t for t in token.children][i].tree]))
                        word = [t for t in token.children][i].text
                        print('Spracovavam ' + word)
                        print(relations)
                        if text.find(word) < text.find(token.text) and was_before:
                            relations.append(word)
                            print('pridal slovo ' + word)
                        elif text.find(word) > text.find(token.text) and was_before:
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
                    print('Vychadza z ' + [t for t in token.children][object_start].text)
                    for i in range(object_start, num_of_children):
                        [objects.append(tt.text) for tt in [t for t in token.children][i].subtree]

        return [main_relation, ' '.join(subjects), ' '.join(relations), ' '.join(objects)]

    def get_descendants(self,word, sent):
        # Initialize an empty list to store descendants
        # Initialize an empty list to store descendants
        descendants = []

        # Traverse the sentence to maintain the order of words
        for dep_word in sent.words:
            # Check if the current word is a descendant of the given word
            if int(dep_word.head) == word.id and dep_word.text != '.':
                # Recursively get descendants of the current word
                descendants.append(dep_word)
                descendants.extend(self.get_descendants(dep_word, sent))

        return descendants

    def giveStanzaChildren(self,find,sent):
        ret = []
        for word in sent.words:
            if word.head == find.id and word.text!='.':
                ret.append(word)
        return ret

    def dependencyTreePipelineStanza(self, sent):
    #     subjects = []
    #     objects = []
    #     relations = []
    #
    #     relation_id = 0
    #     subject_id = 0
    #     object_id = 0
    #
    #     for word in sent.words:
    #         print(word)
    #         if word.deprel == 'root':
    #             relation_id = word.id
    #
    #     for word in sent.words:
    #         if (word.head == relation_id
    #             and 'subj' not in word.deprel
    #             and 'ob' not in word.deprel
    #             and word.deprel not in ('punct')) \
    #                 or word.deprel == 'root':
    #             relations.append(word.text)
    #
    #     for word in sent.words:
    #         if word.head == relation_id and 'subj' in word.deprel:
    #             subject_id = word.id
    #
    #     for word in sent.words:
    #         if (word.head == subject_id or word.id == subject_id) and word.deprel not in ('punct'):
    #             subjects.append(word.text)
    #
    #     for word in sent.words:
    #         if word.head == relation_id and 'ob' in word.deprel:
    #             object_id = word.id
    #
    #     for word in sent.words:
    #         if (word.head == object_id or word.id == object_id) and word.deprel not in ('punct'):
    #             objects.append(word.text)
    #
    #     return ['', ' '.join(subjects), ' '.join(relations), ' '.join(objects)]
        subjects = []
        objects = []
        relations = []
        orig_sentence = ''.join([word.text for word in sent.words])
        main_relation = ''

        for word in sent.words:
            was_before = True
            print('Token je ' + word.text)
            # print('Jeho deti su ' + str([t.text for t in self.giveStanzaChildren(word,sent)]))
            if word.deprel == 'root':
                main_relation = word.lemma
                print(word.lemma + ' je root')

                print('Jeho deti su:' + str([t.text for t in self.giveStanzaChildren(word,sent)]))
                print('Jeho deti su:' + str([t.deprel for t in self.giveStanzaChildren(word,sent)]))
                # print('Jeho deti su:' + str([spacy.explain(t.dep_) for t in token.children]))
                print('Jeho subtree je' + str([t for t in self.get_descendants(word,sent)]))
                num_of_children = len([t.text for t in self.giveStanzaChildren(word,sent)])
                object_start = num_of_children - 1  # point from which only object will be created
                found = False
                for child in reversed([t for t in self.get_descendants(word,sent)]):
                    if child.text != '.':
                        if child.deprel not in ['obj','nmod','compound','case'] and child.deprel != 'prep' and not found:
                            object_start -= 1
                            print('odcital' + child.text)
                        elif child.deprel in ['obj','nmod','compound','case'] or child.deprel == 'prep':
                            found = True;

                if (num_of_children == 2):
                    relations.append(word.lemma)
                    [subjects.append(tt.text) for tt in self.get_descendants([t for t in self.giveStanzaChildren(word,sent)][0],sent)]
                    subjects.append(self.giveStanzaChildren(word,sent)[0].text)
                    [objects.append(tt.text) for tt in self.get_descendants([t for t in self.giveStanzaChildren(word, sent)][1], sent)]
                    objects.append(self.giveStanzaChildren(word, sent)[1].text)
                    print('slova subjectov')
                    print(self.giveStanzaChildren(word, sent))
                    print(self.get_descendants([t for t in self.giveStanzaChildren(word, sent)][0], sent))

                else:
                    [subjects.append(tt.text) for tt in self.get_descendants([t for t in self.giveStanzaChildren(word,sent)][0],sent)]
                    print('slova subjectov')
                    print(self.giveStanzaChildren(word,sent))
                    print(self.get_descendants([t for t in self.giveStanzaChildren(word,sent)][0],sent))
                    # relations.append(token.text)
                    for i in range(1, object_start):
                        print('deti predchadzajuceho slova')
                        # print('Jeho deti su:' + str([tt.text for tt in [t for t in token.children][i].tree]))
                        new_word = [t for t in self.giveStanzaChildren(word,sent)][i].text
                        print('Spracovavam ' + word.text)
                        print(relations)
                        if orig_sentence.find(new_word) < orig_sentence.find(word.text) and was_before:
                            relations.append(new_word)
                            print('pridal slovo ' + new_word)
                        elif orig_sentence.find(new_word) > orig_sentence.find(word.text) and was_before:
                            was_before = False
                            relations.append(word.text)
                            relations.append(new_word)
                            print('appendol token vo fore')
                            print('pridal slovo ' + new_word)
                        else:
                            relations.append(new_word)
                            print('muckol slovo ' + new_word)
                    if was_before:
                        relations.append(word.text)
                        print('appendol token')
                        print('priklincoval slovo ' + word.text)
                    # print('Vychadza z ' + [t for t in token.children][object_start].text)
                    for i in range(object_start, num_of_children):
                        [objects.append(tt.text) for tt in self.get_descendants([t for t in self.giveStanzaChildren(word, sent)][i], sent)]

        return [main_relation, ' '.join(subjects), ' '.join(relations), ' '.join(objects)]

    def synonyms(self, text):
        syn = []
        for sublist in wn.synonyms(text):
            for i in sublist:
                syn.append(i)
        return syn

    def solveCoReference(self, type):
        # TODO: skontrolovat, ci sa to neda urobit cez is_user
        words = []
        numbers = [0]
        for i in range(1, self.numberOfSentences + 1):
            n = 0
            for j in self.solutions[i][type].split():
                words.append(j)
                n += 1
            numbers.append(n)
        print('aspon pretiekol')
        for i in range(len(words)):
            word1 = words[i].lower()
            for j in range(len(words)):
                word2 = words[j].lower()
                print('Slovo 1 je :' + word1)
                print('synonima su:' + str(self.synonyms(word1)))
                print('Slovo 1 je :' + word2)
                print('synonima su:' + str(self.synonyms(word2)))
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
        for i in range(1, self.numberOfSentences + 1):

            self.solutions[i][type] = []
            while (numbers[i] != 0):
                numbers[i] -= 1
                self.solutions[i][type].append(words[n])
                n += 1
            self.solutions[i][type] = ' '.join(self.solutions[i][type])
        return words
