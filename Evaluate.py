from sklearn.metrics import f1_score
import spacy


class Evaluate:
    def give_sources(self, first, second):
        with open(second) as f:
            true_labels = f.readlines()
        with open(first) as f:
            predicted_labels = f.readlines()
        return [true_labels, predicted_labels]

    def evaluate_whole_words(self, first, second):
        src = self.give_sources(first, second)
        true_labels = src[0]
        predicted_labels = src[1]
        print('evaluate_whole_words')
        print(true_labels)
        print(predicted_labels)
        try:
            f1 = f1_score(true_labels, predicted_labels, average='micro')
        except ValueError:
            f1 = "Was not successful enough"
        return f1

    def evaluate_life_lines(self, first, second):
        src = self.give_sources(first, second)
        true_labels = src[0]
        predicted_labels = src[1]
        true_actors = self.extract_actors(true_labels)
        predicted_actors = self.extract_actors(predicted_labels)

        try:
            f1 = f1_score(true_actors, predicted_actors, average='micro')
        except ValueError:
            f1 = "Was not successful enough"
        return f1


    def evaluate_messages(self, first, second):
        src = self.give_sources(first, second)
        true_labels = src[0]
        predicted_labels = src[1]
        print('evaluate_messages')
        print(true_labels)
        print(predicted_labels)
        true_messages = self.extract_messages(true_labels)
        predicted_messages = self.extract_messages(predicted_labels)
        try:
            f1 = f1_score(true_messages, predicted_messages, average='micro')
        except ValueError :
            f1 = "Was not successful enough"

        return f1

    def evaluate_syntax_similarity(self, first, second):
        nlp = spacy.load("en_core_web_lg")

        src = self.give_sources(first, second)
        true_labels = "".join(src[0])
        predicted_labels = "".join(src[1])
        # Process the texts with spaCy

        doc1 = nlp(true_labels)
        doc2 = nlp(predicted_labels)

        # Calculate the similarity score
        similarity_score = doc1.similarity(doc2)

        try:
            similarity_score = doc1.similarity(doc2)
        except ValueError:
            similarity_score = "Was not successful enough"


        return similarity_score

    def extract_actors(self, lines):
        actors = []

        for line in lines:
            if 'actor' in line.split()[0]:
                actors.append(line)

        return actors

    def extract_messages(self, lines):
        messages = []

        for line in lines:
            if 'actor' not in line.split()[0]:
                messages.append(line)

        return messages
