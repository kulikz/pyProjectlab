import subprocess


def add_user(username: str, comment: str = "") -> bool:
    """
    Создание нового пользователя

    Args:
        username: имя пользователя
        comment: комментарий (полное имя)

    Returns:
        True если успешно, False если ошибка
    """
    try:
        if comment:
            subprocess.run(['sudo', 'useradd', '-c', comment, username], check=True)
        else:
            subprocess.run(['sudo', 'useradd', username], check=True)
        print(f"Пользователь '{username}' успешно создан")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании пользователя '{username}': {e}")
        return False


def remove_user(username: str) -> bool:
    """
    Удаление пользователя

    Args:
        username: имя пользователя

    Returns:
        True если успешно, False если ошибка
    """
    try:
        subprocess.run(['sudo', 'userdel', '-r', username], check=True)
        print(f"Пользователь '{username}' успешно удалён")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при удалении пользователя '{username}': {e}")
        return False


def list_users() -> list:
    """
    Получение списка обычных пользователей

    Returns:
        список пользователей
    """
    try:
        result = subprocess.run(['getent', 'passwd'], capture_output=True, text=True)
        users = []
        for line in result.stdout.splitlines():
            parts = line.split(':')
            uid = int(parts[2])
            if uid >= 1000 and uid < 65534:  # Обычные пользователи
                users.append(parts[0])
        return users
    except Exception as e:
        print(f"Ошибка при получении списка пользователей: {e}")
        return []