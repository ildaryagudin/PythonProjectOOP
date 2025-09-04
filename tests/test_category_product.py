from src.category_product import Product, Smartphone, LawnGrass, Category
import pytest

class TestProduct:
    """Тесты для класса Product"""

    def test_product_creation(self):
        """Тест создания продукта"""
        product = Product("Телефон", "Смартфон", 10000.0, 5)
        assert product.name == "Телефон"
        assert product.description == "Смартфон"
        assert product.price == 10000.0
        assert product.quantity == 5

    def test_price_property(self):
        """Тест геттера и сеттера цены"""
        product = Product("Телефон", "Смартфон", 10000.0, 5)

        # Проверка геттера
        assert product.price == 10000.0

        # Проверка сеттера с корректным значением
        product.price = 15000.0
        assert product.price == 15000.0

        # Проверка сеттера с некорректным значением (цена не должна измениться)
        product.price = -1000.0
        assert product.price == 15000.0  # Цена осталась прежней

    def test_str_representation(self):
        """Тест строкового представления"""
        product = Product("Телефон", "Смартфон", 9999.99, 10)
        expected = "Телефон, 9999.99 руб. Остаток: 10 шт."
        assert str(product) == expected

    def test_add_same_products(self):
        """Тест сложения одинаковых продуктов"""
        product1 = Product("Телефон", "Смартфон", 10000.0, 2)
        product2 = Product("Телефон", "Смартфон", 10000.0, 3)

        result = product1 + product2
        expected = 10000.0 * 2 + 10000.0 * 3
        assert result == expected

    def test_add_different_products_same_class(self):
        """Тест сложения разных продуктов одного класса"""
        product1 = Product("Телефон", "Смартфон", 10000.0, 2)
        product2 = Product("Ноутбук", "Игровой", 50000.0, 1)

        result = product1 + product2
        expected = 10000.0 * 2 + 50000.0 * 1
        assert result == expected

    def test_add_different_classes(self):
        """Тест сложения продуктов разных классов (должна быть ошибка)"""
        product = Product("Телефон", "Смартфон", 10000.0, 2)
        smartphone = Smartphone("iPhone", "Смартфон", 80000.0, 1, "Высокая", "15 Pro", 256, "Black")

        with pytest.raises(TypeError, match="Объекты принадлежат разным классам и не могут быть сложены вместе"):
            product + smartphone

    def test_add_with_non_product(self):
        """Тест сложения продукта с не-продуктом (должна быть ошибка)"""
        product = Product("Телефон", "Смартфон", 10000.0, 2)

        with pytest.raises(TypeError, match="Объекты принадлежат разным классам и не могут быть сложены вместе"):
            product + 100


class TestCategory:
    """Тесты для класса Category"""

    def setup_method(self):
        """Сбрасываем счетчик перед каждым тестом"""
        Category.product_count = 0

    def test_category_creation(self):
        """Тест создания категории"""
        category = Category("Электроника")
        assert category.name == "Электроника"
        assert category.products_list == 'Список товаров пуст.'

    def test_add_product(self):
        """Тест добавления продукта в категорию"""
        category = Category("Электроника")
        product = Product("Телефон", "Смартфон", 10000.0, 5)

        category.add_product(product)
        assert len(category._products) == 1
        assert Category.product_count == 1

    def test_add_non_product(self):
        """Тест добавления не-продукта в категорию (должна быть ошибка)"""
        category = Category("Электроника")

        with pytest.raises(ValueError, match="не является экземпляром класса Product или его наследника"):
            category.add_product("not a product")

    def test_products_list_property(self):
        """Тест свойства products_list"""
        category = Category("Электроника")

        # Пустой список
        assert category.products_list == 'Список товаров пуст.'

        # С одним продуктом
        product1 = Product("Телефон", "Смартфон", 10000.0, 5)
        category.add_product(product1)
        assert "Телефон, 10000.00 руб. Остаток: 5 шт." in category.products_list

        # С несколькими продуктами
        product2 = Product("Ноутбук", "Игровой", 50000.0, 2)
        category.add_product(product2)
        products_str = category.products_list
        assert "Телефон, 10000.00 руб. Остаток: 5 шт." in products_str
        assert "Ноутбук, 50000.00 руб. Остаток: 2 шт." in products_str

    def test_str_representation(self):
        """Тест строкового представления категории"""
        category = Category("Электроника")

        # Пустая категория
        assert str(category) == "Электроника, количество продуктов: 0 шт."

        # Категория с товарами
        product1 = Product("Телефон", "Смартфон", 10000.0, 5)
        product2 = Product("Ноутбук", "Игровой", 50000.0, 2)
        category.add_product(product1)
        category.add_product(product2)

        assert str(category) == "Электроника, количество продуктов: 7 шт."

    def test_product_count_class_variable(self):
        """Тест счетчика продуктов (классовая переменная)"""
        category1 = Category("Электроника")
        category2 = Category("Одежда")

        product1 = Product("Телефон", "Смартфон", 10000.0, 5)
        product2 = Product("Ноутбук", "Игровой", 50000.0, 2)
        product3 = Product("Футболка", "Хлопок", 1000.0, 10)

        category1.add_product(product1)
        assert Category.product_count == 1

        category1.add_product(product2)
        assert Category.product_count == 2

        category2.add_product(product3)
        assert Category.product_count == 3


class TestSmartphone:
    """Тесты для класса Smartphone"""

    def test_smartphone_creation(self):
        """Тест создания смартфона"""
        smartphone = Smartphone(
            "iPhone", "Смартфон", 80000.0, 3,
            "Высокая", "15 Pro", 256, "Black"
        )

        assert smartphone.name == "iPhone"
        assert smartphone.description == "Смартфон"
        assert smartphone.price == 80000.0
        assert smartphone.quantity == 3
        assert smartphone.efficiency == "Высокая"
        assert smartphone.model == "15 Pro"
        assert smartphone.memory == 256
        assert smartphone.color == "Black"

    def test_smartphone_str_representation(self):
        """Тест строкового представления смартфона"""
        smartphone = Smartphone(
            "iPhone", "Смартфон", 80000.0, 3,
            "Высокая", "15 Pro", 256, "Black"
        )

        expected = "iPhone, 80000.00 руб. Остаток: 3 шт. (15 Pro, память: 256 ГБ)"
        assert str(smartphone) == expected

    def test_smartphone_addition(self):
        """Тест сложения смартфонов"""
        smartphone1 = Smartphone(
            "iPhone", "Смартфон", 80000.0, 2,
            "Высокая", "15 Pro", 256, "Black"
        )
        smartphone2 = Smartphone(
            "Samsung", "Смартфон", 60000.0, 3,
            "Высокая", "S23", 128, "White"
        )

        result = smartphone1 + smartphone2
        expected = 80000.0 * 2 + 60000.0 * 3
        assert result == expected


class TestLawnGrass:
    """Тесты для класса LawnGrass"""

    def test_lawn_grass_creation(self):
        """Тест создания газонной травы"""
        lawn_grass = LawnGrass(
            "Газонная трава", "Для дачи", 500.0, 100,
            "Россия", "14 дней", "Зеленая"
        )

        assert lawn_grass.name == "Газонная трава"
        assert lawn_grass.description == "Для дачи"
        assert lawn_grass.price == 500.0
        assert lawn_grass.quantity == 100
        assert lawn_grass.country == "Россия"
        assert lawn_grass.germination_period == "14 дней"
        assert lawn_grass.color == "Зеленая"

    def test_lawn_grass_str_representation(self):
        """Тест строкового представления газонной травы"""
        lawn_grass = LawnGrass(
            "Газонная трава", "Для дачи", 500.0, 100,
            "Россия", "14 дней", "Зеленая"
        )

        expected = "Газонная трава, 500.00 руб. Остаток: 100 шт. (Страна производства: Россия)"
        assert str(lawn_grass) == expected

    def test_lawn_grass_addition(self):
        """Тест сложения газонных трав"""
        lawn_grass1 = LawnGrass(
            "Газонная трава", "Для дачи", 500.0, 50,
            "Россия", "14 дней", "Зеленая"
        )
        lawn_grass2 = LawnGrass(
            "Элитная трава", "Для гольфа", 1000.0, 25,
            "Германия", "10 дней", "Темно-зеленая"
        )

        result = lawn_grass1 + lawn_grass2
        expected = 500.0 * 50 + 1000.0 * 25
        assert result == expected


class TestInheritance:
    """Тесты наследования и полиморфизма"""

    def setup_method(self):
        """Сбрасываем счетчик перед каждым тестом"""
        Category.product_count = 0

    def test_inheritance_hierarchy(self):
        """Тест иерархии наследования"""
        smartphone = Smartphone(
            "iPhone", "Смартфон", 80000.0, 3,
            "Высокая", "15 Pro", 256, "Black"
        )
        lawn_grass = LawnGrass(
            "Газонная трава", "Для дачи", 500.0, 100,
            "Россия", "14 дней", "Зеленая"
        )

        # Проверка наследования
        assert isinstance(smartphone, Product)
        assert isinstance(lawn_grass, Product)

        # Проверка типов
        assert type(smartphone) == Smartphone
        assert type(lawn_grass) == LawnGrass

    def test_cross_class_addition_error(self):
        """Тест ошибки при сложении объектов разных наследников"""
        smartphone = Smartphone(
            "iPhone", "Смартфон", 80000.0, 3,
            "Высокая", "15 Pro", 256, "Black"
        )
        lawn_grass = LawnGrass(
            "Газонная трава", "Для дачи", 500.0, 100,
            "Россия", "14 дней", "Зеленая"
        )

        with pytest.raises(TypeError, match="Объекты принадлежат разным классам и не могут быть сложены вместе"):
            smartphone + lawn_grass

    def test_polymorphism_in_category(self):
        """Тест полиморфизма при добавлении в категорию"""
        category = Category("Разные товары")

        product = Product("Книга", "Художественная", 500.0, 10)
        smartphone = Smartphone(
            "iPhone", "Смартфон", 80000.0, 3,
            "Высокая", "15 Pro", 256, "Black"
        )
        lawn_grass = LawnGrass(
            "Газонная трава", "Для дачи", 500.0, 100,
            "Россия", "14 дней", "Зеленая"
        )

        # Все три объекта должны добавляться без ошибок
        category.add_product(product)
        category.add_product(smartphone)
        category.add_product(lawn_grass)

        assert len(category._products) == 3
        assert Category.product_count == 3

    def test_product_addition_different_types_error_message(self):
        """Тест сообщения об ошибке при сложении разных типов"""
        product = Product("Телефон", "Смартфон", 10000.0, 2)
        smartphone = Smartphone("iPhone", "Смартфон", 80000.0, 1, "Высокая", "15 Pro", 256, "Black")

        with pytest.raises(TypeError) as exc_info:
            product + smartphone

        assert "Объекты принадлежат разным классам и не могут быть сложены вместе" in str(exc_info.value)

    def test_product_addition_different_types_error_message(self):
        """Тест сообщения об ошибке при сложении разных типов - покрытие строки 37"""
        product = Product("Телефон", "Смартфон", 10000.0, 2)
        smartphone = Smartphone("iPhone", "Смартфон", 80000.0, 1, "Высокая", "15 Pro", 256, "Black")

        with pytest.raises(TypeError) as exc_info:
            product + smartphone

        error_message = str(exc_info.value)
        assert "Объекты принадлежат разным классам и не могут быть сложены вместе" in error_message
        assert "разным классам" in error_message  # Дополнительная проверка

    def test_isinstance_check_in_add_method(self):
        """Тест проверки isinstance в методе __add__ - покрытие логики"""
        product = Product("Телефон", "Смартфон", 10000.0, 2)

        # Создаем объект, который не является Product
        class FakeProduct:
            def __init__(self):
                self.price = 100
                self.quantity = 1

        fake_product = FakeProduct()

        with pytest.raises(TypeError) as exc_info:
            product + fake_product

        error_message = str(exc_info.value)
        # Исправляем ожидаемое сообщение об ошибке
        assert "Объекты принадлежат разным классам и не могут быть сложены вместе" in error_message
    def test_product_addition_order(self):
        """Тест порядка сложения продуктов"""
        product1 = Product("Товар1", "Описание1", 100.0, 2)
        product2 = Product("Товар2", "Описание2", 200.0, 3)

        result1 = product1 + product2
        result2 = product2 + product1

        assert result1 == result2 == 100.0 * 2 + 200.0 * 3

    def test_product_with_zero_quantity_addition(self):
        """Тест сложения продуктов с нулевым количеством"""
        product1 = Product("Товар1", "Описание1", 100.0, 0)  # Нулевое количество
        product2 = Product("Товар2", "Описание2", 200.0, 5)

        result = product1 + product2
        assert result == 100.0 * 0 + 200.0 * 5  # Должно быть 1000.0

    def test_product_addition_commutative(self):
        """Тест коммутативности сложения продуктов"""
        product1 = Product("Товар1", "Описание1", 100.0, 2)
        product2 = Product("Товар2", "Описание2", 200.0, 3)

        # a + b должно равняться b + a
        assert (product1 + product2) == (product2 + product1)

    def test_category_str_empty(self):
        """Тест строкового представления пустой категории"""
        category = Category("Пустая категория")
        assert str(category) == "Пустая категория, количество продуктов: 0 шт."

    def test_category_str_single_product(self):
        """Тест строкового представления категории с одним продуктом"""
        category = Category("Категория")
        product = Product("Товар", "Описание", 100.0, 5)
        category.add_product(product)

        assert str(category) == "Категория, количество продуктов: 5 шт."

    def test_category_product_count_class_variable_reset(self):
        """Тест, что классовая переменная product_count работает корректно"""
        # Сбросим счетчик
        Category.product_count = 0

        category1 = Category("Категория 1")
        category2 = Category("Категория 2")

        product1 = Product("Товар 1", "Описание", 100.0, 1)
        product2 = Product("Товар 2", "Описание", 200.0, 2)
        product3 = Product("Товар 3", "Описание", 300.0, 3)

        category1.add_product(product1)
        assert Category.product_count == 1

        category1.add_product(product2)
        assert Category.product_count == 2

        category2.add_product(product3)
        assert Category.product_count == 3

        # Создадим новую категорию и проверим что счетчик продолжает работать
        category3 = Category("Категория 3")
        product4 = Product("Товар 4", "Описание", 400.0, 4)
        category3.add_product(product4)
        assert Category.product_count == 4


def test_price_setter_positive_value():
    """Тест сеттера цены с положительным значением"""
    product = Product("Тест", "Описание", 100.0, 5)
    product.price = 200.0
    assert product.price == 200.0


def test_price_getter():
    """Тест геттера цены"""
    product = Product("Тест", "Описание", 150.0, 3)
    assert product.price == 150.0


def test_product_initialization():
    """Тест инициализации продукта со всеми атрибутами"""
    product = Product("Телефон", "Смартфон", 10000.0, 5)
    assert product.name == "Телефон"
    assert product.description == "Смартфон"
    assert product.price == 10000.0
    assert product.quantity == 5


def test_category_initialization():
    """Тест инициализации категории"""
    category = Category("Электроника")
    assert category.name == "Электроника"
    assert category._products == []


def test_category_add_product_increases_count():
    """Тест что добавление продукта увеличивает счетчик"""
    initial_count = Category.product_count
    category = Category("Тест")
    product = Product("Тест", "Описание", 100.0, 1)

    category.add_product(product)
    assert Category.product_count == initial_count + 1


def test_category_products_list_empty():
    """Тест properties products_list для пустой категории"""
    category = Category("Пустая")
    assert category.products_list == 'Список товаров пуст.'


def test_category_products_list_with_products():
    """Тест properties products_list для категории с продуктами"""
    category = Category("Тест")
    product = Product("Тест", "Описание", 100.0, 5)
    category.add_product(product)

    assert "Тест, 100.00 руб. Остаток: 5 шт." in category.products_list


def test_category_str_representation():
    """Тест строкового представления категории"""
    category = Category("Тест")
    product = Product("Тест", "Описание", 100.0, 3)
    category.add_product(product)

    assert "Тест, количество продуктов: 3 шт." in str(category)


def test_smartphone_initialization():
    """Тест инициализации смартфона"""
    smartphone = Smartphone(
        "iPhone", "Смартфон", 80000.0, 3,
        "Высокая", "15 Pro", 256, "Black"
    )

    assert smartphone.name == "iPhone"
    assert smartphone.model == "15 Pro"
    assert smartphone.memory == 256


def test_lawn_grass_initialization():
    """Тест инициализации газонной травы"""
    lawn_grass = LawnGrass(
        "Газон", "Для дачи", 500.0, 100,
        "Россия", "14 дней", "Зеленая"
    )

    assert lawn_grass.name == "Газон"
    assert lawn_grass.country == "Россия"
    assert lawn_grass.germination_period == "14 дней"


def test_smartphone_str_representation():
    """Тест строкового представления смартфона"""
    smartphone = Smartphone(
        "iPhone", "Смартфон", 80000.0, 3,
        "Высокая", "15 Pro", 256, "Black"
    )

    result = str(smartphone)
    assert "iPhone" in result
    assert "15 Pro" in result
    assert "256" in result


def test_lawn_grass_str_representation():
    """Тест строкового представления газонной травы"""
    lawn_grass = LawnGrass(
        "Газон", "Для дачи", 500.0, 100,
        "Россия", "14 дней", "Зеленая"
    )

    result = str(lawn_grass)
    assert "Газон" in result
    assert "Россия" in result