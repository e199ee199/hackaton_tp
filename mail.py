# Mail module

import os
import logging
import json

log=logging.getLogger()
class Message:
    def __init__(self,file_path):
        self.file_path =file_path
        self.filename=os.path.basename(file_path)
        self.subject= ''
        self.sender = ''
        self.body= ''
        self.extension = ''
        self.category= 'uncategorized'
        self.error= ''
class Reader:
    def __init__(self):
        self.messages=[]
        self.binary_formats = [
            'jpeg', 'jpg', 'png', 'gif', 'bmp',
            'bin', 'exe', 'zip', 'rar', 'pdf'
        ]

    def get_format(self, file_name):
        ext=''
        if '.' in file_name:
            parts= file_name.split('.')
            ext=parts[-1]
            ext=ext.lower()
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