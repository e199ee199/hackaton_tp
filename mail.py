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

    def process(self):
        self.create_folders()
        message_list = self.reader.read_folders(self.inbox_dir)
        cnt = len(message_list)
        msg = f'Обработано писем: {cnt}'
        print(msg)
        log.info(msg)

        for msg in message_list: #классификация каждого письма
            category = self.classifier.choose_category(msg)
            msg.category = category
            self.results[msg.filename] = category

            if category not in self.stats:#статистика 
                self.stats[category] = 0
            self.stats[category] += 1
            self.move_file(msg, category)
        return self.results
    def statistics(self):#статистика 
        total = 0
        for key in self.stats: #общее количество
            total +=self.stats[key]
        stats_list = []
        for key in self.stats:
            stats_list.append([key, self.stats[key]])

        for i in range(len(stats_list)):#сортировка
            for j in range(i+1, len(stats_list)):
                if stats_list[j][1] > stats_list[i][1]:
                    tmp = stats_list[i]
                    stats_list[i] = stats_list[j]
                    stats_list[j] = tmp

        for item in stats_list:
            name = item[0]
            count = item[1]
            if total>0:
                percent = round((count*100) / total, 1)#доля категории в процентах 
            else:
                percent = 0
            print(f'{name}: {count} писем {percent}%')
        print(f'Итого {total} писем ')
        log.info(f'Статистика {self.stats}')
        return self.stats