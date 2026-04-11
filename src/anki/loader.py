from pathlib import Path
import json


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
            # Исправлено: добавляем тип полученного значения
            received_type = type(words).__name__
            raise ValueError(
                f"Параметр `words` должен быть словарём, "
                f"получен {received_type}"
                )

        with self._file_path.open("w", encoding="utf-8") as f:
            return self._save_to_file(words, f)

    def _load_from_file(self, file_object):
        """
        Реализует логику загрузки данных
        определённого формата из `file_object`.

        Метод должен быть переопределён в наследниках.

        Parameters
        ----------
        file_object : FileLike
            FileLike объект, из которого идёт чтение данных.

        Returns
        -------
        dict
            Словарь с загруженными словами.

        Raises
        ------
        NotImplementedError
            Если метод не переопределён в классе-наследнике.
        """
        raise NotImplementedError

    def _save_to_file(self, words, file_object):
        """
        Реализует логику сохранения слов
        в определённом формате в файл `file_object`.

        Метод должен быть переопределён в наследниках.

        Parameters
        ----------
        words : dict
            Словарь с словами и переводами.
        file_object : FileLike
            FileLike объект, в который производится запись данных.

        Returns
        -------
        None

        Raises
        ------
        NotImplementedError
            Если метод не переопределён в классе-наследнике.
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
        Загружает слова из текстового файла
        в формате CSV (разделитель - запятая).

        Parameters
        ----------
        file_object : FileLike
            Открытый файловый объект для чтения.

        Returns
        -------
        dict
            Словарь вида {"слово": "перевод"}.
        """
        words = {}
        for line in file_object:
            # Пропускаем пустые строки
            if not line.strip():
                continue

            try:
                # Разделяем только по первой запятой
                word, translation = line.split(",", 1)
                words[word.strip()] = translation.strip()
            except ValueError:
                # Пропускаем строки с некорректным форматом
                continue

        return words

    def _save_to_file(self, words, file_object):
        """
        Сохраняет словарь в текстовый файл
        в формате CSV (разделитель - запятая).

        Parameters
        ----------
        words : dict
            Словарь для сохранения.
        file_object : FileLike
            Открытый файловый объект для записи.

        Returns
        -------
        None
        """
        for word, translation in words.items():
            file_object.write(f'{word},{translation}\n')


class TSVFileLoader(BaseFileLoader):
    """
    Класс для загрузки и сохранения словаря слов из TSV-файла и в файл.

    Обеспечивает чтение данных из файла в формате "слово\\tперевод" и запись
    словаря обратно в файл. TSV (Tab-Separated Values) использует символ
    табуляции в качестве разделителя.

    Формат файла:
        Каждая строка содержит слово и его перевод,
        разделённые символом табуляции.
        Пример: "hello\\tпривет"

    Attributes:
        _file_path (Path): Защищённый атрибут, содержащий путь к файлу
                           в виде объекта pathlib.Path.

    Examples:
        >>> loader = TSVFileLoader(file_path="./my_words.tsv")
        >>> loader.save_words({"hello": "привет", "world": "мир"})
        >>> loaded_words = loader.load_words()
        >>> print(loaded_words)
        {'hello': 'привет', 'world': 'мир'}
    """
    DEFAULT_FILE_PATH = "./words.tsv"

    def _load_from_file(self, file_object):
        """
        Загружает слова из TSV-файла (разделитель - табуляция).

        Parameters
        ----------
        file_object : FileLike
            Открытый файловый объект для чтения.

        Returns
        -------
        dict
            Словарь вида {"слово": "перевод"}.
        """
        words = {}
        for line in file_object:
            # Пропускаем пустые строки
            if not line.strip():
                continue

            try:
                # Разделяем только по первому табу
                word, translation = line.split("\t", 1)
                words[word.strip()] = translation.strip()
            except ValueError:
                # Пропускаем строки с некорректным форматом
                continue

        return words

    def _save_to_file(self, words, file_object):
        """
        Сохраняет словарь в TSV-файл (разделитель - табуляция).

        Parameters
        ----------
        words : dict
            Словарь для сохранения.
        file_object : FileLike
            Открытый файловый объект для записи.

        Returns
        -------
        None
        """
        for word, translation in words.items():
            file_object.write(f'{word}\t{translation}\n')


class JsonFileLoader(BaseFileLoader):
    """
    Класс для загрузки и сохранения словаря слов из JSON-файла и в файл.

    Обеспечивает чтение данных из JSON-файла, который должен содержать
    объект (словарь) с парами "слово": "перевод". Запись словаря обратно
    в файл выполняется в форматированном JSON-виде.

    Формат файла:
        JSON-объект с ключами-словами и значениями-переводами.
        Пример: {"hello": "привет", "world": "мир"}

    Attributes:
        _file_path (Path): Защищённый атрибут, содержащий путь к файлу
                           в виде объекта pathlib.Path.

    Examples:
        >>> loader = JsonFileLoader(file_path="./my_words.json")
        >>> loader.save_words({"hello": "привет", "world": "мир"})
        >>> loaded_words = loader.load_words()
        >>> print(loaded_words)
        {'hello': 'привет', 'world': 'мир'}
    """
    DEFAULT_FILE_PATH = "./words.json"

    def _load_from_file(self, file_object):
        """
        Загружает словарь из JSON-файла.

        Parameters
        ----------
        file_object : FileLike
            Открытый файловый объект для чтения.

        Returns
        -------
        dict
            Словарь вида {"слово": "перевод"}.

        Notes
        -----
        Если JSON-файл содержит не словарь, а другой тип данных,
        метод вернёт пустой словарь.
        """
        try:
            data = json.load(file_object)
            # Проверяем, что загруженные данные являются словарём
            if isinstance(data, dict):
                return data
            else:
                # Если в JSON не словарь, возвращаем пустой словарь
                return {}
        except json.JSONDecodeError:
            # При ошибке парсинга JSON возвращаем пустой словарь
            return {}

    def _save_to_file(self, words, file_object):
        """
        Сохраняет словарь в JSON-файл с форматированием.

        Параметры форматирования:
            - indent=2: создаёт читаемый JSON с отступами в 2 пробела
            - ensure_ascii=False: сохраняет кириллицу и другие Unicode-символы
              в исходном виде, а не в виде escape-последовательностей

        Parameters
        ----------
        words : dict
            Словарь для сохранения.
        file_object : FileLike
            Открытый файловый объект для записи.

        Returns
        -------
        None

        Examples
        --------
        >>> loader = JsonFileLoader()
        >>> loader.save_words({"привет": "hello", "мир": "world"}, file)
        # В файл будет записано:
        # {
        #   "привет": "hello",
        #   "мир": "world"
        # }
        """
        json.dump(words, file_object, indent=2, ensure_ascii=False)
