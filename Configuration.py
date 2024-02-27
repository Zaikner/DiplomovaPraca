class Configuration:
    def __init__(self):
        self.text = ''
        self.project = False
        self.coreference = False
        self.steps = False
        self.engine = 'spacy'
        self.mode = 'POS'
        self.processors = ['all']
        self.model = 'en_core_web_lg'
        self.fragments = False
        self.keywords = False

