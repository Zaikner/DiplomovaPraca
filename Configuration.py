class Configuration:
    def __init__(self):
        self.text = ''
        self.system = 'system'
        self.users = {}
        self.project = None
        self.coreference = False
        self.steps = False
        self.engine = 'spacy'
        self.mode = 'POS'
        self.processors = ['all']
        self.model = 'en_core_web_lg'
        self.fragments = False
        self.fragmentPattern = None
        self.parameters = False
        self.pattern = None

