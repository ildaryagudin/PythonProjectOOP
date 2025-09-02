class Product:
    """
    Класс продукта с приватным атрибутом цены и соответствующими геттерами и сеттерами
    """
    def __init__(self, name, description, price, quantity):
        self.name = name                    # Название товара
        self.description = description      # Описание товара
        self.__price = price                # Приватный атрибут цены
        self.quantity = quantity            # Количество товара

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
        if isinstance(other, Product):
            # Расчёт стоимости текущего товара
            cost_self = self.price * self.quantity
            # Расчёт стоимости другого товара
            cost_other = other.price * other.quantity
            # Возврат общей стоимости
            return cost_self + cost_other
        else:
            raise TypeError("Нельзя складывать объект Product с объектами другого типа")


class Category:
    # Общий счетчик количества товаров среди всех категорий
    product_count = 0

    def __init__(self, name):
        self.name = name                     # Имя категории
        self._products = []                  # Список товаров в данной категории

    def add_product(self, product):
        """
        Метод для добавления нового товара в категорию с проверкой типа объекта.
        Проверяется, что добавляемый продукт является экземпляром класса Product или его наследника.
        Если условие выполнено, товар добавляется в список товаров категории.
        """
        if isinstance(product, Product):
            self._products.append(product)
            # Повышаем общий счётчик количества товаров
            Category.product_count += 1
        else:
            raise ValueError(f"{product} не является экземпляром класса Product.")

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