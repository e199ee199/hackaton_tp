# Mail module

import os
import logging
import json
import shutil

log = logging.getLogger()

class Message:
    def __init__(self, file_path):
        self.file_path = file_path
        self.filename = os.path.basename(file_path)
        self.subject = ''
        self.sender = ''
        self.body = ''
        self.extension = ''
        self.category = 'uncategorized'
        self.error = ''


class Reader:
    def __init__(self):
        self.messages = []
        self.binary_formats = [
            'jpeg', 'jpg', 'png', 'gif', 'bmp',
            'bin', 'exe', 'zip', 'rar', 'pdf'
        ]

    def get_format(self, file_name):
        ext = ''
        if '.' in file_name:
            parts = file_name.split('.')
            ext = parts[-1]
            ext = ext.lower()
        return ext

    def read_message(self, file_path):
        msg = Message(file_path)
        ext = self.get_format(msg.filename)
        msg.extension = ext
        flag = False
        for fmt in self.binary_formats:
            if ext == fmt:
                flag = True
                break

        if flag:
            msg.error = 'Бинарный файл'
            log.warning(f'Файл {msg.filename} с бинарным форматом')
            return msg

        text = ''
        try:
            f = open(file_path, 'r', encoding='utf-8')
            text = f.read()
            f.close()
        except Exception as error:
            msg.error = 'Ошибка чтения'
            log.error(f'Файл {msg.filename} с ошибкой чтения {error}')
            return msg

        tmp_text = text.strip()
        if len(tmp_text) == 0:
            msg.error = 'Пустой файл'
            log.warning(f'Файл {msg.filename} пустой')
            return msg

        if ext == 'json':
            msg = self.parse_json(msg, text)
            return msg

        lines = text.split('\n')
        body_start = 0
        for i in range(len(lines)):
            line = lines[i].strip()
            if line == '':
                body_start = i + 1
                break
            s_lower = line.lower()
            if s_lower.startswith("subject:") or s_lower.startswith("тема:"):
                parts = line.split(":", 1)
                if len(parts) > 1:
                    msg.subject = parts[1].strip()
            elif s_lower.startswith("from:") or s_lower.startswith("от кого:"):
                parts = line.split(":", 1)
                if len(parts) > 1:
                    msg.sender = parts[1].strip()
            elif s_lower.startswith("to:") or s_lower.startswith("кому:") or s_lower.startswith("date:") or s_lower.startswith("дата:"):
                pass
            else:
                body_start = i
                break

        body_lines = []
        for j in range(body_start, len(lines)):
            body_lines.append(lines[j])
        body_text = '\n'.join(body_lines)
        msg.body = body_text.strip()
        return msg

    def parse_json(self, msg, text):
        try:
            data = json.loads(text)
            msg.subject = data.get("subject", "")
            msg.sender = data.get("from", "")
            msg.body = data.get("body", str(data))
        except json.JSONDecodeError:
            msg.body = text
            log.warning(f"Файл {msg.filename} c некорректным json")
        return msg

    def read_folders(self, folder):
        if not os.path.isdir(folder):
            log.error("Папка {} не найдена!".format(folder))
            return []

        messages = []
        for name in sorted(os.listdir(folder)):
            if name[0] == ".":
                continue
            path = os.path.join(folder, name)
            if not os.path.isfile(path):
                continue
            messages.append(self.read_message(path))
        return messages


class Classifier:
    def __init__(self):
        self.rules = {}
        self.make_rules()
        self.category_order = ["monitoring", "incident", "spam", "hr", "equipment", "request", "finance", "info"]
    def make_rules(self):
        self.rules["monitoring"] = ["мониторинг", "cpu usage", "disk usage", "healthcheck", "uptime"]
        self.rules["incident"]   = ["ошибка 500", "сбой", "не отвечает", "критический инцидент", "не могу войти"]
        self.rules["spam"]       = ["выиграли приз", "нажмите на ссылку", "подтвердите личность", "скидка 90%","аккаунт заблокирован", "аккаунт будет заблокирован", "перейдите по ссылке","верификация аккаунта", "победителем розыгрыша"]
        self.rules["hr"]         = ["отпуск", "больничн", "новый сотрудник", "рабочее место", "график работы"]
        self.rules["equipment"]  = ["ремонт", "не включается", "сломался", "замен", "оборудован"]
        self.rules["request"]    = ["доступ", "нужна помощь", "не работает", "запрос", "клиент"]
        self.rules["finance"]    = ["счёт", "счет", "оплат", "акт", "бухгалтер"]
        self.rules["info"]       = ["дайджест", "инструкц", "созвон", "демо", "техническое задание"]
    def choose_category(self, message):
        if message.error != '':
            return 'uncategorized'
        full_text = (message.subject.lower() + ' ' + message.body.lower())
        if len(full_text) < 5:
            return 'uncategorized'
        for category in self.category_order:
            words = self.rules.get(category, [])
            for word in words:
                if word in full_text:
                    return category
        return 'uncategorized'

class Processor:
    def __init__(self, inbox_dir, out_dir):
        self.inbox_dir = inbox_dir
        self.out_dir = out_dir
        self.reader = Reader()
        self.classifier = Classifier()
        self.results = {}
        self.stats = {}
        self.categories = ['incident', 'request', 'hr', 'equipment', 'monitoring', 'info', 'spam', 'finance', 'uncategorized']

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

        for msg in message_list:
            category = self.classifier.choose_category(msg)
            msg.category = category
            self.results[msg.filename] = category

            if category not in self.stats:
                self.stats[category] = 0
            self.stats[category] += 1
            self.move_file(msg, category)
        return self.results

    def statistics(self):
        total = 0
        for key in self.stats:
            total += self.stats[key]
        stats_list = []
        for key in self.stats:
            stats_list.append([key, self.stats[key]])

        for i in range(len(stats_list)):
            for j in range(i + 1, len(stats_list)):
                if stats_list[j][1] > stats_list[i][1]:
                    tmp = stats_list[i]
                    stats_list[i] = stats_list[j]
                    stats_list[j] = tmp

        for item in stats_list:
            name = item[0]
            count = item[1]
            if total > 0:
                percent = round((count * 100) / total, 1)
            else:
                percent = 0
            print(f'{name}: {count} писем {percent}%')

        print(f'Итого {total} писем ')
        log.info(f'Статистика {self.stats}')
        return self.stats