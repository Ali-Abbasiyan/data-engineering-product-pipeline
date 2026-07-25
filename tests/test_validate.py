from src.validate import validate_product


def test_valid_product_has_no_errors():
    product = {
        "id": 1,
        "title": "Laptop",
        "price": 999.99,
        "category": "laptops",
    }

    errors = validate_product(product)

    assert errors == []


def test_invalid_product_returns_errors():
    product = {
        "id": -1,
        "title": "",
        "price": -50,
        "category": "",
    }

    errors = validate_product(product)

    assert "id must be a positive integer" in errors
    assert "title must be a non-empty string" in errors
    assert "price must be a non-negative number" in errors
    assert "category must be a non-empty string" in errors