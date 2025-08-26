import pytest

from src.main import Product, Category  # Импортируйте ваши классы отсюда

@pytest.fixture(autouse=True)
def reset_counts():
    """Сбрасываем счётчики перед каждым тестом"""
    Category.category_count = 0
    Category.product_count = 0

# Тестирование инициализации объекта Product
def test_product_initialization(reset_counts):
    prod = Product("Телефон Samsung", "Оригинальный смартфон Samsung", 10000, 5)
    assert prod.name == "Телефон Samsung"
    assert prod.description == "Оригинальный смартфон Samsung"
    assert prod.price == 10000
    assert prod.quantity == 5

# Тестирование инициализации объекта Category
def test_category_initialization(reset_counts):
    p1 = Product("Телефон Samsung", "Оригинальный смартфон Samsung", 10000, 5)
    p2 = Product("Ноутбук Lenovo", "Компактный ноутбук Lenovo", 30000, 3)
    cat = Category("Электроника", "Техника для дома и офиса", [p1, p2])
    assert cat.name == "Электроника"
    assert cat.description == "Техника для дома и офиса"
    assert len(cat.products) == 2

# Тестирование правильного подсчета количества товаров
def test_product_count(reset_counts):
    p1 = Product("Телефон Samsung", "Оригинальный смартфон Samsung", 10000, 5)
    p2 = Product("Ноутбук Lenovo", "Компактный ноутбук Lenovo", 30000, 3)
    cat = Category("Электроника", "Техника для дома и офиса", [p1, p2])
    total_products = sum(prod.quantity for prod in cat.products)  # Ручной подсчёт товаров
    assert total_products == 8  # 5 телефонов + 3 ноутбука = 8 штук

# Тестирование правильного подсчета количества категорий
def test_category_count(reset_counts):
    p1 = Product("Телефон Samsung", "Оригинальный смартфон Samsung", 10000, 5)
    p2 = Product("Ноутбук Lenovo", "Компактный ноутбук Lenovo", 30000, 3)
    cat1 = Category("Электроника", "Техника для дома и офиса", [p1, p2])
    cat2 = Category("Автомобили", "Транспортные средства", [])  # Вторая категория без товаров
    assert Category.category_count == 2  # Всего создано 2 категории