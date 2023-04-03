from stanza.server import CoreNLPClient
import stanza
from nltk.corpus import wordnet as wn

from DiplomovaPraca.utilities import readFile

useCase = readFile('src/UC2.txt')


def pipeline(object_rule,relation_rule,subject_rule,text):
    text = 'Voltage Regulator Controller functions accordingly.'
    nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma')
    doc = nlp(text)
    subjects = ''
    objects = ''
    relations = ''
    for sent in doc.sentences:
        for word in sent.words:
            print('<text>' + word.text + '</text>')
            print('<lemma>' + word.lemma + '</lemma>')
            print('<upos>' + word.upos + '/upos>')
            print('<xpos>' + word.xpos + '/xpos>')
            print('<--------------------------->')

    text = (' ').join([word.lemma for sent in doc.sentences for word in sent.words])

    with CoreNLPClient(annotators=['tokenize', 'ssplit', 'pos', 'lemma', 'ner', 'depparse', 'natlog', 'openie'], memory='3G') as client:
        # print('spustil')
        ann = client.annotate(text)

        for sentence in ann.sentence:
            for triple in sentence.openieTriple:
                print('TRIPLE!')
                print(triple)
                # print('<subject>' + triple.subject + '</subject>')
                #
                # if len(triple.subject) > len(subjects) or len(subjects) == 0:
                #     subjects = triple.subject
                #
                # print('<relation>' + triple.relation + '</relation>')
                #
                # if len(triple.relation) < len(relations) or len(relations) == 0:
                #     relations = triple.relation
                #
                # print('<object>' + triple.object + '</object>')
                #
                # if len(triple.object) > len(objects) or len(objects) == 0:
                #     objects = triple.object

    #   treba vybrať najdlhši subject najdlhši object a ralaciu, ktorá ich dokáže spojit
    # print('Subject: ' + subjects)
    # print('Relations: ' + relations)
    # print('Object: ' + objects)


pipeline(1,1,1,useCase[0])

def synonyms(text):
    syn = []
    for sublist in wn.synonyms(text):
        for i in sublist:
            syn.append(i)
    return syn

