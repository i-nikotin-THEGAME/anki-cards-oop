from pathlib import Path
import json
from typing import Callable, Protocol, Self
import requests


class LoaderProtocol(Protocol):
    def load_words(self) -> dict[str, str]: ...
    def save_words(self, words: dict[str, str]) -> None: ...
    @classmethod
    def from_source(cls, source: str) -> Self: ...


class BaseFileLoader:
    DEFAULT_FILE_PATH = "./words.txt"

    def __init__(self, *, file_path=None):
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


class LoaderRegistry:

    def __init__(self) -> None:
        self._registry: dict[type[LoaderProtocol], Callable[[str], bool]] = {}

    def register(
        self,
        predicate: Callable[[str], bool],
    ) -> Callable[[type[LoaderProtocol]], type[LoaderProtocol]]:
        """Регистрирует класс загрузчик в реестре `self._registry`"""
        def decorator(cls: type[LoaderProtocol]) -> type[LoaderProtocol]:
            self._registry[cls] = predicate
            return cls
        return decorator

    def get_loader(self, source: str) -> type[LoaderProtocol]:
        """Выбирает конкретный класс загрузчика по идентификатору"""

        for loader_cls, predicate in self._registry.items():
            if predicate(source):
                return loader_cls

        raise ValueError(f"Неизвестный источник: {source}")


loader_registry = LoaderRegistry()


def is_txt_source(source: str) -> bool:
    return source.endswith(".txt")


def is_tsv_source(source: str) -> bool:
    return source.endswith(".tsv")


def is_json_source(source: str) -> bool:
    return source.endswith(".json")


def is_http_source(source: str) -> bool:
    return source.startswith("http")


@loader_registry.register(is_txt_source)
class TextFileLoader(BaseFileLoader):
    """
    Класс для загрузки и сохранения словаря слов из текстового файла и в файл.
    """
    DEFAULT_FILE_PATH = "./words.txt"

    @classmethod
    def from_source(cls, source: str) -> Self:
        """
        Создаёт экземпляр загрузчика из источника.

        Args:
            source (str): Путь к файлу.

        Returns:
            Self: Экземпляр TextFileLoader.
        """
        return cls(file_path=source)

    def _load_from_file(self, file_object):
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
        for word, translation in words.items():
            file_object.write(f'{word},{translation}\n')


@loader_registry.register(is_tsv_source)
class TSVFileLoader(BaseFileLoader):
    """
    Класс для загрузки и сохранения словаря слов из TSV-файла и в файл.
    """
    DEFAULT_FILE_PATH = "./words.tsv"

    @classmethod
    def from_source(cls, source: str) -> Self:
        """
        Создаёт экземпляр загрузчика из источника.

        Args:
            source (str): Путь к файлу.

        Returns:
            Self: Экземпляр TSVFileLoader.
        """
        return cls(file_path=source)

    def _load_from_file(self, file_object):
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
        for word, translation in words.items():
            file_object.write(f'{word}\t{translation}\n')


@loader_registry.register(is_json_source)
class JsonFileLoader(BaseFileLoader):
    """
    Класс для загрузки и сохранения словаря слов из JSON-файла и в файл.
    """
    DEFAULT_FILE_PATH = "./words.json"

    @classmethod
    def from_source(cls, source: str) -> Self:
        """
        Создаёт экземпляр загрузчика из источника.

        Args:
            source (str): Путь к файлу.

        Returns:
            Self: Экземпляр JsonFileLoader.
        """
        return cls(file_path=source)

    def _load_from_file(self, file_object):
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
        json.dump(words, file_object, indent=2, ensure_ascii=False)


@loader_registry.register(is_http_source)
class JsonNetworkLoader:
    """
    Загрузчик словарей из JSON по сети.
    """

    def __init__(self, url):
        self.url = url

    @classmethod
    def from_source(cls, source: str) -> Self:
        """
        Создаёт экземпляр загрузчика из источника (URL).

        Args:
            source (str): URL для загрузки JSON-файла.

        Returns:
            Self: Экземпляр JsonNetworkLoader.
        """
        return cls(url=source)

    def load_words(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Выбросит исключение при HTTP-ошибке

            data = response.json()

            # Проверяем, что загруженные данные являются словарём
            if isinstance(data, dict):
                return data
            else:
                print(
                    f"Предупреждение: данные по URL {self.url} "
                    "не являются словарём. Возвращаем пустой словарь.")
                return {}
        except (requests.RequestException, json.JSONDecodeError):
            # При любой ошибке возвращаем пустой словарь
            print(
                f"Предупреждение: ошибка при загрузке {self.url}. "
                "Возвращаем пустой словарь.")
            return {}

    def save_words(self, words):
        pass  # Метод-заглушка, ничего не делает
