import argparse
# import pathlib

from anki.anki import Anki
from anki.loader import LoaderProtocol, loader_registry
from anki.ui import TextUI


class GameContext:
    """
    Контекстный менеджер для управления жизненным циклом игры.

    При входе в контекст загружает слова через загрузчик и добавляет их
    в экземпляр Anki. При выходе из контекста сохраняет текущее состояние
    словаря через загрузчик, даже если произошла ошибка.

    Attributes:
        loader (Any): Загрузчик слов (должен иметь методы load_words()
        и save_words())
        anki (Anki): Экземпляр класса Anki для управления словами

    Examples:
        >>> loader = TextFileLoader(file_path="./words.txt")
        >>> anki = Anki()
        >>> with GameContext(loader, anki):
        ...     ui = TextUI(anki)
        ...     ui.main_loop()
    """

    def __init__(self, loader, anki):
        """
        Инициализирует контекстный менеджер.

        Args:
            loader: Загрузчик с методами load_words() и save_words()
            anki: Экземпляр класса Anki
        """
        self.loader = loader
        self.anki = anki

    def __enter__(self):
        """
        Загружает слова через загрузчик и добавляет их в экземпляр Anki.

        Returns:
            GameContext: Сам контекстный менеджер
        """
        try:
            words = self.loader.load_words()
            if words:
                self.anki.words = words
        except Exception:
            # Если загрузка не удалась, продолжаем с пустым словарём
            pass
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Сохраняет текущее состояние словаря через загрузчик.

        Сохранение выполняется всегда, даже если в теле контекстного
        менеджера произошла ошибка.

        Args:
            exc_type: Тип исключения (если было)
            exc_val: Значение исключения
            exc_tb: Трассировка исключения

        Returns:
            bool: False, чтобы не подавлять исключения
        """
        try:
            self.loader.save_words(self.anki.words)
        except Exception:
            # Подавляем ошибки сохранения,
            # чтобы не перекрывать основное исключение
            pass
        return False  # Не подавляем исключения


def get_loader(source: str) -> LoaderProtocol:
    """
    Автоматические выбирает конкретную реализацию загрузчика,
    в зависимости от `source`.
    """

    loader_cls = loader_registry.get_loader(source)
    return loader_cls.from_source(source)


def main():
    # Создали объект парсера аргументов командной строки.
    parser = argparse.ArgumentParser(prog="anki")

    # Добавили новый аргумент.
    parser.add_argument(
        "--source", default="./words.txt",
        help="Путь до локального файла со словами или URL для загрузки JSON",
        metavar="SOURCE_PATH",
    )

    # Распарсили аргументы командной строки.
    args = parser.parse_args()

    loader = get_loader(args.source)
    anki = Anki()

    with GameContext(loader, anki):
        ui = TextUI(anki)
        ui.main_loop()


if __name__ == "__main__":
    main()
