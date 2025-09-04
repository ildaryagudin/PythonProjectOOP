import pytest
from io import StringIO
import sys
from src.category_product import MixinLogCreation, Product, Smartphone, LawnGrass, Category


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


# Остальные классы остаются без изменений...

class TestMixinLogCreation:
    """Тесты для MixinLogCreation"""

    def test_repr_method(self):
        """Тест метода __repr__ миксина"""

        class TestClass(MixinLogCreation):
            def __init__(self):
                super().__init__()

        obj = TestClass()
        assert repr(obj) == "Создается объект класса 'TestClass'"

    def test_init_with_arguments(self, capsys):
        """Тест конструктора миксина с аргументами"""

        class TestClass(MixinLogCreation):
            def __init__(self, a, b, c=1, d=2):
                super().__init__(a, b, c=c, d=d)

        # Перехватываем вывод
        obj = TestClass(1, 2, c=3, d=4)
        captured = capsys.readouterr()

        assert "Создается объект класса 'TestClass' с аргументами:" in captured.out
        assert "Позиционные аргументы: (1, 2)" in captured.out
        assert "Ключевые аргументы: {'c': 3, 'd': 4}" in captured.out


class TestProduct:
    """Тесты для класса Product"""

    def test_product_creation(self, capsys):
        """Тест создания продукта"""
        product = Product("Test", "Description", 100.0, 10)
        captured = capsys.readouterr()

        assert product.name == "Test"
        assert product.description == "Description"
        assert product.price == 100.0
        assert product.quantity == 10
        assert "Создается объект класса 'Product'" in captured.out

    def test_price_property(self):
        """Тест свойства price"""
        product = Product("Test", "Description", 100.0, 10)
        assert product.price == 100.0

    def test_price_setter_valid(self):
        """Тест сеттера цены с валидным значением"""
        product = Product("Test", "Description", 100.0, 10)
        product.price = 150.0
        assert product.price == 150.0

    def test_price_setter_invalid(self, capsys):
        """Тест сеттера цены с невалидным значением"""
        product = Product("Test", "Description", 100.0, 10)
        product.price = -50.0
        captured = capsys.readouterr()

        assert product.price == 100.0  # Цена не должна измениться
        assert "Цена не должна быть нулевой или отрицательной" in captured.out

    def test_str_method(self):
        """Тест строкового представления"""
        product = Product("Test", "Description", 100.50, 5)
        assert str(product) == "Test, 100.50 руб. Остаток: 5 шт."

    def test_add_method_same_type(self):
        """Тест сложения продуктов одного типа"""
        product1 = Product("Product1", "Desc1", 100.0, 2)
        product2 = Product("Product2", "Desc2", 200.0, 3)

        result = product1 + product2
        expected = (100.0 * 2) + (200.0 * 3)
        assert result == expected

    def test_add_method_different_type(self):
        """Тест сложения продуктов разных типов"""
        product = Product("Product", "Desc", 100.0, 2)
        smartphone = Smartphone("Phone", "Smart", 500.0, 1, "Brand", 6.1)

        with pytest.raises(TypeError, match="Объекты принадлежат разным классам и не могут быть сложены вместе."):
            product + smartphone


class TestSmartphone:
    """Тесты для класса Smartphone"""

    def test_smartphone_creation(self):
        """Тест создания смартфона"""
        phone = Smartphone("iPhone", "Smartphone", 1000.0, 5, "Apple", 6.1)

        assert phone.name == "iPhone"
        assert phone.description == "Smartphone"
        assert phone.price == 1000.0
        assert phone.quantity == 5
        assert phone.brand == "Apple"
        assert phone.screen_size == 6.1

    def test_smartphone_str_method(self):
        """Тест строкового представления смартфона"""
        phone = Smartphone("iPhone", "Smartphone", 1000.0, 5, "Apple", 6.1)
        expected = "Смартфон 'iPhone' (Apple, экран 6.1 дюймов), 1000.00 руб. Остаток: 5 шт."
        assert str(phone) == expected

    def test_smartphone_addition(self):
        """Тест сложения смартфонов"""
        phone1 = Smartphone("Phone1", "Smart", 500.0, 2, "Brand1", 6.0)
        phone2 = Smartphone("Phone2", "Smart", 700.0, 3, "Brand2", 6.5)

        result = phone1 + phone2
        expected = (500.0 * 2) + (700.0 * 3)
        assert result == expected


class TestLawnGrass:
    """Тесты для класса LawnGrass"""

    def test_lawn_grass_creation(self):
        """Тест создания газонной травы"""
        grass = LawnGrass("Green", "Grass", 50.0, 20, "USA", 14, "green")

        assert grass.name == "Green"
        assert grass.description == "Grass"
        assert grass.price == 50.0
        assert grass.quantity == 20
        assert grass.country == "USA"
        assert grass.germination_period == 14
        assert grass.color == "green"

    def test_lawn_grass_str_method(self):
        """Тест строкового представления газонной травы"""
        grass = LawnGrass("Green", "Grass", 50.0, 20, "USA", 14, "green")
        expected = "Трава газонная 'Green' (USA, период всхожести 14 дней, цвет green), 50.00 руб. Остаток: 20 шт."
        assert str(grass) == expected

    def test_lawn_grass_addition(self):
        """Тест сложения газонных трав"""
        grass1 = LawnGrass("Grass1", "Grass", 30.0, 10, "USA", 14, "green")
        grass2 = LawnGrass("Grass2", "Grass", 40.0, 15, "Canada", 10, "dark green")

        result = grass1 + grass2
        expected = (30.0 * 10) + (40.0 * 15)
        assert result == expected


class TestCategory:
    """Тесты для класса Category"""

    def test_category_creation(self):
        """Тест создания категории"""
        category = Category("Electronics", "Electronic devices")

        assert category.name == "Electronics"
        assert category.description == "Electronic devices"
        assert category.products == []
        assert Category.category_count >= 1  # Может быть больше из-за других тестов

    def test_add_valid_product(self):
        """Тест добавления валидного продукта"""
        category = Category("Electronics", "Electronic devices")
        product = Product("Laptop", "Gaming laptop", 1000.0, 5)

        initial_count = Category.product_count
        category.add_product(product)

        assert len(category.products) == 1
        assert category.products[0] == product
        assert Category.product_count == initial_count + 1

    def test_add_invalid_product(self):
        """Тест добавления невалидного продукта"""
        category = Category("Electronics", "Electronic devices")

        with pytest.raises(ValueError, match="не является экземпляром класса Product или его наследником."):
            category.add_product("not a product")

    def test_str_method_empty_category(self):
        """Тест строкового представления пустой категории"""
        category = Category("Empty", "Empty category")
        assert str(category) == "Empty, количество продуктов: 0 шт."

    def test_str_method_with_products(self):
        """Тест строкового представления категории с продуктами"""
        category = Category("Electronics", "Electronic devices")
        product1 = Product("Laptop", "Gaming", 1000.0, 2)
        product2 = Product("Mouse", "Wireless", 50.0, 3)

        category.add_product(product1)
        category.add_product(product2)

        assert str(category) == "Electronics, количество продуктов: 5 шт."

    def test_products_property(self):
        """Тест свойства products"""
        category = Category("Test", "Test category")
        product = Product("Test", "Test", 100.0, 1)

        category.add_product(product)
        assert category.products == [product]


class TestIntegration:
    """Интеграционные тесты"""

    def test_multiple_inheritance_chain(self, capsys):
        """Тест цепочки множественного наследования"""
        phone = Smartphone("TestPhone", "Test", 500.0, 2, "TestBrand", 6.0)
        captured = capsys.readouterr()

        # Проверяем, что миксин сработал
        assert "Создается объект класса 'Smartphone'" in captured.out
        assert "Позиционные аргументы: ()" in captured.out

        # Проверяем, что наследование работает корректно
        assert isinstance(phone, Smartphone)
        assert isinstance(phone, Product)
        assert isinstance(phone, MixinLogCreation)

    def test_category_with_different_products(self):
        """Тест категории с разными типами продуктов"""
        category = Category("Mixed", "Mixed products")

        product = Product("Product", "Regular", 100.0, 2)
        smartphone = Smartphone("Phone", "Smart", 500.0, 1, "Brand", 6.1)
        grass = LawnGrass("Grass", "Green", 50.0, 5, "USA", 14, "green")

        category.add_product(product)
        category.add_product(smartphone)
        category.add_product(grass)

        assert len(category.products) == 3
        assert str(category) == "Mixed, количество продуктов: 8 шт."

    def test_class_counters(self):
        """Тест счетчиков классов"""
        # Сбрасываем счетчики для чистого теста
        Category.category_count = 0
        Category.product_count = 0

        category1 = Category("Cat1", "Desc1")
        category2 = Category("Cat2", "Desc2")

        product1 = Product("Prod1", "Desc", 100.0, 1)
        product2 = Product("Prod2", "Desc", 200.0, 2)

        category1.add_product(product1)
        category2.add_product(product2)

        assert Category.category_count == 2
        assert Category.product_count == 2