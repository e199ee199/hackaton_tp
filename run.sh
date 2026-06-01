#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

if [ ! -d "inbox" ]; then
    echo "Ошибка: папка inbox/ не найдена!"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "Ошибка: python3 не установлен!"
    exit 1
fi

python3 main.py
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "Статус: Обработка успешно завершена!"
else
    echo "Ошибка при выполнении программы! Код: $EXIT_CODE"
    exit $EXIT_CODE
fi
