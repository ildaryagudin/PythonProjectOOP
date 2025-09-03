class Product:
    """
    Класс продукта с приватным атрибутом цены и соответствующими геттерами и сеттерами
    """
    def __init__(self, name, description, price, quantity):
        self.name = name                    # Название товара
        self.description = description      # Описание товара
        self.__price = price                # Приватный атрибут цены
        self.quantity = quantity            # Количество товара
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

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
        return f"{self.name}, {self.price:.2f} руб., остаток: {self.quantity} шт."

    # Специальный метод для сложения товаров
    def __add__(self, other):
        if isinstance(other, Product):
            # Расчёт стоимости текущего товара
            cost_self = self.price * self.quantity
            # Расчёт стоимости другого товара
            cost_other = other.price * other.quantity
            # Возврат общей стоимости
            return cost_self + cost_other
        else:
            raise TypeError("Нельзя складывать объект Product с объектами другого типа")
        # Проверяем, что другие объект принадлежит тому же самому типу
        if type(self) != type(other):
            raise TypeError("Объекты принадлежат разным классам и не могут быть сложены вместе.")

        # Вычисляем суммарную стоимость текущих товаров
        cost_self = self.price * self.quantity
        cost_other = other.price * other.quantity
        return cost_self + cost_other


class Category:
    # Общий счетчик количества товаров среди всех категорий
    product_count = 0

    def __init__(self, name):
        self.name = name                     # Имя категории
        self._products = []                  # Список товаров в данной категории
        self.name = name
        self._products = []

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
            raise ValueError(f"{product} не является экземпляром класса Product.")
            raise ValueError(f"{product} не является экземпляром класса Product или его наследником.")

    # Свойство для вывода списка товаров
    @property
    def products_list(self):
        if not self._products:
            return 'Список товаров пуст.'
        return '\\n'.join(str(product) for product in self._products)

    # Строковое представление категории
    def __str__(self):
        total_quantity = sum(product.quantity for product in self._products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."
        return f"{self.name}, количество продуктов: {total_quantity} шт."


# Классы-наследники
class Smartphone(Product):
    def __init__(self, name, description, price, quantity, efficiency, model, memory, color):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __str__(self):
        return f"{super().__str__()} ({self.model}, память: {self.memory} ГБ)"


class LawnGrass(Product):
    def __init__(self, name, description, price, quantity, country, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __str__(self):
        return f"{super().__str__()} (Страна производства: {self.country})"