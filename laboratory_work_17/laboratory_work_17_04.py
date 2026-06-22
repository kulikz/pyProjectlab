import schedule
import time
from datetime import datetime


def scheduled_task() -> None:
    """Пример задачи, выполняемой по расписанию"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Запланированная задача выполнена!")


def run_backup_schedule(source: str, backup: str, time_str: str = "00:00") -> None:
    """
    Настройка регулярного резервного копирования по расписанию

    Args:
        source: исходная директория
        backup: директория для резервной копии
        time_str: время выполнения (формат "ЧЧ:ММ")
    """

    def backup_job():
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_with_date = f"{backup}_{timestamp}"
            shutil.copytree(source, backup_with_date)
            print(f"[{datetime.now()}] Резервная копия создана: {backup_with_date}")
        except Exception as e:
            print(f"[{datetime.now()}] Ошибка резервного копирования: {e}")

    schedule.every().day.at(time_str).do(backup_job)
    print(f"Запланировано резервное копирование каждый день в {time_str}")


def run_monitoring_schedule(interval_minutes: int = 5) -> None:
    """
    Настройка регулярного мониторинга по расписанию

    Args:
        interval_minutes: интервал в минутах
    """

    def monitoring_job():
        print(f"\n[{datetime.now()}] ПЛАНОВЫЙ МОНИТОРИНГ:")
        cpu = get_cpu_usage()
        mem = get_memory_usage()
        print(f"   CPU: {cpu}%, Память: {mem['percent']}%")

    schedule.every(interval_minutes).minutes.do(monitoring_job)
    print(f"Запланирован мониторинг каждые {interval_minutes} минут")


def run_scheduler(duration: int = 60) -> None:
    """
    Запуск планировщика задач

    Args:
        duration: продолжительность работы в секундах
    """
    print(f"\nПланировщик задач запущен (будет работать {duration} секунд)")
    print("   Нажмите Ctrl+C для досрочного завершения\n")

    start_time = time.time()
    while time.time() - start_time < duration:
        schedule.run_pending()
        time.sleep(1)

    print("\nПланировщик задач завершил работу")