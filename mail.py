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
    def create_folders(self): 
        for category in self.categories:
            folder_path = os.path.join(self.out_dir, category)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                log.info(f'Создана папка {category}')

    def move_file(self, message, category):  
        dest_folder = os.path.join(self.out_dir, category)
        new_path = os.path.join(dest_folder, message.filename)
        try:
            shutil.copy2(message.file_path, new_path)
        except Exception as error:
            log.error(f'Ошибка копирования {message.filename}: {error}')