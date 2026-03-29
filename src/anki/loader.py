from pathlib import Path
import sys


class TextFileLoader:
    def __init__(self, *, file_path="./words.txt"):
        # Преобразуем переданный путь в объект Path
        self._file_path = Path(file_path)

        # Проверяем, что путь не является директорией
        if self._file_path.is_dir():
            raise ValueError(
                f"Указанный путь '{file_path}' является директорией, "
                f"а должен быть файлом")

    def load_words(self):
        """
        Загружает словарь из текстового файла.
        """

        words = {}

        # Проверяем, существует ли файл
        if not self._file_path.exists():
            return words

        try:
            with open(self._file_path, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if not line:  # Пропускаем пустые строки
                        continue

                    parts = line.split(",")
                    if len(parts) == 2:
                        word = parts[0].strip()
                        translation = parts[1].strip()
                        if word and translation:
                            words[word] = translation
            return words
        except FileNotFoundError:
            print(f"Ошибка: файл '{self._file_path}' не найден")
            sys.exit(1)

    def save_words(self, words):
        """
        Сохраняет словарь в текстовый файл.
        """

        # Валидация входных данных
        if not isinstance(words, dict):
            raise ValueError(
                f'Параметр `words` должен быть словарём, получен '
                f'{type(words).__name__}')

        with open(self._file_path, "w", encoding="utf-8") as file:
            for word, translation in words.items():
                file.write(f"{word},{translation}\n")
        print(f"Было сохранено {len(words)} слов в файл {self._file_path}")
