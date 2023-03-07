from stanza.server import CoreNLPClient
import stanza
text = "The system displays a list of discount offers"

#with CoreNLPClient(annotators=["tokenize","ssplit","pos","lemma","depparse","natlog","openie"], be_quiet=False) as client:
with CoreNLPClient(annotators=["openie"], be_quiet=False) as client:
    ann = client.annotate(text)
    #print(ann)
    for sentence in ann.sentence:
        for triple in sentence.openieTriple:
            print(triple)

# stanza.install_corenlp()