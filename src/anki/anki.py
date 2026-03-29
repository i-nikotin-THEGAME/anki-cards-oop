class Anki:
    def __init__(self, *, words=None):
        self.words = words if words is not None else {}
        if not isinstance(self.words, dict):
            raise ValueError('Значение параметра `words` должно быть словарём')

        # Проверка, что все ключи и значения — строки
        for key, value in self.words.items():
            if not isinstance(key, str):
                raise ValueError(
                    'Все ключи в словаре words должны быть строками')
            if not isinstance(value, str):
                raise ValueError(
                    'Все значения в словаре words должны быть строками')
