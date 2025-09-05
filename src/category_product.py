from abc import ABC, abstractmethod


class MixinLogCreation:
    """Mixin-класс для логирования создания объекта."""

    def __repr__(self):
        """Специальный метод для вывода информации о создании объекта"""
        return f"Создается объект класса '{type(self).__name__}'"

    def __init__(self, *args, **kwargs):
        """Конструктор миксина выводит информацию о классе и передаваемых аргументах"""
        print(f"Создается объект класса '{type(self).__name__}' с аргументами:")
        print(f"Позиционные аргументы: {args}")
        print(f"Ключевые аргументы: {kwargs}")

        # Безопасный вызов super()
        try:
            super().__init__(*args, **kwargs)
        except TypeError:
            # Если следующий класс не принимает аргументы (например, object)
            super().__init__()


class AbstractProduct(ABC):
    """Абстрактный базовый класс для продуктов"""

    @abstractmethod
    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __add__(self, other):
        pass


class Category:
    # Общий счетчик количества категорий
    category_count = 0
    # Общий счетчик количества товаров среди всех категорий
    product_count = 0

    def __init__(self, name, description):
        self.name = name  # Имя категории
        self.description = description  # Описание категории
        self._products = []  # Список товаров в данной категории
        Category.category_count += 1

    def add_product(self, product):
        """
        Метод для добавления нового товара в категорию с проверкой типа объекта.
        Проверяется, что добавляемый продукт является экземпляром класса Product или его наследника.
        Если условие выполнено, товар добавляется в список товаров категории.
        """
        # Проверяем, что добавляемый объект относится к классу Product или его потомкам
        if isinstance(product, Product):
            self._products.append(product)
            # Повышаем общий счётчик количества товаров
            Category.product_count += 1
        else:
            raise ValueError(f"{product} не является экземпляром класса Product или его наследником.")

    # Свойство для вывода списка товаров
    @property
    def products(self):
        return self._products

    # Строковое представление категории
    def __str__(self):
        total_quantity = sum(product.quantity for product in self._products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."


class Product(MixinLogCreation, AbstractProduct):
    """
    Класс продукта с приватным атрибутом цены и соответствующими геттерами и сеттерами
    """

    def __init__(self, name, description, price, quantity):
        super().__init__(name=name, description=description, price=price, quantity=quantity)
        self.name = name  # Название товара
        self.description = description  # Описание товара
        self.__price = price  # Приватный атрибут цены
        self.quantity = quantity  # Количество товара

    # Геттер для цены
    @property
    def price(self):
        return self.__price

    # Сеттер для цены
    @price.setter
    def price(self, value):
        if value <= 0:
            print("Цена не должна быть нулевой или отрицательной")
        else:
            self.__price = value

    # Строковое представление продукта
    def __str__(self):
        return f"{self.name}, {self.price:.2f} руб. Остаток: {self.quantity} шт."

    # Специальный метод для сложения товаров
    def __add__(self, other):
        # Проверяем, что другой объект принадлежит тому же самому типу
        if type(self) != type(other):
            raise TypeError("Объекты принадлежат разным классам и не могут быть сложены вместе.")

        # Вычисляем суммарную стоимость текущих товаров
        cost_self = self.price * self.quantity
        cost_other = other.price * other.quantity
        return cost_self + cost_other


class Smartphone(Product):
    """Класс Смартфона, расширяющий базовые характеристики продукта"""

    def __init__(self, name, description, price, quantity, brand, screen_size):
        """
        Конструктор смартфона включает общие данные продукта + специфичные для смартфонов характеристики

        :param brand: Бренд смартфона
        :param screen_size: Размер экрана смартфона
        """
        super().__init__(name, description, price, quantity)
        self.brand = brand
        self.screen_size = screen_size

    def __str__(self):
        return f"Смартфон '{self.name}' ({self.brand}, экран {self.screen_size} дюймов), {self.price:.2f} руб. Остаток: {self.quantity} шт."


class LawnGrass(Product):
    """Класс Газонной травы, расширяющий базовые характеристики продукта"""

    def __init__(self, name, description, price, quantity, country, germination_period, color):
        """
        Конструктор травы включает общие данные продукта + специфичные для травы характеристики

        :param country: Страна-производитель
        :param germination_period: Период всхожести семян
        :param color: Цвет травы
        """
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __str__(self):
        return f"Трава газонная '{self.name}' ({self.country}, период всхожести {self.germination_period} дней, цвет {self.color}), {self.price:.2f} руб. Остаток: {self.quantity} шт."