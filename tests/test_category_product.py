import pytest
from src.category_product import Product  # импортируйте правильный модуль, где находятся ваши классы

@pytest.fixture
def sample_product():
    return Product("Телефон", "Описание телефона", 10000, 10)

def test_get_price(sample_product):
    # Проверяем получение цены
    assert sample_product.price == 10000

def test_set_valid_price(sample_product):
    # Меняем цену на валидное значение
    sample_product.price = 15000
    assert sample_product.price == 15000

def test_set_invalid_price_negative(sample_product, capsys):
    # Пробуем задать отрицательное значение цены
    sample_product.price = -5000
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert sample_product.price == 10000  # цена осталась неизменной

def test_set_invalid_price_zero(sample_product, capsys):
    # Пробуем задать нулевое значение цены
    sample_product.price = 0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert sample_product.price == 10000  # цена осталась неизменной


from src.category_product import Category  # замените на ваше реальное расположение модуля

@pytest.fixture
def empty_category():
    return Category("Категории", "Описание категории")

@pytest.fixture
def populated_category(empty_category):
    empty_category.add_product(Product("Телефон", "Описание телефона", 10000, 10))
    empty_category.add_product(Product("Планшет", "Описание планшета", 20000, 5))
    return empty_category

def test_empty_products_list(empty_category):
    # Проверяем отсутствие товаров
    assert empty_category.products_list == "Список товаров пуст."

def test_populated_products_list(populated_category):
    expected_output = (
        "Телефон, 10000.00 руб. Остаток: 10 шт.\\n"
        "Планшет, 20000.00 руб. Остаток: 5 шт."
    )
    assert populated_category.products_list == expected_output

def test_add_product(empty_category):
    # Проверяем добавление товара
    empty_category.add_product(Product("Телефон", "Описание телефона", 10000, 10))
    assert len(empty_category._products) == 1



@pytest.fixture
def create_product():
    return Product(name="Test Product", description="Description", price=100, quantity=10)

def test_add_two_products(create_product):
    # Создаём два товара
    p1 = create_product()
    p2 = Product(name="Another Test Product", description="Another Description", price=200, quantity=2)

    # Проверяем результат сложения
    expected_total_cost = p1.price * p1.quantity + p2.price * p2.quantity
    assert p1 + p2 == expected_total_cost, "Ошибка при сложении товаров"


def test_invalid_type_in_addition(create_product):
    p1 = create_product()
    invalid_object = "Not a Product instance"

    with pytest.raises(TypeError):
        _ = p1 + invalid_object