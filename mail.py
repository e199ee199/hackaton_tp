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
        tmp_text = text.strip()
        if len(tmp_text) == 0:
            msg.error = 'Пустой файл'
            log.warning (f'Файл {msg.filename} пустой')
            return msg

        if ext == 'json':
            msg = self.parse_json(msg, text)
            return msg

        lines = text.split('\n')
        body_start = 0
        for i in range(len(lines)):
            line=lines[i].strip()
            if line == '':
                body_start = i+1
                break
            s_lower = line.lower()
            if s_lower.startswith("subject:") or s_lower.startswith("тема:"):
                parts = line.split(":", 1)
                if len(parts) >1:
                    msg.subject = parts[1].strip()
            elif s_lower.startswith("from:") or s_lower.startswith("от кого:"):
                parts = line.split(":", 1)
                if len(parts)> 1:
                    msg.sender = parts[1].strip()
            elif s_lower.startswith("to:") or s_lower.startswith("кому:") or s_lower.startswith("date:") or s_lower.startswith("дата:"):
                pass
            else:
                body_start =i
                break
        body_lines = []
        for j in range(body_start,len(lines)):
            body_lines.append(lines[j])
        body_text = '\n'.join(body_lines)
        msg.body = body_text.strip()
        return msg