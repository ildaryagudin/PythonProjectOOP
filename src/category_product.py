class Product:
    """
        Класс продукта с приватным атрибутом цены и соответствующими геттерами и сеттерами
    """
    def __init__(self, name, description, price, quantity):
        self.name = name                   # Название товара
        self.description = description     # Описание товара
        self.__price = price               # Приватный атрибут цены
        self.quantity = quantity           # Количество товара

    # Геттер для цены
    @property
    def price(self):
        return self.__price

    # Сеттер для цены
    @price.setter
    def price(self, value):
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = value


class Category:
    # Общий счетчик количества товаров среди всех категорий
    product_count = 0

    def __init__(self, name):
        self.name = name  # Имя категории
        self._products = []  # Список товаров в данной категории

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

    @property
    def products_list(self):
        """Возвращает строку с перечнем товаров в удобном формате."""
        if not self._products:
            return 'Список товаров пуст.'

        formatted_products = []
        for product in self._products:
            formatted_products.append(
                f'{product.name}, {product.price:.2f} руб. Остаток: {product.quantity} шт.'
            )
        return '\\n'.join(formatted_products)




