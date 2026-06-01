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