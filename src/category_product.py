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
    # Другие части класса оставляем без изменений

    @property
    def products_list(self):
        """Возвращает строку с перечнем товаров в удобном формате"""
        if not self._products:
            return 'Список товаров пуст.'

        formatted_products = []
        for product in self._products:
            formatted_products.append(
                f'{product.name}, {product.price:.2f} руб. Остаток: {product.quantity} шт.'
            )
        return '\\n'.join(formatted_products)

    def add_product(self, product):
        """ Метод для добавления нового товара в категорию """
        self._products.append(product)
        # Повышаем общий счётчик количества товаров
        Category.product_count += 1




