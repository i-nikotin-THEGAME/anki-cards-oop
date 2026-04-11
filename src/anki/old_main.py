import random
import sys
import time
# from typing import Dict, Tuple


STOP_WORD = "СТОП"


def load_words(filename="words.txt"):
    """
    Загружает словарь из текстового файла.

    Args:
        filename (str): Имя файла для загрузки. По умолчанию 'words.txt'.

    Returns:
        dict: Словарь, где ключ — слово, значение — перевод.

    Raises:
        SystemExit: Если файл не найден, программа завершается.

    Example:
        >>> words = load_words("dictionary.txt")
        >>> print(words["hello"])
        привет
    """
    try:
        words = {}
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                parts = line.split(",")
                if len(parts) == 2:
                    word = parts[0].strip()
                    translation = parts[1].strip()
                    if word and translation:
                        words[word] = translation
        return words
    except FileNotFoundError:
        print(f"Ошибка: файл '{filename}' не найден")
        sys.exit(1)


def print_statistics(score, total_time):
    """
    Выводит статистику игровой сессии.

    Args:
        score (int): Количество правильных ответов.
        total_time (float): Общее время игры.

    Returns:
        None

    Example:
        >>> print_statistics(2, 19.85)
        Ваш итоговый счёт: 2
        Время игры: 19.85 секунд (среднее время: 9.92 сек.)
    """
    print(f"Ваш итоговый счет: {score}")
    if score > 0:
        average_time = total_time / score
        print(
            f"Время игры: {total_time:.2f} секунд "
            f"(среднее время: {average_time:.2f} сек.)"
        )
    else:
        print(f"Время игры: {total_time:.2f} секунд (среднее время: —)")


def ask_and_check(word, correct):
    """
    Запрашивает перевод слова, проверяет правильность и возвращает результаты.

    Args:
        word (str): Слово для перевода.
        correct (str): Правильный перевод.

    Returns:
        Tuple[bool, bool, float]: (need_exit, is_correct, answer_time)
            - need_exit: True если введено STOP слово, иначе False
            - is_correct: True если ответ правильный, иначе False
            - answer_time: время ответа в секундах (0.0 если need_exit=True)

    Example:
        >>> ask_and_check("кот", "cat")
        Ваше слово: кот
        Ваш перевод: cat
        (False, True, 1.23)
    """
    print(f"Ваше слово: {word}")
    start_time = time.time()
    user_answer = input("Ваш перевод: ").strip()
    elapsed_time = time.time() - start_time

    if user_answer.upper() == STOP_WORD:
        return True, False, 0.0

    is_correct = user_answer.lower() == correct.lower()
    return False, is_correct, elapsed_time


def start_game(words):
    """
    Запускает игровой режим, в котором пользователь переводит случайные слова.

    Args:
        words (dict): Словарь, где ключ — слово, значение — перевод.

    Returns:
        None

    Example:
        >>> words = {'отец': 'father', 'кот': 'cat'}
        >>> start_game(words)
        # Чтобы закончить, введите СТОП
        # Ваше слово: кот
        # Ваш перевод: cat
        # Верно! Время на ответ: 1.23 секунд
        # ...
        # Спасибо за игру!
        # Ваш итоговый счёт: 2
        # Время игры: 5.67 секунд (среднее время: 2.84 сек.)
    """
    if not words:
        print("Словарь пуст. Добавьте слова перед началом игры.")
        return

    print(f"Чтобы закончить, введите {STOP_WORD}")

    score = 0
    total_time = 0

    while True:
        word = random.choice(list(words.keys()))
        correct_translation = words[word]

        need_exit, is_correct, answer_time = ask_and_check(
            word, correct_translation)

        if need_exit:
            break

        total_time += answer_time

        if is_correct:
            print(f"Верно! Время на ответ: {answer_time:.2f} секунд")
            score += 1
        else:
            print(
                f"Неправильно, правильный ответ: {correct_translation}"
                f" (Время на ответ: {answer_time:.2f} секунд)"
            )
    print("Спасибо за игру!")
    print_statistics(score, total_time)


def train_until_mistake(words):
    """
    Запускает игровой режим "до первой ошибки".

    Args:
        words (dict): Словарь, где ключ — слово, значение — перевод.

    Returns:
        None

    Example:
        >>> words = {'стол': 'table', 'собака': 'dog'}
        >>> train_until_mistake(words)
        Режим: Игра до первой ошибки! Чтобы выйти вручную, введите СТОП
        # Ваше слово: стол
        # Ваш перевод: table
        # Верно! Всего очков: 1 (ответ за 2.97 секунд)
        # ...
    """
    if not words:
        print("Словарь пуст. Добавьте слова перед началом игры.")
        return

    print("Режим: Игра до первой ошибки! Чтобы выйти вручную, введите СТОП\n")

    words_list = list(words.keys())
    score = 0
    total_time = 0

    while True:
        word = random.choice(words_list)
        correct_translation = words[word]

        need_exit, is_correct, answer_time = ask_and_check(
            word, correct_translation)

        total_time += answer_time

        if need_exit:
            print("Выход из режима по запросу пользователя.\n")
            break

        if is_correct:
            score += 1
            print(
                f"Верно! Всего очков: {score}"
                f" (ответ за {answer_time:.2f} секунд)\n")
        else:
            print(f"Ошибка! Неверно. Правильный ответ: {correct_translation}")
            break
    print()
    print_statistics(score, total_time)


def add_words(words):
    """
    Добавляет новые пары слово-перевод в словарь в интерактивном режиме.

    Args:
        words (dict): Словарь, в который добавляются новые пары.

    Returns:
        None. Словарь изменяется по месту.

    Example:
        >>> words = {}
        >>> add_words(words)
        # Введите слово: cat
        # Введите перевод: кот
        # Введите слово: СТОП
        >>> print(words)
        {'cat': 'кот'}
    """
    print(f"Для завершения введите: {STOP_WORD}")
    while True:
        word = input("Введите слово: ").strip()
        if word.upper() == STOP_WORD:
            break
        translation = input("Введите перевод: ").strip()
        if translation.upper() == STOP_WORD:
            break
        words[word] = translation


def show_all_words(words):
    """
    Выводит все пары слово-перевод из словаря в одну строку.

    Args:
        words (dict): Словарь, где ключ — слово, значение — перевод.

    Returns:
        None

    Example:
        >>> words = {'cat': 'кот', 'dog': 'собака', 'tree': 'дерево'}
        >>> show_all_words(words)
        cat - кот; dog - собака; tree - дерево
    """
    pairs = [f"{word} - {translation}" for word, translation in words.items()]
    print("; ".join(pairs))


def save_words(words, filename="words.txt"):
    """
    Сохраняет словарь в текстовый файл.

    Args:
        words (dict): Словарь, где ключ — слово, значение — перевод.
        filename (str): Имя файла для сохранения. По умолчанию 'words.txt'.

    Returns:
        None

    Example:
        >>> words = {"hello": "привет", "world": "мир"}
        >>> save_words(words, "dictionary.txt")
        Было сохранено 2 слов в файл dictionary.txt
    """
    with open(filename, "w", encoding="utf-8") as file:
        for word, translation in words.items():
            file.write(f"{word}, {translation}\n")
    print(f"Было сохранено {len(words)} слов в файл {filename}")


def main():
    """
    Главное меню программы-тренажёра для изучения слов.

    Действия:
        - Загружает словарь из файла 'words.txt'
        - Выводит количество загруженных слов
        - Запускает бесконечный цикл меню с выбором режимов
        - Обрабатывает выбор пользователя и вызывает соответствующие функции
        - При выходе сохраняет словарь и завершает программу

    Пункты меню:
        1. Начать игру (start_game)
        2. Добавить слова (add_words)
        3. Тренировка до первой ошибки (train_until_mistake)
        4. Вывод всех слов (show_all_words)
        5. Выход (сохранение и завершение)
    """
    words = load_words()
    print(f"Было загружено {len(words)} слов из файла words.txt\n")

    while True:
        menu = """Меню:
        1. Начать игру
        2. Добавить слова
        3. Тренировка до первой ошибки
        4. Вывод всех слов
        5. Выход
        """
        print(menu)
        menu_choice = input("Пункт меню: ").strip()

        if menu_choice == "1":
            start_game(words)
        elif menu_choice == "2":
            add_words(words)
        elif menu_choice == "3":
            train_until_mistake(words)
        elif menu_choice == "4":
            show_all_words(words)
        elif menu_choice == "5":
            save_words(words)
            sys.exit()
        else:
            print("Неизвестный пункт меню. "
                  + "Пожалуйста, выберите число от 1 до 5.\n")


if __name__ == "__main__":
    main()
