def main():
    """Основная функция для демонстрации работы всех модулей"""

    print("=" * 60)
    print("ЛАБОРАТОРНАЯ РАБОТА №17")
    print("Базовое администрирование Linux с использованием Python")
    print("=" * 60)

    # Создание тестовых файлов для демонстрации
    print("\nПодготовка тестовых файлов...")
    with open("test_file.txt", "w") as f:
        f.write("Тестовый файл для лабораторной работы №17")
    os.makedirs("test_dir", exist_ok=True)
    with open("test_dir/test.txt", "w") as f:
        f.write("Вложенный файл")

    # 1. Управление пользователями
    print("\n" + "=" * 60)
    print("1. УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ")
    print("=" * 60)

    users = list_users()
    print(f"Существующие пользователи: {users[:5] if len(users) > 5 else users}")
    print("   (Для реального создания пользователей необходимы права sudo)")

    # 2. Работа с файлами
    print("\n" + "=" * 60)
    print("2. РАБОТА С ФАЙЛАМИ И ДИРЕКТОРИЯМИ")
    print("=" * 60)

    copy_file("test_file.txt", "test_file_copy.txt")
    copy_directory("test_dir", "test_dir_copy")
    delete_file("test_file_copy.txt")

    # 3. Мониторинг ресурсов
    print("\n" + "=" * 60)
    print("3. МОНИТОРИНГ СИСТЕМНЫХ РЕСУРСОВ")
    print("=" * 60)

    print_system_info()
    print_top_processes(5)
    monitor_resources(interval=2, duration=10)

    # 4. Планировщик задач
    print("\n" + "=" * 60)
    print("4. ПЛАНИРОВЩИК ЗАДАЧ")
    print("=" * 60)

    schedule.every(5).seconds.do(lambda: print("Разовое задание выполнено!"))
    schedule.every(10).seconds.do(lambda: print("Запланированное задание!"))

    print("Планировщик запущен на 15 секунд...")
    start_time = time.time()
    while time.time() - start_time < 15:
        schedule.run_pending()
        time.sleep(1)

    schedule.clear()

    # 5. Резервное копирование
    print("\n" + "=" * 60)
    print("5. РЕЗЕРВНОЕ КОПИРОВАНИЕ")
    print("=" * 60)

    create_backup("test_dir", "backups")

    # 6. Изменение прав доступа
    print("\n" + "=" * 60)
    print("6. ИЗМЕНЕНИЕ ПРАВ ДОСТУПА")
    print("=" * 60)

    print_permissions("test_file.txt")
    change_permissions("test_file.txt", 0o644)
    print_permissions("test_file.txt")

    # Очистка тестовых файлов
    print("\nОчистка тестовых файлов...")
    delete_file("test_file.txt")
    delete_directory("test_dir")
    delete_directory("test_dir_copy")
    delete_directory("backups")

    print("\n" + "=" * 60)
    print("ЛАБОРАТОРНАЯ РАБОТА №17 ВЫПОЛНЕНА")
    print("=" * 60)


if __name__ == "__main__":
    main()