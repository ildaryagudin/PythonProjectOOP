import pytest
from io import StringIO
import sys
from unittest.mock import patch
from src.category_product import Product, Category, BaseProduct, Smartphone, LawnGrass, MixinLogCreation

class TestMixinLogCreation:
    """Тесты для миксина логирования создания объектов"""

    def test_mixin_log_creation_output(self):
        """Тестирование вывода информации при создании объекта"""
        captured_output = StringIO()
        sys.stdout = captured_output

        class TestClass(MixinLogCreation):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

        test_obj = TestClass(1, 2, name="test", value=42)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        assert "Создается объект класса 'TestClass' с аргументами:" in output
        assert "Позиционные аргументы: (1, 2)" in output
        assert "Ключевые аргументы: {'name': 'test', 'value': 42}" in output


class TestProduct:
    """Тесты для класса Product"""

    def test_product_initialization(self):
        """Тестирование инициализации продукта"""
        product = Product("Test Product", "Test Description", 100.0, 10)

        assert product.name == "Test Product"
        assert product.description == "Test Description"
        assert product.quantity == 10

    def test_price_property(self):
        """Тестирование свойства цены"""
        product = Product("Test", "Desc", 50.0, 5)

        assert product.price == 50.0

    def test_price_setter_valid(self):
        """Тестирование установки корректной цены"""
        product = Product("Test", "Desc", 50.0, 5)
        product.price = 75.0

        assert product.price == 75.0

    def test_price_setter_invalid(self, capsys):
        """Тестирование установки некорректной цены"""
        product = Product("Test", "Desc", 50.0, 5)
        product.price = -10

        captured = capsys.readouterr()
        assert product.price == 50.0  # Цена не должна измениться
        assert "Цена не должна быть нулевой или отрицательной" in captured.out

    def test_str_representation(self):
        """Тестирование строкового представления"""
        product = Product("Test Product", "Description", 99.99, 5)
        result = str(product)

        assert "Test Product" in result
        assert "99.99 руб." in result
        assert "5 шт." in result

    def test_add_products_same_type(self):
        """Тестирование сложения товаров одного типа"""
        product1 = Product("Product1", "Desc1", 10.0, 2)
        product2 = Product("Product2", "Desc2", 20.0, 3)

        result = product1 + product2
        expected = (10.0 * 2) + (20.0 * 3)

        assert result == expected

    def test_add_products_different_types(self):
        """Тестирование сложения товаров разных типов"""
        product = Product("Product", "Desc", 10.0, 2)

        with pytest.raises(TypeError, match="Нельзя складывать объект Product с объектами другого типа"):
            product + "not a product"


class TestCategory:
    """Тесты для класса Category"""

    def setup_method(self):
        """Сброс счетчика перед каждым тестом"""
        Category.product_count = 0

    def test_category_initialization(self):
        """Тестирование инициализации категории"""
        category = Category("Test Category")

        assert category.name == "Test Category"
        assert category._products == []

    def test_add_valid_product(self):
        """Тестирование добавления корректного продукта"""
        category = Category("Test Category")
        product = Product("Test Product", "Desc", 10.0, 5)

        category.add_product(product)

        assert len(category._products) == 1
        assert category._products[0] == product
        assert Category.product_count == 1

    def test_add_invalid_product(self):
        """Тестирование добавления некорректного продукта"""
        category = Category("Test Category")

        with pytest.raises(ValueError, match="не является экземпляром класса Product"):
            category.add_product("not a product")

    def test_products_list_empty(self):
        """Тестирование свойства products_list для пустой категории"""
        category = Category("Test Category")

        assert category.products_list == 'Список товаров пуст.'

    def test_products_list_with_products(self):
        """Тестирование свойства products_list с товарами"""
        category = Category("Test Category")
        product1 = Product("Product1", "Desc1", 10.0, 2)
        product2 = Product("Product2", "Desc2", 20.0, 3)

        category.add_product(product1)
        category.add_product(product2)

        products_list = category.products_list
        assert "Product1" in products_list
        assert "Product2" in products_list
        assert "10.00 руб." in products_list

    def test_str_representation_empty(self):
        """Тестирование строкового представления пустой категории"""
        category = Category("Test Category")

        assert str(category) == "Test Category, количество продуктов: 0 шт."

    def test_str_representation_with_products(self):
        """Тестирование строкового представления категории с товарами"""
        category = Category("Test Category")
        product1 = Product("Product1", "Desc1", 10.0, 2)
        product2 = Product("Product2", "Desc2", 20.0, 3)

        category.add_product(product1)
        category.add_product(product2)

        assert str(category) == "Test Category, количество продуктов: 5 шт."


class TestSmartphone:
    """Тесты для класса Smartphone"""

    def test_smartphone_initialization(self):
        """Тестирование инициализации смартфона"""
        smartphone = Smartphone(
            "iPhone", "Smartphone", 1000.0, 10,
            "Apple", 6.1
        )

        assert smartphone.name == "iPhone"
        assert smartphone.description == "Smartphone"
        assert smartphone.price == 1000.0
        assert smartphone.quantity == 10
        assert smartphone.brand == "Apple"
        assert smartphone.screen_size == 6.1

    def test_smartphone_str_representation(self):
        """Тестирование строкового представления смартфона"""
        smartphone = Smartphone(
            "Galaxy", "Android phone", 800.0, 5,
            "Samsung", 6.7
        )

        result = str(smartphone)
        assert "Смартфон 'Galaxy'" in result
        assert "Samsung" in result
        assert "6.7 дюймов" in result


class TestLawnGrass:
    """Тесты для класса LawnGrass"""

    def test_lawn_grass_initialization(self):
        """Тестирование инициализации газонной травы"""
        grass = LawnGrass(
            "Premium Grass", "Green grass", 50.0, 100,
            "Germany", 14, "dark green"
        )

        assert grass.name == "Premium Grass"
        assert grass.description == "Green grass"
        assert grass.price == 50.0
        assert grass.quantity == 100
        assert grass.country == "Germany"
        assert grass.germination_period == 14
        assert grass.color == "dark green"

    def test_lawn_grass_str_representation(self):
        """Тестирование строкового представления газонной травы"""
        grass = LawnGrass(
            "Soft Lawn", "Soft grass", 40.0, 80,
            "USA", 10, "light green"
        )

        result = str(grass)
        assert "Трава газонная 'Soft Lawn'" in result
        assert "USA" in result
        assert "10 дней" in result
        assert "light green" in result


class TestInheritance:
    """Тесты наследования и полиморфизма"""

    def test_product_inheritance(self):
        """Тестирование наследования Product от BaseProduct"""
        product = Product("Test", "Desc", 10.0, 5)

        assert isinstance(product, BaseProduct)
        assert hasattr(product, 'name')
        assert hasattr(product, 'description')
        assert hasattr(product, 'price')
        assert hasattr(product, 'quantity')

    def test_smartphone_inheritance(self):
        """Тестирование наследования Smartphone от BaseProduct"""
        smartphone = Smartphone("Test", "Desc", 10.0, 5, "Brand", 6.0)

        assert isinstance(smartphone, BaseProduct)

    def test_lawn_grass_inheritance(self):
        """Тестирование наследования LawnGrass от BaseProduct"""
        grass = LawnGrass("Test", "Desc", 10.0, 5, "Country", 10, "green")

        assert isinstance(grass, BaseProduct)


def test_product_count_global_counter():
    """Тестирование глобального счетчика товаров"""
    Category.product_count = 0  # Сброс счетчика

    category1 = Category("Category 1")
    category2 = Category("Category 2")

    product1 = Product("Product1", "Desc1", 10.0, 2)
    product2 = Product("Product2", "Desc2", 20.0, 3)
    product3 = Product("Product3", "Desc3", 30.0, 4)

    category1.add_product(product1)
    category1.add_product(product2)
    category2.add_product(product3)

    assert Category.product_count == 3