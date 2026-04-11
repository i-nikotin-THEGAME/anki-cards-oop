import copy
import random


class Anki:
    """
    Класс для управления коллекцией слов и их переводов.

    Обеспечивает хранение, нормализацию и добавление слов с переводами.
    Все слова нормализуются (приводятся к нижнему регистру и удаляются пробелы)
    для обеспечения консистентности данных.

    Attributes:
        _words (dict): Защищённый словарь, где ключи — нормализованные слова,
                       значения — их нормализованные переводы.

    Examples:
        >>> anki = Anki(words={"Hello": "Привет", "  World  ": "  МИР  "})
        >>> anki.get_words()
        {'hello': 'привет', 'world': 'мир'}

        >>> anki.add_word("  Python  ", "  Питон  ")
        >>> anki.get_words()
        {'hello': 'привет', 'world': 'мир', 'python': 'питон'}
    """

    def __init__(self, *, words=None):
        """
        Инициализирует экземпляр Anki.

        Args:
            words (dict, optional): Словарь вида {"слово": "перевод"}.
                                    Если передан, все ключи и значения
                                    нормализуются. По умолчанию None
                                    (создаётся пустой словарь).

        Raises:
            ValueError: Если параметр words передан, но не является словарём.

        Examples:
            >>> anki1 = Anki()  # Пустой словарь
            >>> anki2 = Anki(words={"Cat": "Кошка"})
            >>> anki3 = Anki(words="not a dict")  # Вызовет ValueError
        """

        self._words = {}

        if words is not None:
            if not isinstance(words, dict):
                raise ValueError(
                    'Значение параметра `words` должно быть словарём')

            # Нормализуем все ключи и значения с помощью normalize_word
            for key, value in words.items():
                normalized_key = self.normalize_word(key)
                normalized_value = self.normalize_word(value)
                self._words[normalized_key] = normalized_value

    @staticmethod
    def normalize_word(word):
        """
        Нормализует слово: удаляет пробелы по краям и приводит
        к нижнему регистру.

        Args:
            word (str): Строка для нормализации.

        Returns:
            str: Нормализованная строка без пробелов по краям
            и в нижнем регистре.

        Raises:
            ValueError: Если переданное значение не является строкой.

        Examples:
            >>> Anki.normalize_word("  Hello World  ")
            'hello world'
            >>> Anki.normalize_word("PYTHON")
            'python'
            >>> Anki.normalize_word(123)
            Traceback (most recent call last):
                ...
            ValueError: Параметр `word` должен быть строкой, получен int
        """
        if not isinstance(word, str):
            raise ValueError(
                f'Параметр `word` должен быть строкой, получен '
                f'{type(word).__name__}'
            )

        return word.strip().lower()

    def add_word(self, word, translation):
        """
        Добавляет слово и его перевод в словарь.

        Перед добавлением оба параметра нормализуются с помощью
        normalize_word(). Если слово уже существует в словаре,
        его перевод будет перезаписан.

        Args:
            word (str): Слово для добавления.
            translation (str): Перевод слова.

        Raises:
            ValueError: Если word или translation не являются строками.

        Examples:
            >>> anki = Anki()
            >>> anki.add_word("Apple", "Яблоко")
            >>> anki.add_word("  Apple  ", "  ЯБЛОКО  ")\
                # Перезапишет с нормализацией
            >>> anki.get_words()
            {'apple': 'яблоко'}
        """

        # Нормализуем и добавляем
        normalized_word = self.normalize_word(word)
        normalized_translation = self.normalize_word(translation)

        self._words[normalized_word] = normalized_translation

    def get_words(self):
        """
        Возвращает копию словаря со словами для защиты от внешних изменений.

        Возвращается глубокая копия словаря, чтобы предотвратить нежелательные
        изменения оригинальных данных через возвращённую ссылку.

        Returns:
            dict: Глубокая копия словаря вида {"слово": "перевод"}.

        Examples:
            >>> anki = Anki(words={"hello": "привет"})
            >>> words_copy = anki.get_words()
            >>> words_copy["hello"] = "изменено"  # Не влияет на оригинал
            >>> anki.get_words()
            {'hello': 'привет'}
        """

        return copy.deepcopy(self._words)

    # def __str__(self) -> str:
    #     return f'Колода карт Anki, total_words: {len(self._words)}'

    def __contains__(self, word):
        """
        Проверяет, содержится ли слово в словаре.

        Аргументы:
            word (str): Слово для проверки.

        Возвращает:
            bool: True, если слово есть в словаре, иначе False.

        Исключения:
            ValueError: Если word не является строкой.

        Примеры:
            >>> anki = Anki(words={"Python": "Питон"})
            >>> "python" in anki
            True
            >>> "TypeScript" in anki
            False
        """
        # Нормализуем искомое слово
        normalized_word = self.normalize_word(word)

        # Проверяем наличие в словаре
        return normalized_word in self._words

    def __str__(self):
        """
        Возвращает строковое представление объекта Anki.

        Возвращает:
            str: Информация о количестве слов в словаре.

        Примеры:
            >>> anki = Anki()
            >>> print(anki)
            Anki: 0 слов

            >>> anki = Anki(words={"hello": "привет", "world": "мир"})
            >>> print(anki)
            Anki: 2 слова
        """
        words_count = len(self._words)

        # Выбираем правильное склонение слова "слово"
        if words_count % 10 == 1 and words_count % 100 != 11:
            word_form = "слово"
        elif (
            2 <= words_count % 10 <= 4
            and not (12 <= words_count % 100 <= 14)
        ):
            word_form = "слова"
        else:
            word_form = "слов"

        return f"Колода карт Anki: {words_count} {word_form}"

    def get_random_word(self):
        """
        Возвращает случайное слово из словаря.

        Returns:
            str: Случайное слово из коллекции.

        Raises:
            ValueError: Если словарь пуст.

        Examples:
            >>> anki = Anki(words={"hello": "привет", "world": "мир"})
            >>> word = anki.get_random_word()
            >>> word in ["hello", "world"]
            True

            >>> anki = Anki()
            >>> anki.get_random_word()
            Traceback (most recent call last):
                ...
            ValueError: Невозможно получить случайное слово: словарь пуст
        """
        if not self._words:
            raise ValueError(
                "Невозможно получить случайное слово: словарь пуст"
            )

        return random.choice(list(self._words.keys()))

    def check_translation(self, word, translation):
        """
        Проверяет, правильный ли перевод указан для слова.

        Args:
            word (str): Слово для проверки.
            translation (str): Перевод, который нужно проверить.

        Returns:
            bool: True, если перевод верный, иначе False.

        Raises:
            ValueError: Если слово отсутствует в словаре.

        Examples:
            >>> anki = Anki(words={"hello": "привет", "world": "мир"})
            >>> anki.check_translation("hello", "привет")
            True
            >>> anki.check_translation("hello", "пока")
            False
            >>> anki.check_translation("python", "питон")
            Traceback (most recent call last):
                ...
            ValueError: Слово 'python' отсутствует в словаре
        """
        normalized_word = self.normalize_word(word)
        normalized_translation = self.normalize_word(translation)

        if normalized_word not in self._words:
            raise ValueError(
                f"Слово '{word}' отсутствует в словаре"
            )

        return self._words[normalized_word] == normalized_translation

    def get_translation(self, word):
        """
        Возвращает перевод указанного слова.

        Args:
            word (str): Слово, перевод которого нужно получить.

        Returns:
            str: Перевод слова.

        Raises:
            ValueError: Если слово отсутствует в словаре.

        Examples:
            >>> anki = Anki(words={"hello": "привет", "world": "мир"})
            >>> anki.get_translation("hello")
            'привет'
            >>> anki.get_translation("python")
            Traceback (most recent call last):
                ...
            ValueError: Слово 'python' отсутствует в словаре
        """
        normalized_word = self.normalize_word(word)

        if normalized_word not in self._words:
            raise ValueError(
                f"Слово '{word}' отсутствует в словаре"
            )

        return self._words[normalized_word]
