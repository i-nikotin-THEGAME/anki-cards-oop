import copy
import random
import time


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

            # Используем нормализацию через защищённый метод
            self._words = self._normalize_dict(words)

        # Начата ли сессия тренировки до первой ошибки.
        self._session_active = False
        # Время начала тренировки.
        self._session_start_time = 0.0
        # Количество правильных ответов.
        self._session_user_score = 0

        # Информация о последней тренировке.
        self.last_session_stats = {
            "correct_answers": 0,
            "total_time": 0.0,
        }

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

    def _normalize_dict(self, words_dict):
        """
        Нормализует все ключи и значения словаря.

        Защищённый метод для устранения дублирования кода.
        Используется в __init__ и в сеттере words.

        Args:
            words_dict (dict): Словарь для нормализации.

        Returns:
            dict: Новый словарь с нормализованными ключами и значениями.

        Raises:
            ValueError: Если words_dict не является словарём.

        Examples:
            >>> anki = Anki()
            >>> anki._normalize_dict({"Hello": "Привет", "  World  ": "  МИР  "})
            {'hello': 'привет', 'world': 'мир'}
        """
        if not isinstance(words_dict, dict):
            raise ValueError(
                f'Параметр `words_dict` должен быть словарём, получен '
                f'{type(words_dict).__name__}'
            )

        normalized = {}
        for key, value in words_dict.items():
            normalized_key = self.normalize_word(key)
            normalized_value = self.normalize_word(value)
            normalized[normalized_key] = normalized_value

        return normalized

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

    @property
    def words(self):
        """
        Геттер для атрибута words. Возвращает копию словаря _words.

        Returns:
            dict: Глубокая копия словаря вида {"слово": "перевод"}.

        Examples:
            >>> anki = Anki(words={"hello": "привет"})
            >>> words_copy = anki.words
            >>> words_copy["hello"] = "изменено"  # Не влияет на оригинал
            >>> anki.words
            {'hello': 'привет'}
        """
        return copy.deepcopy(self._words)

    @words.setter
    def words(self, value):
        """
        Сеттер для атрибута words. Валидирует и нормализует новый словарь.

        Args:
            value (dict): Новый словарь вида {"слово": "перевод"}.

        Raises:
            ValueError: Если value не является словарём или если попытка
                    замены словаря происходит во время активной тренировки.

        Examples:
            >>> anki = Anki()
            >>> anki.words = {"Hello": "Привет"}
            >>> anki.words
            {'hello': 'привет'}

            >>> anki.words = "not a dict"  # Вызовет ValueError
            Traceback (most recent call last):
                ...
            ValueError: Значением параметра `words` должен быть словарь
        """
        # Защита от замены словаря во время активной тренировки
        if self._session_active:
            raise ValueError(
                "Невозможно полностью заменить словарь во время активной тренировки. "
                "Сначала завершите тренировку."
            )

        # Валидация и нормализация через защищённый метод
        self._words = self._normalize_dict(value)

    def __len__(self):
        """
        Возвращает количество слов в словаре.

        Returns:
            int: Количество слов в коллекции.

        Examples:
            >>> anki = Anki()
            >>> len(anki)
            0
            >>> anki.add_word("hello", "привет")
            >>> len(anki)
            1
            >>> anki.add_word("world", "мир")
            >>> len(anki)
            2
        """
        return len(self._words)

    def __iter__(self):
        """
        Возвращает итератор по парам (слово, перевод).

        Returns:
            iterator: Итератор, возвращающий кортежи вида (слово, перевод).

        Examples:
            >>> anki = Anki(words={"hello": "привет", "world": "мир"})
            >>> list(anki)
            [('hello', 'привет'), ('world', 'мир')]

            >>> for word, translation in anki:
            ...     print(f"{word} -> {translation}")
            hello -> привет
            world -> мир
        """
        return iter(self._words.items())

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

        При активной сессии запоминает последнее выданное слово для
        последующей проверки.

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

        word = random.choice(list(self._words.keys()))

        # Если сессия активна, запоминаем выданное слово
        if self._session_active:
            self._last_word = word

        return word

    def check_translation(self, word, translation):
        """
        Проверяет, правильный ли перевод указан для слова.

        Args:
            word (str): Слово для проверки.
            translation (str): Перевод, который нужно проверить.

        Returns:
            bool: True, если перевод верный, иначе False.

        Raises:
            ValueError: Если слово отсутствует в словаре или при активной
                    сессии переданное слово не совпадает с последним
                    выданным словом.

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

        is_correct = self._words[normalized_word] == normalized_translation

        # Логика сессии
        if self._session_active:
            # Проверяем, что переданное слово совпадает с последним выданным
            if not hasattr(self, '_last_word') or self._last_word != normalized_word:
                # Завершаем сессию и выбрасываем исключение
                self.end_session()
                raise ValueError(
                    f"Ошибка тренировки: ожидалась проверка слова '{self._last_word if hasattr(self, '_last_word') else '?'}', "
                    f"а получено '{normalized_word}'. Тренировка завершена."
                )

            if is_correct:
                self._session_user_score += 1
                # Сбрасываем последнее слово, чтобы нельзя было проверить то же слово дважды
                self._last_word = None
            else:
                self.end_session()

        return is_correct

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

    def start_session(self):
        """Начинает новую тренировочную сессию."""
        if self._session_active:
            raise RuntimeError("Нельзя начать тренировку, если она уже начата")

        if not self._words:
            raise ValueError("Нельзя начать тренировку: словарь пуст")

        self._session_active = True
        self._session_start_time = time.time()
        self._session_user_score = 0
        self._last_word = None

    def end_session(self):
        """Завершает текущую тренировочную сессию."""
        if not self._session_active:
            raise RuntimeError("Нельзя завершить неактивную сессию")

        # Сохраняем статистику
        self.last_session_stats = {
            "correct_answers": self._session_user_score,
            "total_time": time.time() - self._session_start_time
        }

        # Сбрасываем состояние
        self._session_active = False
        self._session_user_score = 0
        self._session_start_time = 0.0
        self._last_word = None
