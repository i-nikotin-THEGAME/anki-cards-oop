import textwrap

# from anki.anki import Anki


class TextUI:
    MENU = textwrap.dedent("""\
        Меню:
        1. Начать игру
        2. Добавить слова
        3. Тренировка до первой ошибки
        4. Вывод всех слов
        5. Выход
    """)

    STOP_WORD = "выход"

    def __init__(self, anki_game):
        """
        Инициализирует экземпляр TextUI.

        Args:
            anki_game (Anki): Экземпляр класса Anki для работы со словами.

        Raises:
            ValueError: Если переданный аргумент не является экземпляром Anki.

        Examples:
            >>> anki = Anki()
            >>> ui = TextUI(anki)
        """
        # if not isinstance(anki_game, Anki):
        #     raise ValueError(
        #         "Аргумент должен быть экземпляром класса Anki"
        #     )

        self._anki_game = anki_game

    def start_game(self):
        """
        Запускает игру: показывает случайное слово и проверяет перевод.
        Игра продолжается до тех пор, пока пользователь не введёт STOP_WORD.

        Examples:
            >>> anki = Anki(words={"hello": "привет", "world": "мир"})
            >>> ui = TextUI(anki)
            >>> # Пользователь вводит: привет, мир, выход
        """
        print(f"Для выхода из игры введите '{self.STOP_WORD}'")
        print("\nИгра началась!")
        print("-" * 40)

        while True:
            try:
                # Получаем случайное слово
                word = self._anki_game.get_random_word()
                print(f"\nПереведите слово: {word}")

                # Получаем ответ пользователя
                user_answer = input("Ваш перевод: ").strip().lower()

                # Проверяем на выход
                if user_answer == self.STOP_WORD:
                    print("Выход из игры...")
                    break

                # Проверяем перевод
                if self._anki_game.check_translation(word, user_answer):
                    print("✓ Правильно! Поздравляю!")
                else:
                    correct = self._anki_game.get_translation(word)
                    print(f"✗ Неправильно. Правильный перевод: {correct}")

            except ValueError as e:
                print(f"Ошибка: {e}")
                print("Попробуйте снова.")
                break

    def add_words(self):
        """
        Добавляет новые слова в словарь.
        Пользователь вводит слово и перевод до тех пор,
        пока не введёт STOP_WORD.

        Examples:
            >>> anki = Anki()
            >>> ui = TextUI(anki)
            >>> # Пользователь вводит: hello, привет, python, питон, выход
        """
        print(f"Для завершения введите '{self.STOP_WORD}'")
        print("\nДобавление новых слов!")
        print("-" * 40)

        while True:
            word = input("\nВведите слово: ").strip()

            if word == self.STOP_WORD:
                print("Завершение добавления слов...")
                break

            translation = input("Введите перевод: ").strip()

            if translation == self.STOP_WORD:
                print("Завершение добавления слов...")
                break

            try:
                self._anki_game.add_word(word, translation)
                print(f"✓ Слово '{word}' успешно добавлено!")
            except ValueError as e:
                print(f"Ошибка: {e}")
                print("Попробуйте снова.")

    def show_words(self):
        """
        Выводит все слова и их переводы в формате "слово - перевод".

        Examples:
            >>> anki = Anki(words={"hello": "привет", "world": "мир"})
            >>> ui = TextUI(anki)
            >>> ui.show_words()
            hello - привет
            world - мир
        """
        words = self._anki_game.get_words()

        if not words:
            print("\nСловарь пуст. Добавьте слова через пункт меню 2.")
            return

        # print("\nСписок всех слов:")
        # print("-" * 40)

        for word, translation in words.items():
            print(f"{word} - {translation}")

        # print("-" * 40)

    def main_loop(self):
        """
        Главный цикл приложения: отображает меню и
        обрабатывает ввод пользователя.
        """
        while True:
            print(self.MENU)
            choice = input("Выберите пункт меню: ").strip()

            if choice == "1":
                self.start_game()
            elif choice == "2":
                self.add_words()
            elif choice == "3":
                print("\nДанная функциональность ещё не реализована")
            elif choice == "4":
                self.show_words()
            elif choice == "5":
                print("До свидания!")
                break
            else:
                print("Неверный ввод. Пожалуйста, выберите пункт от 1 до 5.")
