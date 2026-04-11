from pathlib import Path
# import sys


class BaseFileLoader:
    DEFAULT_FILE_PATH = "./words.txt"

    def __init__(self, file_path=None):
        if file_path is None:
            # Если путь не передали явно, используем значение
            # по умолчанию, определённое в теле класса.
            file_path = self.DEFAULT_FILE_PATH

        self._file_path = Path(file_path)

        if self._file_path.exists() and self._file_path.is_dir():
            raise ValueError(
                f"Путь {file_path} является директорией, а должен быть файлом"
            )

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
        if not self._file_path.exists():
            return {}

        with self._file_path.open("r", encoding="utf-8") as f:
            return self._load_from_file(f)

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
        if not isinstance(words, dict):
            raise ValueError("Значением параметра `words` должен быть словарь")

        with self._file_path.open("w", encoding="utf-8") as f:
            return self._save_to_file(words, f)

    def _load_from_file(self, file_object):
        """Реализует логику загрузки данных определённого формата
        из `file_object`.

        Метод должен быть переопределён в наследниках

        Parameters
        ----------
        file_object : FileLike
            FileLike объект, из которого идёт чтение данных

        Returns
        -------
        dict
            Словарь с загруженными словами
        """
        raise NotImplementedError

    def _save_to_file(self, words, file_object):
        """Реализует логику сохранения слов
        в определённом формате в файл `file_object`.

        Метод должен быть переопределён в наследниках

        Parameters
        ----------
        words : dict
            Словарь с словами и переводами
        file_object : FileLike
            FileLike объект, из которого идёт чтение данных

        Returns
        -------
        None
        """
        raise NotImplementedError


class TextFileLoader(BaseFileLoader):
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
    DEFAULT_FILE_PATH = "./words.txt"

    def _load_from_file(self, file_object):
        """
        """

        words = {}
        for line in file_object:
            word, translation = line.split(",")
            words[word.strip()] = translation.strip()
            return words

    def _save_to_file(self, words, file_object):
        for word, translation in words.items():
            file_object.write(f'{word},{translation}\n')


class TSVFileLoader(BaseFileLoader):
    """
    Реализует загрузку слов из TSV-файла и логику сохранения
    слов в TSV файл
    """
    DEFAULT_FILE_PATH = "./words.tsv"

    def _load_from_file(self, file_object):
        words = {}
        for line in file_object:
            word, translation = line.split("\t")
            words[word.strip()] = translation.strip()
        return words

    def _save_to_file(self, words, file_object):
        for word, translation in words.items():
            file_object.write(f'{word}\t{translation}\n')
