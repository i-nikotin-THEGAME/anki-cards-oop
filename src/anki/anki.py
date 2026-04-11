import copy


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

    def __str__(self) -> str:
        return f'Колода карт Anki, total_words: {len(self._words)}'
