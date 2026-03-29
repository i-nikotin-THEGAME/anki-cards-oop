import copy


class Anki:
    def __init__(self, *, words=None):
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
        Нормализует слово: удаляет пробелы по краям и приводит к нижнему
        регистру.
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
        """

        # Нормализуем и добавляем
        normalized_word = self.normalize_word(word)
        normalized_translation = self.normalize_word(translation)

        self._words[normalized_word] = normalized_translation

    def get_words(self):
        """
        Возвращает копию словаря со словами для защиты от внешних изменений.
        """
        return copy.deepcopy(self._words)
