import pytest
# import os
# import pathlib
from anki.loader import TextFileLoader

"""
Фикстура
"""
# @pytest.fixture()
# def tmp_file():
#     # Создаём объект пути до файла.
#     path = pathlib.Path("./test_words.txt")
#     # Сохраняем слова в файл.
#     path.write_text("hello,привет\n", encoding="utf-8")
#     # Возвращаем путь до файла из фикстуры.
#     yield str(path)

#     # Удаляем созданный ранее файл.
#     os.remove(path)


"""
Встроенные фикстуры
"""


@pytest.fixture()
def tmp_file(tmp_path):
    # Создаём объект пути до файла.
    path = tmp_path / "test_words.txt"
    # Сохраняем в файл слова.
    path.write_text("hello,привет\n", encoding="utf-8")
    # Возвращаем путь до файла из фикстуры.
    return str(path)


# def test_load_words_loads_words_from_comma_separated_values(tmp_file):
#     """Метод `load_words` класса `TextFileLoader` должен выполнить
#     загрузку слов из файла, путь до которого передан
#     при инициализации экземпляра класса `TextFileLoader`.
#     """
#     loader = TextFileLoader(file_path=tmp_file)
#     words = loader.load_words()
#     assert words == {"hello": "привет"}


@pytest.fixture
def temp_file(tmp_path):
    """Создаёт временный файл и возвращает путь к нему."""
    file_path = tmp_path / "test_words.txt"
    return str(file_path)


@pytest.mark.parametrize(
    "words_to_save, expected_content",
    [
        (
            {"hello": "привет"},
            "hello,привет\n"
        ),
        (
            {"hello": "привет", "world": "мир"},
            "hello,привет\nworld,мир\n"
        ),
        (
            {"  hello  ": "  привет  "},
            "  hello  ,  привет  \n"
        ),
        (
            {"Python": "Питон", "test": "тест"},
            "Python,Питон\ntest,тест\n"
        ),
        (
            {},
            ""
        ),
    ]
)
def test_save_words_saves_words_as_comma_separated_values(
        temp_file, words_to_save, expected_content
):
    """Проверяет, что слова сохраняются в файл в формате «слово,перевод»."""
    loader = TextFileLoader(file_path=temp_file)
    loader.save_words(words_to_save)

    # Проверяем содержимое файла
    with open(temp_file, "r", encoding="utf-8") as f:
        content = f.read()

    assert content == expected_content


@pytest.mark.parametrize(
    "invalid_input, expected_type",
    [
        (["hello", "привет"], "list"),
        ("not a dict", "str"),
        (123, "int"),
        (None, "NoneType"),
    ]
)
def test_save_words_raises_value_error_on_invalid_input(
        temp_file, invalid_input, expected_type
):
    """Проверяет, что передача в save_words не словаря вызывает ValueError."""
    loader = TextFileLoader(file_path=temp_file)

    with pytest.raises(
        ValueError,
        match=f"Параметр `words` должен быть словарём, получен {expected_type}"
    ):
        loader.save_words(invalid_input)


def test_save_words_overwrites_existing_file(temp_file):
    """Проверяет, что save_words перезаписывает существующий файл."""
    loader = TextFileLoader(file_path=temp_file)

    # Первое сохранение
    first_words = {"first": "первый"}
    loader.save_words(first_words)

    # Второе сохранение с другими данными
    second_words = {"second": "второй"}
    loader.save_words(second_words)

    # Проверяем содержимое файла
    with open(temp_file, "r", encoding="utf-8") as f:
        content = f.read()

    assert content == "second,второй\n"
    assert "first" not in content


def test_save_words_creates_file_if_not_exists(temp_file):
    """Проверяет, что save_words создаёт файл, если его не существует."""
    # Убеждаемся, что файла нет
    assert not __import__("pathlib").Path(temp_file).exists()

    loader = TextFileLoader(file_path=temp_file)
    words = {"test": "тест"}
    loader.save_words(words)

    # Проверяем, что файл создан
    assert __import__("pathlib").Path(temp_file).exists()

    # Проверяем содержимое
    with open(temp_file, "r", encoding="utf-8") as f:
        content = f.read()

    assert content == "test,тест\n"


def test_load_words_loads_words_from_comma_separated_values(temp_file):
    """Проверяет загрузку слов из файла."""
    # Создаём файл с тестовыми данными
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write("hello,привет\nworld,мир\n")

    loader = TextFileLoader(file_path=temp_file)
    words = loader.load_words()

    assert words == {"hello": "привет", "world": "мир"}
