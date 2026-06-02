import os
import pytest
from mail_system import Message, Reader, Classifier, Processor

@pytest.fixture
def tmp_inbox(tmp_path):
    inbox = tmp_path / 'inbox'
    inbox.mkdir()
    return inbox

@pytest.fixture
def tmp_out(tmp_path):
    return tmp_path / 'processed'

def test_read_normaltext(tmp_path):
    f = tmp_path / 'test_mail.txt'
    f.write_text('Subject: Ошибка доступа\nFrom: user@corp.ru\n\nНе могу войти в систему.', encoding='utf-8')
    
    msg = Reader().read_message(str(f))
    assert msg.subject == 'Ошибка доступа'
    assert 'войти' in msg.body
    assert msg.error == ''

def test_read_emptyfile(tmp_path):
    f = tmp_path / 'empty.txt'
    f.write_text('', encoding='utf-8')
    msg = Reader().read_message(str(f))
    assert msg.error == 'Пустой файл'

def test_read_binary(tmp_path):
    f = tmp_path / 'image.png'
    f.write_bytes(b'\x89PNG\r\n\x1a\n')
    msg = Reader().read_message(str(f))
    assert msg.error == 'Бинарный файл'

def test_read_missfolders(tmp_path):
    result = Reader().read_folders(str(tmp_path / 'нет папки'))
    assert result == []

def test_read_noext(tmp_path):
    f = tmp_path / 'mail_0106'
    f.write_text('Subject: uptime\nFrom: monitor@corp.ru\n\nупtime ok', encoding='utf-8')
    msg = Reader().read_message(str(f))
    assert msg.error == ''
    assert msg.subject == 'uptime'

def test_read_jsonmail(tmp_path):
    f = tmp_path / 'mail.json'
    f.write_text('{"from": "down@mail.ru", "subject": "Аккаунт будет заблокирован", "body": "Подтвердите личность"}',
        encoding='utf-8'
    )
    msg = Reader().read_message(str(f))
    assert msg.sender == 'down@mail.ru'
    assert msg.subject == 'Аккаунт будет заблокирован'
    assert msg.error == ''