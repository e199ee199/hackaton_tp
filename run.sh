#!/bin/bash

if [ ! -d "inbox" ]; then
    echo 'Ошибка папка inbox не найдена'
    exit 1
fi

echo 'Проверка директории inbox'
count=0
for file in inbox/*; do
  if [ -f "$file" ]; then
      let count++
  fi
done
echo "Найдено файлов для обработки: $count"

echo "Запуск обработки"
if python3 main.py; then
    echo 'Готово обработка завершена'
else
    echo 'Ошибка при обработке писем'
    exit 1
fi

echo 'Готов результат по папкам'
if [ -d 'processed' ]; then
    for dir in processed/*; do
      if [ -d "$dir" ]; then
        n=0
        for f in "$dir"/*; do
            if [ -f "$f" ]; then
                let n++
            fi
        done
        echo "  $dir: $n штук"
      fi
    done
else
    echo 'Папка processed не создана и нечего проверять.'
fi