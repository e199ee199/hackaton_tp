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