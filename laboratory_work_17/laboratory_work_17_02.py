import shutil
import os


def copy_file(src: str, dst: str) -> bool:
    """
    Копирование файла

    Args:
        src: исходный файл
        dst: файл назначения

    Returns:
        True если успешно, False если ошибка
    """
    try:
        shutil.copy2(src, dst)  # copy2 сохраняет метаданные
        print(f"Файл '{src}' скопирован в '{dst}'")
        return True
    except FileNotFoundError:
        print(f"Файл '{src}' не найден")
        return False
    except Exception as e:
        print(f"Ошибка при копировании: {e}")
        return False


def copy_directory(src: str, dst: str) -> bool:
    """
    Копирование директории рекурсивно

    Args:
        src: исходная директория
        dst: директория назначения

    Returns:
        True если успешно, False если ошибка
    """
    try:
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        print(f"Директория '{src}' скопирована в '{dst}'")
        return True
    except Exception as e:
        print(f"Ошибка при копировании директории: {e}")
        return False


def delete_file(filename: str) -> bool:
    """
    Удаление файла

    Args:
        filename: имя файла

    Returns:
        True если успешно, False если ошибка
    """
    try:
        os.remove(filename)
        print(f"Файл '{filename}' удалён")
        return True
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден")
        return False
    except Exception as e:
        print(f"Ошибка при удалении: {e}")
        return False


def delete_directory(dirname: str) -> bool:
    """
    Удаление директории рекурсивно

    Args:
        dirname: имя директории

    Returns:
        True если успешно, False если ошибка
    """
    try:
        shutil.rmtree(dirname)
        print(f"Директория '{dirname}' удалена")
        return True
    except FileNotFoundError:
        print(f"Директория '{dirname}' не найдена")
        return False
    except Exception as e:
        print(f"Ошибка при удалении директории: {e}")
        return False