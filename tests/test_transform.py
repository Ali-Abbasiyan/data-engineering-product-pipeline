from src.transform import transform_product


def test_transform_product_calculates_final_price():
    product = {
        "id": 1,
        "title": "  Laptop  ",
        "category": "  LAPTOPS  ",
        "brand": "Test Brand",
        "price": 100,
        "discountPercentage": 20,
        "rating": 4.5,
        "stock": 10,
    }

    transformed_product = transform_product(product)

    assert transformed_product["product_id"] == 1
    assert transformed_product["title"] == "Laptop"
    assert transformed_product["category"] == "laptops"
    assert transformed_product["original_price"] == 100
    assert transformed_product["discount_percentage"] == 20
    assert transformed_product["final_price"] == 80.0
    assert transformed_product["rating"] == 4.5
    assert transformed_product["stock"] == 10