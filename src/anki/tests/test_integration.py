from anki.loader import TextFileLoader
from anki.anki import Anki


def test_integration(tmp_path):
    """Проверяет полный сценарий работы приложения:
    загрузка слов из файла → создание Anki → добавление слова →
    сохранение в файл → проверка содержимого.
    """
    # Создаём временный файл с исходными словами
    file_path = tmp_path / "words.txt"
    initial_words = {"hello": "привет", "world": "мир"}

    with open(file_path, "w", encoding="utf-8") as f:
        for word, translation in initial_words.items():
            f.write(f"{word},{translation}\n")

    # 1. Создаём TextFileLoader с временным файлом
    loader = TextFileLoader(file_path=str(file_path))

    # 2. Загружаем слова методом load_words()
    loaded_words = loader.load_words()

    # 3. Создаём Anki с загруженными словами
    anki = Anki(words=loaded_words)

    # 4. Проверяем, что get_words() возвращает правильные слова
    assert anki.get_words() == initial_words

    # 5. Добавляем новое слово через add_word()
    new_word = "python"
    new_translation = "питон"
    anki.add_word(new_word, new_translation)

    # Проверяем, что слово добавилось
    expected_words = {**initial_words, new_word: new_translation}
    assert anki.get_words() == expected_words

    # 6. Сохраняем слова через save_words()
    loader.save_words(anki.get_words())

    # 7. Проверяем, что файл содержит все слова (исходные и новое)
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Проверяем содержимое файла
    expected_content = "hello,привет\nworld,мир\npython,питон\n"
    assert content == expected_content

    # Дополнительная проверка: загружаем слова заново и сравниваем
    reloaded_words = loader.load_words()
    assert reloaded_words == expected_words


def test_integration_empty_file(tmp_path):
    """Проверяет сценарий с пустым файлом."""
    file_path = tmp_path / "empty_words.txt"

    # Создаём пустой файл
    file_path.touch()

    loader = TextFileLoader(file_path=str(file_path))

    # Загружаем слова из пустого файла
    loaded_words = loader.load_words()

    # Создаём Anki с пустым словарём
    anki = Anki(words=loaded_words)
    assert anki.get_words() == {}

    # Добавляем слова
    anki.add_word("cat", "кошка")
    anki.add_word("dog", "собака")

    # Сохраняем
    loader.save_words(anki.get_words())

    # Проверяем содержимое файла
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    expected_content = "cat,кошка\ndog,собака\n"
    assert content == expected_content


def test_integration_normalization(tmp_path):
    """Проверяет сценарий с нормализацией слов."""
    file_path = tmp_path / "normalized_words.txt"

    # Создаём файл со словами в разных регистрах и пробелами
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("  Hello  ,  Привет  \n")
        f.write("WORLD,МИР\n")

    loader = TextFileLoader(file_path=str(file_path))
    loaded_words = loader.load_words()

    # Создаём Anki (он сам нормализует слова при инициализации)
    anki = Anki(words=loaded_words)

    # Проверяем, что слова нормализовались
    words = anki.get_words()
    assert words == {"hello": "привет", "world": "мир"}

    # Добавляем новое слово с пробелами
    anki.add_word("  PyThOn  ", "  ПиТоН  ")

    # Сохраняем
    loader.save_words(anki.get_words())

    # Проверяем, что в файле сохранились нормализованные версии
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Anki нормализует, но save_words сохраняет как есть
    # (нормализованные слова без лишних пробелов)
    assert "hello,привет" in content
    assert "world,мир" in content
    assert "python,питон" in content
