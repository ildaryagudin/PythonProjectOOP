class Product:
    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value <= 0:
            print("Цена не должна быть нулевой или отрицательной")
        else:
            self.__price = value

    def __str__(self):
        return f"{self.name}, {self.price:.2f} руб., остаток: {self.quantity} шт."

    def __add__(self, other):
        # Проверяем, что другие объект принадлежит тому же самому типу
        if type(self) != type(other):
            raise TypeError("Объекты принадлежат разным классам и не могут быть сложены вместе.")

        # Вычисляем суммарную стоимость текущих товаров
        cost_self = self.price * self.quantity
        cost_other = other.price * other.quantity
        return cost_self + cost_other


class Category:
    product_count = 0

    def __init__(self, name):
        self.name = name
        self._products = []

    def add_product(self, product):
        # Проверяем, что добавляемый объект относится к классу Product или его потомкам
        if isinstance(product, Product):
            self._products.append(product)
            Category.product_count += 1
        else:
            raise ValueError(f"{product} не является экземпляром класса Product или его наследником.")

    @property
    def products_list(self):
        if not self._products:
            return 'Список товаров пуст.'
        return '\\n'.join(str(product) for product in self._products)

    def __str__(self):
        total_quantity = sum(product.quantity for product in self._products)
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