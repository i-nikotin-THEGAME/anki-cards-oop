from pathlib import Path
import sys


class TextFileLoader:
    """
    Класс для загрузки и сохранения словаря слов из текстового файла и в файл.

    Обеспечивает чтение данных из файла в формате "слово,перевод" и запись
    словаря обратно в файл. Поддерживает валидацию пути и обработку ошибок
    ввода-вывода.

    Формат файла:
        Каждая строка содержит слово и его перевод, разделённые запятой.
        Пример: "hello,привет"

    Attributes:
        _file_path (Path): Защищённый атрибут, содержащий путь к файлу
                           в виде объекта pathlib.Path.

    Examples:
        >>> loader = TextFileLoader(file_path="./my_words.txt")
        >>> loader.save_words({"hello": "привет", "world": "мир"})
        Сохранено 2 слов в файл ./my_words.txt

        >>> loaded_words = loader.load_words()
        >>> print(loaded_words)
        {'hello': 'привет', 'world': 'мир'}
    """

    def __init__(self, *, file_path="./words.txt"):
        """
        Инициализирует экземпляр TextFileLoader.

        Args:
            file_path (str, optional): Путь к файлу для загрузки/сохранения
                                       слов. По умолчанию "./words.txt".

        Raises:
            ValueError: Если указанный путь является директорией, а не файлом.

        Examples:
            >>> loader1 = TextFileLoader()  # Использует путь по умолчанию
            >>> loader2 = TextFileLoader(file_path="./data/words.txt")
            >>> loader3 = TextFileLoader(file_path="./")  # Вызовет ValueError
            Traceback (most recent call last):
                ...
            ValueError: Указанный путь './' является директорией,
            а должен быть файлом
        """
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

        Читает файл по пути self._file_path, парсит строки в формате
        "слово,перевод" и возвращает словарь. Пустые строки и строки
        некорректного формата игнорируются.

        Returns:
            dict: Словарь вида {"слово": "перевод"}. Если файл не существует,
                  возвращает пустой словарь {}.

        Notes:
            - Файл должен быть в кодировке UTF-8
            - Каждая строка должна содержать ровно одну запятую
            - Пробелы в начале и конце слов автоматически удаляются
            - Пустые слова или переводы игнорируются

        Examples:
            >>> loader = TextFileLoader(file_path="./existing_words.txt")
            >>> # Предположим, файл содержит: "hello,привет\\nworld,мир"
            >>> words = loader.load_words()
            >>> print(words)
            {'hello': 'привет', 'world': 'мир'}

            >>> loader2 = TextFileLoader(file_path="./nonexistent.txt")
            >>> words2 = loader2.load_words()
            >>> print(words2)
            {}
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

        Перезаписывает содержимое файла по пути self._file_path данными
        из переданного словаря. Каждая пара "слово-перевод" записывается
        в отдельную строку в формате "слово,перевод".

        Args:
            words (dict): Словарь для сохранения вида {"слово": "перевод"}.

        Raises:
            ValueError: Если параметр words не является словарём.

        Notes:
            - Файл сохраняется в кодировке UTF-8
            - Существующий файл полностью перезаписывается
            - Пробелы в словах и переводах сохраняются как есть

        Examples:
            >>> loader = TextFileLoader(file_path="./output.txt")
            >>> words_to_save = {"cat": "кошка", "dog": "собака"}
            >>> loader.save_words(words_to_save)
            Сохранено 2 слов в файл ./output.txt

            >>> # Проверка содержимого файла
            >>> with open("./output.txt", "r") as f:
            ...     print(f.read())
            cat,кошка
            dog,собака

            >>> # Попытка сохранить не словарь
            >>> loader.save_words(["not", "a", "dict"])
            Traceback (most recent call last):
                ...
            ValueError: Параметр `words` должен быть словарём, получен list
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
