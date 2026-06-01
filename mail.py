class Processor: #класс для связывания всего 
    def __init__(self, inbox_dir, out_dir):
        self.inbox_dir = inbox_dir
        self.out_dir = out_dir
        self.reader = Reader()
        self.classifier = Classifier()
        self.results = {}
        self.stats = {}
        self.categories = ['incident', 'request','hr', 'equipment', 'monitoring', 'info', 'spam', 'finance', 'uncategorized'
                            ]