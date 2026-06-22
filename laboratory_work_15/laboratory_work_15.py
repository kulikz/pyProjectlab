import ctypes
import sys


class MyList:
    def __init__(self):
        self.length = 0
        self.capacity = 8
        self.array = (self.capacity * ctypes.py_object)()

    def append(self, item):
        """Добавляет элемент в конец списка"""
        if self.length == self.capacity:
            self._resize(self.capacity * 2)
        self.array[self.length] = item
        self.length += 1

    def insert(self, index, item):
        """
        Вставляет элемент в произвольное место списка

        Args:
            index: индекс, куда вставить элемент
            item: вставляемый элемент
        """
        # Корректировка индекса (отрицательные индексы)
        if index < 0:
            index = self.length + index + 1

        # Проверка границ
        if index < 0:
            index = 0
        if index > self.length:
            index = self.length

        # Если нужно, увеличиваем capacity
        if self.length == self.capacity:
            self._resize(self.capacity * 2)

        # Сдвигаем элементы вправо
        for i in range(self.length, index, -1):
            self.array[i] = self.array[i - 1]

        # Вставляем новый элемент
        self.array[index] = item
        self.length += 1

    def delete(self, index):
        """
        Удаляет элемент из произвольного места списка

        Args:
            index: индекс удаляемого элемента

        Returns:
            удалённый элемент
        """
        # Корректировка индекса (отрицательные индексы)
        if index < 0:
            index = self.length + index

        # Проверка границ
        if index < 0 or index >= self.length:
            raise IndexError("Индекс вне диапазона")

        # Сохраняем удаляемый элемент
        deleted_item = self.array[index]

        # Сдвигаем элементы влево
        for i in range(index, self.length - 1):
            self.array[i] = self.array[i + 1]

        self.length -= 1

        # Если нужно, уменьшаем capacity
        if self.length <= (self.capacity // 2) and self.capacity > 8:
            self._resize(max(self.capacity // 2, 8))

        return deleted_item

    def pop(self, index=None):
        """
        Удаляет элемент из списка

        Args:
            index: индекс удаляемого элемента (по умолчанию - последний)

        Returns:
            удалённый элемент
        """
        if index is None:
            # Удаляем последний элемент
            if self.length == 0:
                raise IndexError("Удаление из пустого списка")
            self.length -= 1
            deleted_item = self.array[self.length]

            # Оптимизация памяти
            if self.length <= (self.capacity // 2) and self.capacity > 8:
                self._resize(max(self.capacity // 2, 8))

            return deleted_item
        else:
            return self.delete(index)

    def remove(self, value):
        """
        Удаляет первое вхождение значения из списка

        Args:
            value: удаляемое значение

        Raises:
            ValueError: если значение не найдено
        """
        for i in range(self.length):
            if self.array[i] == value:
                self.delete(i)
                return
        raise ValueError(f"Значение {value} не найдено в списке")

    def clear(self):
        """Очищает список"""
        self.length = 0
        self.capacity = 8
        self.array = (self.capacity * ctypes.py_object)()

    def __len__(self):
        return self.length

    def __getitem__(self, index):
        if index < 0:
            index = self.length + index
        if index < 0 or index >= self.length:
            raise IndexError("Индекс вне диапазона")
        return self.array[index]

    def __setitem__(self, index, value):
        if index < 0:
            index = self.length + index
        if index < 0 or index >= self.length:
            raise IndexError("Индекс вне диапазона")
        self.array[index] = value

    def __contains__(self, item):
        for i in range(self.length):
            if self.array[i] == item:
                return True
        return False

    def index(self, value):
        """Возвращает индекс первого вхождения значения"""
        for i in range(self.length):
            if self.array[i] == value:
                return i
        raise ValueError(f"Значение {value} не найдено в списке")

    def __str__(self):
        if self.length == 0:
            return "[]"
        result = "["
        for i in range(self.length - 1):
            result += str(self.array[i]) + ", "
        result += str(self.array[self.length - 1]) + "]"
        return result

    def _resize(self, new_capacity):
        """Изменяет ёмкость списка"""
        new_array = (new_capacity * ctypes.py_object)()
        for index in range(self.length):
            new_array[index] = self.array[index]
        self.array = new_array
        self.capacity = new_capacity


# ===================== ДЕМОНСТРАЦИЯ РАБОТЫ =====================

if __name__ == "__main__":
    print("=" * 60)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ КЛАССА MyList")
    print("=" * 60)

    # Создаём список
    my_list = MyList()
    print(f"Создан пустой список: {my_list}")
    print(f"Длина: {len(my_list)}, Capacity: {my_list.capacity}")

    # Добавляем элементы через append
    print("\n" + "-" * 40)
    print("1. Добавление элементов (append):")
    for i in range(5):
        my_list.append(f"элемент_{i}")
        print(f"  Добавлен: элемент_{i} -> {my_list}")

    # Вставка в начало
    print("\n" + "-" * 40)
    print("2. Вставка в начало (insert(0, 'НОВЫЙ')):")
    my_list.insert(0, "НОВЫЙ_В_НАЧАЛО")
    print(f"  Результат: {my_list}")

    # Вставка в середину
    print("\n" + "-" * 40)
    print("3. Вставка в середину (insert(3, 'В_СЕРЕДИНУ')):")
    my_list.insert(3, "В_СЕРЕДИНУ")
    print(f"  Результат: {my_list}")

    # Вставка в конец
    print("\n" + "-" * 40)
    print("4. Вставка в конец (insert(100, 'В_КОНЕЦ')):")
    my_list.insert(100, "В_КОНЕЦ")
    print(f"  Результат: {my_list}")

    # Вставка с отрицательным индексом
    print("\n" + "-" * 40)
    print("5. Вставка с отрицательным индексом (insert(-2, 'ПРЕДПОСЛЕДНИЙ')):")
    my_list.insert(-2, "ПРЕДПОСЛЕДНИЙ")
    print(f"  Результат: {my_list}")

    # Удаление по индексу (delete)
    print("\n" + "-" * 40)
    print("6. Удаление по индексу (delete(2)):")
    deleted = my_list.delete(2)
    print(f"  Удалён элемент: '{deleted}'")
    print(f"  Результат: {my_list}")

    # Удаление последнего элемента (pop без индекса)
    print("\n" + "-" * 40)
    print("7. Удаление последнего элемента (pop()):")
    deleted = my_list.pop()
    print(f"  Удалён элемент: '{deleted}'")
    print(f"  Результат: {my_list}")

    # Удаление с отрицательным индексом
    print("\n" + "-" * 40)
    print("8. Удаление с отрицательным индексом (pop(-3)):")
    deleted = my_list.pop(-3)
    print(f"  Удалён элемент: '{deleted}'")
    print(f"  Результат: {my_list}")

    # Удаление по значению (remove)
    print("\n" + "-" * 40)
    print("9. Удаление по значению (remove('элемент_2')):")
    my_list.remove("элемент_2")
    print(f"  Результат: {my_list}")

    # Попытка удалить несуществующее значение
    print("\n" + "-" * 40)
    print("10. Попытка удалить несуществующее значение:")
    try:
        my_list.remove("НЕСУЩЕСТВУЮЩИЙ")
    except ValueError as e:
        print(f"  Ошибка: {e}")

    # Проверка наличия элемента
    print("\n" + "-" * 40)
    print("11. Проверка наличия элемента (__contains__):")
    print(f"  'элемент_1' в списке: {'элемент_1' in my_list}")
    print(f"  'элемент_999' в списке: {'элемент_999' in my_list}")

    # Получение индекса элемента
    print("\n" + "-" * 40)
    print("12. Получение индекса элемента (index):")
    if "элемент_3" in my_list:
        idx = my_list.index("элемент_3")
        print(f"  Индекс 'элемент_3': {idx}")

    # Изменение элемента по индексу
    print("\n" + "-" * 40)
    print("13. Изменение элемента по индексу (__setitem__):")
    my_list[1] = "ИЗМЕНЁННЫЙ"
    print(f"  Результат: {my_list}")

    # Получение элемента по индексу
    print("\n" + "-" * 40)
    print("14. Получение элемента по индексу (__getitem__):")
    print(f"  my_list[0] = '{my_list[0]}'")
    print(f"  my_list[-1] = '{my_list[-1]}'")

    # Очистка списка
    print("\n" + "-" * 40)
    print("15. Очистка списка (clear):")
    my_list.clear()
    print(f"  Результат: {my_list}")
    print(f"  Длина: {len(my_list)}")

    # Демонстрация автоматического изменения capacity
    print("\n" + "=" * 60)
    print("ДЕМОНСТРАЦИЯ АВТОМАТИЧЕСКОГО ИЗМЕНЕНИЯ CAPACITY")
    print("=" * 60)

    demo_list = MyList()
    print(f"Начальная capacity: {demo_list.capacity}")

    print("\nДобавление элементов (append):")
    for i in range(20):
        demo_list.append(i)
        print(f"  len={len(demo_list):2}, capacity={demo_list.capacity}")

    print("\nУдаление элементов (pop):")
    for i in range(20):
        demo_list.pop()
        print(f"  len={len(demo_list):2}, capacity={demo_list.capacity}")

    print("\n" + "=" * 60)
    print("СРАВНЕНИЕ С ВСТРОЕННЫМ СПИСКОМ PYTHON")
    print("=" * 60)

    # Сравнение с встроенным списком
    my_custom_list = MyList()
    python_list = []

    print("\nДобавление 10 элементов:")
    for i in range(10):
        my_custom_list.append(i)
        python_list.append(i)
        print(f"  MyList: {my_custom_list}")
        print(f"  Python list: {python_list}")

    print("\nВставка элемента 'ВСТАВКА' на позицию 3:")
    my_custom_list.insert(3, "ВСТАВКА")
    python_list.insert(3, "ВСТАВКА")
    print(f"  MyList: {my_custom_list}")
    print(f"  Python list: {python_list}")

    print("\nУдаление элемента с позиции 5:")
    deleted_custom = my_custom_list.pop(5)
    deleted_python = python_list.pop(5)
    print(f"  Удалено из MyList: '{deleted_custom}'")
    print(f"  Удалено из Python list: '{deleted_python}'")
    print(f"  MyList: {my_custom_list}")
    print(f"  Python list: {python_list}")