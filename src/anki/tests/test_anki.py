import pytest   # Не забудьте добавить импорт библиотеки.
from anki.anki import Anki  # импорт из пакета anki, файла anki.py класса Anki


@pytest.mark.parametrize(
    "word, case, expected", [
        (
            "hello",
            "корректных данных",
            "hello"
        ),
        (
            "hello world",
            "отсутствия пробельных символов в начале или конце строки",
            "hello world"
        )
    ]
)
def test_normalize_word_method_returns_valid_input_unchanged(
        word, case, expected
):
    """Метод `normalize_word` класса `Anki` должен вернуть переданную строку
    неизменённой, если:
    - строка записана в нижнем регистре,
    - в начале и в конце строки нет пробелов.
    """
    assert Anki.normalize_word(word) == expected, (
        "Метод `normalize_word` должен возвращать неизменённую строку,"
        f" если {case}"
    )


@pytest.mark.parametrize(
    "word, expected", [
        ("pYtHoN", "python"),
        ("Hello World", "hello world"),
        ("   Python   ", "python"),
        ("\tHello World\n", "hello world")]
)
def test_normalize_word_method_normalizes_word(word, expected):
    """Метод `normalize_word` класса `Anki` должен выполнить нормализацию
    строки:
        - все символы приведены к нижнему регистру;
        - удалены пробелы в начале и в конце строки.
    """
    assert Anki.normalize_word(word) == expected, (
        "Метод `normalize_word` должен нормализовать"
        " некорректно отформатированные строки."
    )


@pytest.mark.parametrize('invalid_input', [
    1,
    [],
    set(),
])
def test_normalize_word_raises_ValueError_on_invalid_input(invalid_input):
    """Метод `normalize_word` класса `Anki` должен выдавать исключение
    `ValueError`, если в качестве значения параметра `word`
    передана не строка.
    """
    with pytest.raises(
        ValueError,
        match='Параметр `word` должен быть строкой'
    ):
        Anki.normalize_word(invalid_input)
        pytest.fail(
            "Метод `normalize_word` должен выдавать ValueError"
            " для нестроковых параметров"
        )


@pytest.mark.parametrize(
    "invalid_input, expected_error_message",
    [
        ("not a dict", "Значение параметра `words` должно быть словарём"),
        (
            ["hello", "привет"],
            "Значение параметра `words` должно быть словарём"
        ),
        (123, "Значение параметра `words` должно быть словарём"),
        (42.5, "Значение параметра `words` должно быть словарём"),
        (True, "Значение параметра `words` должно быть словарём"),
        (None, None),  # None не вызывает ошибку
        ({}, None),    # Пустой словарь не вызывает ошибку
    ]
)
def test_anki_init(invalid_input, expected_error_message):
    """Проверяет инициализацию Anki с разными параметрами."""
    if expected_error_message is None:
        # Ожидаем, что ошибки не будет
        Anki(words=invalid_input)
    else:
        # Ожидаем ошибку с конкретным сообщением
        with pytest.raises(ValueError, match=expected_error_message):
            Anki(words=invalid_input)


@pytest.mark.parametrize(
    "word, translation, expected_error_pattern",
    [
        ("hello", "привет", None),
        ("  world  ", "  мир  ", None),
        ("Python", "Питон", None),
        ("", "", None),
        ("   ", "   ", None),
        (123, "привет", "Параметр `word` должен быть строкой, получен int"),
        (
            ["hello"], "привет",
            "Параметр `word` должен быть строкой, получен list"
        ),
        (
            {"hello": "world"}, "привет",
            "Параметр `word` должен быть строкой, получен dict"
        ),
        (
            None, "привет",
            "Параметр `word` должен быть строкой, получен NoneType"
        ),
        (42.5, "привет", "Параметр `word` должен быть строкой, получен float"),
        (True, "привет", "Параметр `word` должен быть строкой, получен bool"),
        ("hello", 456, "Параметр `word` должен быть строкой, получен int"),
        (
            "hello", ["привет"],
            "Параметр `word` должен быть строкой, получен list"
        ),
        (
            "hello", {"привет": "hello"},
            "Параметр `word` должен быть строкой, получен dict"
        ),
        (
            "hello", None,
            "Параметр `word` должен быть строкой, получен NoneType"
        ),
        ("hello", 42.5, "Параметр `word` должен быть строкой, получен float"),
        ("hello", False, "Параметр `word` должен быть строкой, получен bool"),
    ]
)
def test_anki_add_word(word, translation, expected_error_pattern):
    """Проверяет добавление слов с разными параметрами."""
    anki = Anki()

    if expected_error_pattern is None:
        anki.add_word(word, translation)
    else:
        with pytest.raises(ValueError, match=expected_error_pattern):
            anki.add_word(word, translation)
