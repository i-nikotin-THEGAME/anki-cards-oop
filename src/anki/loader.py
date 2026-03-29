from pathlib import Path


class TextFileLoader:
    def __init__(self, *, file_path="./words.txt"):
        # Преобразуем переданный путь в объект Path
        self.file_path = Path(file_path)

        # Проверяем, что путь не является директорией
        if self.file_path.is_dir():
            raise ValueError(
                f"Указанный путь '{file_path}' является директорией, "
                f"а должен быть файлом")
