from src.category_product import Product, Smartphone, Category, LawnGrass, AbstractProduct
import pytest
from io import StringIO
import sys


class TestProduct:
    """Тесты для класса Product"""

    def test_product_creation_success(self):
        """Тест успешного создания продукта"""
        product = Product("Тест", "Описание", 100, 10)
        assert product.name == "Тест"
        assert product.description == "Описание"
        assert product.price == 100
        assert product.quantity == 10

    def test_product_creation_zero_quantity_raises_error(self):
        """Тест создания продукта с нулевым количеством вызывает исключение"""
        with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
            Product("Тест", "Описание", 100, 0)

    def test_product_str_representation(self):
        """Тест строкового представления продукта"""
        product = Product("Телефон", "Смартфон", 15000, 5)
        expected = "Телефон, 15000.00 руб. Остаток: 5 шт."
        assert str(product) == expected

    def test_product_price_setter_valid_value(self):
        """Тест установки корректной цены через сеттер"""
        product = Product("Тест", "Описание", 100, 10)
        product.price = 200
        assert product.price == 200

    def test_product_price_setter_invalid_value(self, capsys):
        """Тест установки некорректной цены через сеттер"""
        product = Product("Тест", "Описание", 100, 10)
        product.price = -50
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевой или отрицательной" in captured.out
        assert product.price == 100  # Цена не должна измениться

    def test_product_addition_same_type(self):
        """Тест сложения продуктов одного типа"""
        product1 = Product("Товар1", "Описание1", 100, 2)
        product2 = Product("Товар2", "Описание2", 200, 3)
        result = product1 + product2
        assert result == 100 * 2 + 200 * 3

    def test_product_addition_different_types_raises_error(self):
        """Тест сложения продуктов разных типов вызывает исключение"""
        product = Product("Товар", "Описание", 100, 2)
        smartphone = Smartphone("Смартфон", "Описание", 200, 1, "Brand", 6.1)

        with pytest.raises(TypeError, match="Объекты принадлежат разным классам и не могут быть сложены вместе"):
            product + smartphone


class TestCategory:
    """Тесты для класса Category"""

    def test_category_creation(self):
        """Тест создания категории"""
        initial_count = Category.category_count
        category = Category("Электроника", "Техника")

        assert category.name == "Электроника"
        assert category.description == "Техника"
        assert len(category.products) == 0
        assert Category.category_count == initial_count + 1

    def test_add_product_success(self):
        """Тест успешного добавления продукта в категорию"""
        category = Category("Электроника", "Техника")
        product = Product("Телефон", "Смартфон", 10000, 5)

        initial_count = Category.product_count
        category.add_product(product)

        assert len(category.products) == 1
        assert category.products[0] == product
        assert Category.product_count == initial_count + 1

    def test_add_non_product_raises_error(self):
        """Тест добавления не-продукта в категорию вызывает исключение"""
        category = Category("Электроника", "Техника")

        with pytest.raises(ValueError, match="не является экземпляром класса Product"):
            category.add_product("not a product")

    def test_category_str_representation(self):
        """Тест строкового представления категории"""
        category = Category("Электроника", "Техника")
        product1 = Product("Товар1", "Описание", 100, 2)
        product2 = Product("Товар2", "Описание", 200, 3)

        category.add_product(product1)
        category.add_product(product2)

        assert str(category) == "Электроника, количество продуктов: 5 шт."

    def test_average_price_with_products(self):
        """Тест расчета средней цены с товарами в категории"""
        category = Category("Электроника", "Техника")
        product1 = Product("Товар1", "Описание", 100, 2)
        product2 = Product("Товар2", "Описание", 300, 1)

        category.add_product(product1)
        category.add_product(product2)

        assert category.average_price() == 200.0  # (100 + 300) / 2

    def test_average_price_empty_category(self):
        """Тест расчета средней цены для пустой категории"""
        category = Category("Пустая", "Категория")
        assert category.average_price() == 0


class TestSmartphone:
    """Тесты для класса Smartphone"""

    def test_smartphone_creation(self):
        """Тест создания смартфона"""
        smartphone = Smartphone("iPhone", "Флагман", 80000, 3, "Apple", 6.1)

        assert smartphone.name == "iPhone"
        assert smartphone.description == "Флагман"
        assert smartphone.price == 80000
        assert smartphone.quantity == 3
        assert smartphone.brand == "Apple"
        assert smartphone.screen_size == 6.1

    def test_smartphone_str_representation(self):
        """Тест строкового представления смартфона"""
        smartphone = Smartphone("Galaxy", "Андроид", 50000, 2, "Samsung", 6.7)
        expected = "Смартфон 'Galaxy' (Samsung, экран 6.7 дюймов), 50000.00 руб. Остаток: 2 шт."
        assert str(smartphone) == expected

    def test_smartphone_zero_quantity_raises_error(self):
        """Тест создания смартфона с нулевым количеством вызывает исключение"""
        with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
            Smartphone("iPhone", "Флагман", 80000, 0, "Apple", 6.1)


class TestLawnGrass:
    """Тесты для класса LawnGrass"""

    def test_lawn_grass_creation(self):
        """Тест создания газонной травы"""
        grass = LawnGrass("Газонная", "Для дачи", 500, 10, "Россия", 14, "зеленый")

        assert grass.name == "Газонная"
        assert grass.description == "Для дачи"
        assert grass.price == 500
        assert grass.quantity == 10
        assert grass.country == "Россия"
        assert grass.germination_period == 14
        assert grass.color == "зеленый"

    def test_lawn_grass_str_representation(self):
        """Тест строкового представления газонной травы"""
        grass = LawnGrass("Премиум", "Элитная", 800, 5, "Германия", 10, "изумрудный")
        expected = "Трава газонная 'Премиум' (Германия, период всхожести 10 дней, цвет изумрудный), 800.00 руб. Остаток: 5 шт."
        assert str(grass) == expected

    def test_lawn_grass_zero_quantity_raises_error(self):
        """Тест создания газонной травы с нулевым количеством вызывает исключение"""
        with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
            LawnGrass("Газонная", "Для дачи", 500, 0, "Россия", 14, "зеленый")


class TestInheritance:
    """Тесты наследования и полиморфизма"""

    def test_product_inheritance(self):
        """Тест что Smartphone и LawnGrass наследуются от Product"""
        smartphone = Smartphone("Тест", "Тест", 100, 1, "Бренд", 6.0)
        grass = LawnGrass("Тест", "Тест", 100, 1, "Страна", 10, "цвет")

        assert isinstance(smartphone, Product)
        assert isinstance(grass, Product)
        assert isinstance(smartphone, AbstractProduct)
        assert isinstance(grass, AbstractProduct)

    def test_addition_same_subclasses(self):
        """Тест сложения объектов одинаковых подклассов"""
        smartphone1 = Smartphone("С1", "Описание", 100, 2, "Бренд", 6.0)
        smartphone2 = Smartphone("С2", "Описание", 200, 3, "Бренд", 6.0)

        result = smartphone1 + smartphone2
        assert result == 100 * 2 + 200 * 3


class TestEdgeCases:
    """Тесты граничных случаев"""

    def test_multiple_categories_count(self):
        """Тест счетчика категорий при создании нескольких категорий"""
        initial_count = Category.category_count
        category1 = Category("Кат1", "Описание")
        category2 = Category("Кат2", "Описание")
        category3 = Category("Кат3", "Описание")

        assert Category.category_count == initial_count + 3

    def test_multiple_products_count(self):
        """Тест счетчика товаров при добавлении нескольких товаров"""
        initial_count = Category.product_count
        category = Category("Кат", "Описание")
        product1 = Product("Т1", "Описание", 100, 1)
        product2 = Product("Т2", "Описание", 200, 2)
        product3 = Product("Т3", "Описание", 300, 3)

        category.add_product(product1)
        category.add_product(product2)
        category.add_product(product3)

        assert Category.product_count == initial_count + 3