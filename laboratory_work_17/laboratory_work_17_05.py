import shutil
import os
from datetime import datetime


def create_backup(source: str, backup_dir: str) -> bool:
    """
    Создание резервной копии с меткой времени

    Args:
        source: исходная директория
        backup_dir: базовая директория для бэкапов

    Returns:
        True если успешно, False если ошибка
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"backup_{timestamp}")

        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        shutil.copytree(source, backup_path)
        print(f"Резервная копия создана: {backup_path}")
        return True
    except Exception as e:
        print(f"Ошибка создания резервной копии: {e}")
        return False


def restore_backup(backup_path: str, target: str) -> bool:
    """
    Восстановление из резервной копии

    Args:
        backup_path: путь к резервной копии
        target: целевая директория

    Returns:
        True если успешно, False если ошибка
    """
    try:
        if os.path.exists(target):
            shutil.rmtree(target)
        shutil.copytree(backup_path, target)
        print(f"Восстановление выполнено: {backup_path} -> {target}")
        return True
    except Exception as e:
        print(f"Ошибка восстановления: {e}")
        return False


def change_permissions(path: str, mode: int) -> bool:
    """
    Изменение прав доступа к файлу или директории

    Args:
        path: путь к файлу/директории
        mode: права доступа в восьмеричном формате (например, 0o755)

    Returns:
        True если успешно, False если ошибка
    """
    try:
        os.chmod(path, mode)
        print(f"Права доступа к '{path}' изменены на {oct(mode)}")
        return True
    except Exception as e:
        print(f"Ошибка изменения прав доступа: {e}")
        return False


def print_permissions(path: str) -> None:
    """Вывод текущих прав доступа"""
    try:
        stat_info = os.stat(path)
        print(f"Права доступа к '{path}': {oct(stat_info.st_mode)[-3:]}")
    except Exception as e:
        print(f"Ошибка получения прав доступа: {e}")