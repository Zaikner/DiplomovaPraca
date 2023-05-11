from nltk.corpus import wordnet as wn
from stanza.server import CoreNLPClient
import stanza
import requests

from DiplomovaPraca.Drawer import Drawer


class ConversionPipeline:

    def __init__(self, text, mode = 'all', coreference = True, steps = False, project=None):
        self.project = project
        self.text = text
        self.coreference = coreference
        self.steps = steps
        self.mode = mode

        if (steps):
            d = Drawer(self.run_with_steps(text))
            d.create_PlantUml()

        else:
            d = Drawer(self.run_without_steps(text))
            d.create_PlantUml()

    def createProject(self, project):
        self.project = project

    def run_without_steps(self,text):
        sentences = text.split('.')
        nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma,depparse')
        doc = nlp(text)

        num = 0
        solutions = {}
        for sent in doc.sentences:
            num+=1
            solutions[num] = {}
            solutions[num]['subjects'] = {}
            solutions[num]['objects'] = {}
            solutions[num]['relations'] = {}
            if (self.mode in ['all','OIE']):
                res = self.openInformationExtractionPipeline(sent)
                found = False
                if self.project != None:
                    for sub in self.project.subjects:
                        if sub in sentences[num - 1]:
                            solutions[num]['subjects']['OIE'] = sub
                            found = True

                if not found:
                    solutions[num]['subjects']['OIE'] = res[1]

                found = False
                if self.project != None:
                    for rel in self.project.relations:
                        if rel in sentences[num - 1]:
                            solutions[num]['relations']['OIE'] = rel
                            found = True

                if not found:
                    solutions[num]['relations']['OIE'] = res[2]

                found = False
                if self.project != None:
                    for obj in self.project.objects:
                        if obj in sentences[num - 1]:
                            solutions[num]['objects']['OIE'] = obj
                            found = True

                if not found:
                    solutions[num]['objects']['OIE'] = res[3]
                resp = 'OIE: ' + solutions[num]['subjects']['OIE'] + '-->' + solutions[num]['relations'][
                    'OIE'] + '-->' + solutions[num]['objects']['OIE']

                print(resp)
            if (self.mode in ['all', 'DP']):
                res = self.dependencyTreePipeline(sent)
                found = False
                if self.project != None:
                    for sub in self.project.subjects:
                        if sub in sentences[num - 1]:
                            solutions[num]['subjects']['Dependency parsing'] = sub
                            found = True

                if not found:
                    solutions[num]['subjects']['Dependency parsing'] = res[1]

                found = False
                if self.project != None:
                    for rel in self.project.relations:
                        if rel in sentences[num - 1]:
                            solutions[num]['relations']['Dependency parsing'] = rel
                            found = True

                if not found:
                    solutions[num]['relations']['Dependency parsing'] = res[2]

                found = False
                if self.project != None:
                    for obj in self.project.objects:
                        if obj in sentences[num - 1]:
                            solutions[num]['objects']['Dependency parsing'] = obj
                            found = True

                if not found:
                    solutions[num]['objects']['Dependency parsing'] = res[3]

                resp = 'Dependency parsing: ' + solutions[num]['subjects']['Dependency parsing'] + '-->' + solutions[num]['relations'][
                    'Dependency parsing'] + '-->' + solutions[num]['objects']['Dependency parsing']

                print(resp)
            if (self.mode in ['all', 'POS']):
                res = self.partOfSpeechPipeline(sent)

                found = False
                if self.project != None:
                    for sub in self.project.subjects:
                        if sub in sentences[num - 1]:
                            solutions[num]['subjects']['POS'] = sub
                            found = True

                if not found:
                    solutions[num]['subjects']['POS'] = res[1]

                found = False
                if self.project != None:
                    for rel in self.project.relations:
                        if rel in sentences[num - 1]:
                            solutions[num]['relations']['POS'] = rel
                            found = True

                if not found:
                    solutions[num]['relations']['POS'] = res[2]

                found = False
                if self.project != None:
                    for obj in self.project.objects:
                        if obj in sentences[num - 1]:
                            solutions[num]['objects']['POS'] = obj
                            found = True

                if not found:
                    solutions[num]['objects']['POS'] = res[3]

                resp = 'POS: ' + solutions[num]['subjects']['POS'] + '-->' + solutions[num]['relations'][
                    'POS'] + '-->' + solutions[num]['objects']['POS']
                print(resp)

        print(solutions)
        if (self.coreference):
            all =[]
            for i in range(1,num+1):
                for j in solutions[i]['subjects'].values():
                   all.append(j)

            print('tu')
            print(all)
            self.solveCoReference(all)
        return solutions

    def run_with_steps(self, text):
        nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma,depparse')
        doc = nlp(text)

        num = 0
        solutions = {}
        for sent in doc.sentences:
            num += 1
            possibilities = {}
            solutions[num] = {}
            solutions[num]['subjects'] = {}
            solutions[num]['objects'] = {}
            solutions[num]['relations'] = {}
            possibilities['subjects'] = {}
            possibilities['objects'] = {}
            possibilities['relations'] = {}
            if (self.mode in ['all', 'OIE']):
                res = self.openInformationExtractionPipeline(sent)
                resp = 'OIE : ' + res[1] + '-->' + res[2] + '-->' + res[3]
                possibilities['subjects']['OIE'] = res[1]
                possibilities['relations']['OIE'] = res[2]
                possibilities['objects']['OIE'] = res[3]
            if (self.mode in ['all', 'DP']):
                res = self.dependencyTreePipeline(sent)
                resp = 'Dependency parsing : ' + res[1] + '-->' + res[2] + '-->' + res[3]
                possibilities['subjects']['Dependency parsing'] = res[1]
                possibilities['relations']['Dependency parsing'] = res[2]
                possibilities['objects']['Dependency parsing'] = res[3]
            if (self.mode in ['all', 'POS']):
                res = self.partOfSpeechPipeline(sent)
                resp = 'POS: ' + res[1] + '-->' + res[2] + '-->' + res[3]
                possibilities['subjects']['POS'] = res[1]
                possibilities['relations']['POS'] = res[2]
                possibilities['objects']['POS'] = res[3]

            choice = 0

            while choice not in [1,2,3]:
                try:
                    print('1. ' + possibilities['subjects']['OIE'])
                    print('2. ' + possibilities['subjects']['Dependency parsing'])
                    print('3. ' + possibilities['subjects']['POS'])
                    choice = int(input('Choose your subject, write number of your choice:'))
                    if choice not in [1,2,3]:
                        print('YOU SHOULD WROTE ONE NUMBER 1,2 OR 3 !')
                except:
                    print('YOU SHOULD WROTE ONE NUMBER 1,2 OR 3 !')

            if (choice == 1):
                print('YOU HAVE CHOSEN '+ possibilities['subjects']['OIE'] + ' AS SUBJECT!')
                solutions[num]['subjects'] = possibilities['subjects']['OIE']
            if (choice == 2):
                print('YOU HAVE CHOSEN '+ possibilities['subjects']['Dependency parsing'] + ' AS SUBJECT!')
                solutions[num]['subjects'] = possibilities['subjects']['Dependency parsing']
            if (choice == 3):
                print('YOU HAVE CHOSEN '+ possibilities['subjects']['POS'] + ' AS SUBJECT!')
                solutions[num]['subjects'] = possibilities['subjects']['POS']
            choice = 0
            while choice not in [1, 2, 3]:
                try:
                    print('1. ' + possibilities['relations']['OIE'])
                    print('2. ' + possibilities['relations']['Dependency parsing'])
                    print('3. ' + possibilities['relations']['POS'])
                    choice = int(input('Choose your relation, write number of your choice:'))
                    if choice not in [1, 2, 3]:
                        print('YOU SHOULD WROTE ONE NUMBER 1,2 OR 3 !')
                except:
                    print('YOU SHOULD WROTE ONE NUMBER 1,2 OR 3 !')

            if (choice == 1):
                print('YOU HAVE CHOSEN ' + possibilities['relations']['OIE'] + ' AS RELATION!')
                solutions[num]['relations'] = possibilities['relations']['OIE']
            if (choice == 2):
                print('YOU HAVE CHOSEN ' + possibilities['relations']['Dependency parsing'] + ' AS RELATION!')
                solutions[num]['relations'] = possibilities['relations']['Dependency parsing']
            if (choice == 3):
                print('YOU HAVE CHOSEN ' + possibilities['relations']['POS'] + ' AS RELATION!')
                solutions[num]['relations'] = possibilities['relations']['POS']
            choice = 0
            while choice not in [1, 2, 3]:
                try:
                    print('1. ' + possibilities['objects']['OIE'])
                    print('2. ' + possibilities['objects']['Dependency parsing'])
                    print('3. ' + possibilities['objects']['POS'])
                    choice = int(input('Choose your object, write number of your choice:'))
                    if choice not in [1, 2, 3]:
                        print('YOU SHOULD WROTE ONE NUMBER 1,2 OR 3 !')
                except:
                    print('YOU SHOULD WROTE ONE NUMBER 1,2 OR 3 !')

            if (choice == 1):
                print('YOU HAVE CHOSEN ' + possibilities['objects']['OIE'] + ' AS OBJECT!')
                solutions[num]['objects'] = possibilities['objects']['OIE']
            if (choice == 2):
                print('YOU HAVE CHOSEN ' + possibilities['objects']['Dependency parsing'] + ' AS OBJECT!')
                solutions[num]['objects'] = possibilities['objects']['Dependency parsing']
            if (choice == 3):
                print('YOU HAVE CHOSEN ' + possibilities['objects']['POS'] + ' AS OBJECT!')
                solutions[num]['objects'] = possibilities['objects']['POS']

        print(solutions)
        if (self.coreference):
                    all = []
                    for i in range(1, num + 1):
                        print(solutions[i]['subjects'])
                        all.append(solutions[i]['subjects'])


                    print('tu')
                    print(all)
                    print(self.solveCoReference(all))
        return resp


    def openInformationExtractionPipeline(self,sent):

        # text = (' ').join([word.lemma for sent in doc.sentences for word in sent.words])
        subjects = ''
        objects = ''
        relations = ''


        with CoreNLPClient(annotators=['tokenize,lemma,pos,depparse,openie'],
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
                print(sentence.openieTriple)
                for triple in sentence.openieTriple:
                    print('TRIPLE!')
                    print(triple)
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
        return [False, '', '', '']
        return [True, ' '.join(subjects), ' '.join(relations), ' '.join(objects)]

    def partOfSpeechPipeline(self,sent):
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

    def dependencyTreePipeline(self,sent):
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
            if word.head == relation_id and 'ob' in word.deprel :
                object_id = word.id


        for word in sent.words:
            if (word.head == object_id or word.id == object_id) and word.deprel not in ('punct'):
                objects.append(word.text)
        return [True, ' '.join(subjects), ' '.join(relations), ' '.join(objects)]


    def draw(self):
        return



    def synonyms(self,text):
        syn = []
        for sublist in wn.synonyms(text):
            for i in sublist:
                syn.append(i)
        return syn

    def solveCoReference(self,words):
        for i in range(len(words)):
            word1 = words[i].lower()
            for j in range(len(words)):
                word2 = words[j].lower()
                if word1 in self.synonyms(word2) and  word2 in self.synonyms(word1):
                    if (len(self.synonyms(word2)) < len(self.synonyms(word1))):
                        words[i] = word1
                        words[j] = word1
                    else:
                        words[i] = word2
                        words[j] = word2

                    print(word1 + 'je synonymum s ' + word2)
            print('aspon zapol')
            print(word1)
            print(self.synonyms(word1))
        return words
