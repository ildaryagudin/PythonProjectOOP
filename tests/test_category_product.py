import pytest

from src.category_product import Product, Smartphone, LawnGrass, Category

# Тест №1: Проверка правильного создания товара и доступности полей
def test_create_product():
    product = Product(name='Тестовый товар', description='Описание товара', price=100, quantity=5)
    assert product.name == 'Тестовый товар'
    assert product.price == 100
    assert product.quantity == 5

# Тест №2: Проверка изменения цены товара
def test_change_price():
    product = Product(name='Телефон', description='Смартфон', price=50000, quantity=10)
    product.price = 60000
    assert product.price == 60000

# Тест №3: Проверка ошибки при изменении цены на отрицательное значение
def test_negative_price(capfd):
    product = Product(name='Книга', description='Научная литература', price=1500, quantity=20)
    product.price = -100
    captured = capfd.readouterr()
    assert captured.out.strip() == "Цена не должна быть нулевой или отрицательной"

# Тест №4: Проверка правильной работы сложения двух товаров одного типа
def test_add_products_of_same_type():
    smartphone1 = Smartphone(
        name="iPhone 14",
        description="Apple смартфон",
        price=99990,
        quantity=10,
        efficiency="Высокая производительность",
        model="Pro Max",
        memory=512,
        color="Черный"
    )
    smartphone2 = Smartphone(
        name="Samsung Galaxy S23",
        description="Samsung смартфон",
        price=89990,
        quantity=15,
        efficiency="Хорошая производительность",
        model="S23 Ultra",
        memory=256,
        color="Белый"
    )
    total_sum = smartphone1 + smartphone2
    expected_result = 99990 * 10 + 89990 * 15
    assert total_sum == expected_result

# Тест №5: Проверка исключения при сложении товаров разного типа
def test_add_different_types():
    smartphone = Smartphone(
        name="iPhone 14",
        description="Apple смартфон",
        price=99990,
        quantity=10,
        efficiency="Высокая производительность",
        model="Pro Max",
        memory=512,
        color="Черный"
    )
    grass = LawnGrass(
        name="Turf Grass",
        description="Газонная трава",
        price=1200,
        quantity=50,
        country="Германия",
        germination_period="7-10 дней",
        color="Зеленый"
    )
    with pytest.raises(TypeError):
        smartphone + grass

# Тест №6: Проверка добавления товаров в категорию
def test_add_to_category():
    category = Category("Смартфоны")
    phone = Smartphone(
        name="iPhone 14",
        description="Apple смартфон",
        price=99990,
        quantity=10,
        efficiency="Высокая производительность",
        model="Pro Max",
        memory=512,
        color="Черный"
    )
    category.add_product(phone)
    assert len(category._products) == 1
    assert category._products[0].name == "iPhone 14"

# Тест №7: Проверка невозможности добавления постороннего объекта в категорию
def test_add_invalid_object_to_category():
    category = Category("Смартфоны")
    invalid_obj = "Некорректный объект"
    with pytest.raises(ValueError):
        category.add_product(invalid_obj)