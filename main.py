import os
import logging
from mail_system import Processor

logging.basicConfig(filename='processing.log', level=logging.INFO)
inbox_dir = 'inbox'
out_dir = 'processed'

if not os.path.isdir(inbox_dir):
    print(f'Ошибка: папка {inbox_dir} не найдена')
else:
    processor = Processor(inbox_dir, out_dir)
    processor.process()
    processor.statistics()