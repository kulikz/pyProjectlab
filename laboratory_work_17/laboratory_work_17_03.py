import psutil
import time
from datetime import datetime


def get_cpu_usage() -> float:
    """Получение загрузки CPU в процентах"""
    return psutil.cpu_percent(interval=1)


def get_memory_usage() -> dict:
    """Получение информации об использовании памяти"""
    mem = psutil.virtual_memory()
    return {
        'total': mem.total,
        'available': mem.available,
        'percent': mem.percent,
        'used': mem.used,
        'free': mem.free
    }


def get_disk_usage(path: str = '/') -> dict:
    """Получение информации об использовании диска"""
    disk = psutil.disk_usage(path)
    return {
        'total': disk.total,
        'used': disk.used,
        'free': disk.free,
        'percent': disk.percent
    }


def get_processes(top_n: int = 10) -> list:
    """
    Получение списка запущенных процессов

    Args:
        top_n: количество процессов для вывода (по умолчанию 10)

    Returns:
        список процессов, отсортированных по использованию CPU
    """
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
    return processes[:top_n]


def monitor_resources(interval: int = 5, duration: int = 30) -> None:
    """
    Мониторинг ресурсов системы в реальном времени

    Args:
        interval: интервал между замерами (секунды)
        duration: общая продолжительность мониторинга (секунды)
    """
    print("\n" + "=" * 60)
    print("МОНИТОРИНГ СИСТЕМНЫХ РЕСУРСОВ")
    print("=" * 60)

    start_time = time.time()
    iterations = 0

    while time.time() - start_time < duration:
        iterations += 1
        print(f"\n--- Замер #{iterations} [{datetime.now().strftime('%H:%M:%S')}] ---")

        cpu = get_cpu_usage()
        print(f"CPU загружен на: {cpu}%")

        mem = get_memory_usage()
        print(f"Оперативная память: {mem['percent']}% использовано "
              f"({mem['used'] // (1024 ** 2)} МБ / {mem['total'] // (1024 ** 2)} МБ)")

        disk = get_disk_usage('/')
        print(f"Диск (/) заполнен на: {disk['percent']}% "
              f"({disk['used'] // (1024 ** 3)} ГБ / {disk['total'] // (1024 ** 3)} ГБ)")

        time.sleep(interval)

    print("\nМониторинг завершён")


def print_system_info() -> None:
    """Вывод подробной информации о системе"""
    print("\n" + "=" * 60)
    print("ИНФОРМАЦИЯ О СИСТЕМЕ")
    print("=" * 60)

    print(f"\nПРОЦЕССОР:")
    print(f"   Физические ядра: {psutil.cpu_count(logical=False)}")
    print(f"   Логические ядра: {psutil.cpu_count(logical=True)}")
    print(f"   Текущая частота: {psutil.cpu_freq().current / 1000:.0f} МГц")

    mem = get_memory_usage()
    print(f"\nОПЕРАТИВНАЯ ПАМЯТЬ:")
    print(f"   Всего: {mem['total'] // (1024 ** 2)} МБ")
    print(f"   Доступно: {mem['available'] // (1024 ** 2)} МБ")
    print(f"   Использовано: {mem['percent']}%")

    disk = get_disk_usage('/')
    print(f"\nДИСК (/):")
    print(f"   Всего: {disk['total'] // (1024 ** 3)} ГБ")
    print(f"   Использовано: {disk['used'] // (1024 ** 3)} ГБ ({disk['percent']}%)")
    print(f"   Свободно: {disk['free'] // (1024 ** 3)} ГБ")


def print_top_processes(n: int = 10) -> None:
    """Вывод списка топ процессов по использованию CPU"""
    print(f"\nТОП-{n} ПРОЦЕССОВ ПО ИСПОЛЬЗОВАНИЮ CPU:")
    print("-" * 60)
    print(f"{'PID':>8} {'CPU%':>8} {'MEM%':>8} {'ИМЯ'}")
    print("-" * 60)

    processes = get_processes(n)
    for proc in processes:
        cpu = proc.get('cpu_percent', 0)
        mem = proc.get('memory_percent', 0)
        pid = proc.get('pid', 0)
        name = proc.get('name', 'unknown')[:40]
        print(f"{pid:>8} {cpu:>7.1f}% {mem:>7.1f}% {name}")