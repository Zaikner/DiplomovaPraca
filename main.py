from DiplomovaPraca.ConversionPipeline import ConversionPipeline
from DiplomovaPraca.Project import Project
from DiplomovaPraca.utilities import readFile



# pipe = ConversionPipeline('Birdie eats carrot. Bird eats poppy. Chick eats fish.','all',True,True)
# pipe = ConversionPipeline('Barack Obama was born in Hawaii. Black Customer hastily pays with red Credit Card. Meter Metrology Board collects meter reading data.','all',False,False)

# project = Project(['Black'],['pays'],['reading data'])
# pipe = ConversionPipeline('Black Customer hastily pays with red Credit Card. Examples that represent exactly the same document. Meter Metrology Board collects meter reading data. Black Customer maliciously stole White Card.','all',False,False)
#pipe = ConversionPipeline('Richard Sulik is running for elections .Richard Sulik is attending elections. Richard Sulik was voted to parliament. Richard Sulik joins coalition. Richard Sulik destroyes coalition. Richard Sulik caused new elections.','all',False,False)
#pipe = ConversionPipeline('System displays a list of discount offers. Customer chooses a specific discount offer. System displays the discount offer details. Customer accepts offer. System checks number of available discount offers. System insert discount offer to basket.','all',False,False)
#pipe = ConversionPipeline('System inserts offer to basket.','all',False,False)
pipe = ConversionPipeline('.','all',False,False)



# Black Customer hastily pays with red Credit Card.
# Examples that represent exactly the same document.
# Meter Metrology Board collects meter reading data.
import requests

# def get_openie_triples(sentence):
#     url = 'http://localhost:9000/api/v1/extract'
#     data = {'data': sentence, 'format': 'json'}
#     r = requests.post(url, json=data)
#     openie_triples = []
#     for triple in r.json()['data']:
#         openie_triples.append((triple['subject'], triple['relation'], triple['object']))
#     return openie_triples
#
# sentence = 'Barack Obama was born in Hawaii.'
# openie_triples = get_openie_triples(sentence)
# print(openie_triples)

import stanza

# nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma,depparse')
# doc = nlp('Meter Metrology Board collects meter reading data')
# print(*[f'id: {word.id}\tword: {word.text}\thead id: {word.head}\thead: {sent.words[word.head-1].text if word.head > 0 else "root"}\tdeprel: {word.deprel}' for sent in doc.sentences for word in sent.words], sep='\n')