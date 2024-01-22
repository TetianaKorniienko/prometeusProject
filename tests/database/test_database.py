import pytest

from datetime import datetime
from modules.common.database import Database


@pytest.mark.database
def test_database_connection():
    db = Database()
    db.test_connection()


@pytest.mark.database
def test_check_all_users():
    db = Database()
    users = db.get_all_users()
    print(users)


@pytest.mark.database
def test_check_user_sergii():
    db = Database()
    user = db.get_user_address_by_name("Sergii")

    assert user[0][0] == "Maydan Nezalezhnosti 1"
    assert user[0][1] == "Kyiv"
    assert user[0][2] == "3127"
    assert user[0][3] == "Ukraine"


@pytest.mark.database
def test_product_qnt_update():
    db = Database()
    db.update_product_qnt_by_id(1, 25)
    water_qnt = db.select_product_qnt_by_id(1)

    assert water_qnt[0][0] == 25


@pytest.mark.database
def test_product_insert():
    db = Database()
    db.insert_product(4, "печиво", "солодке", 30)
    cookie_qnt = db.select_product_qnt_by_id(4)

    assert cookie_qnt[0][0] == 30


@pytest.mark.database
def test_product_delete():
    db = Database()
    db.insert_product(99, "тестові", "дані", 999)
    db.delete_product_by_id(99)
    qnt = db.select_product_qnt_by_id(99)

    assert len(qnt) == 0


@pytest.mark.database
def test_detailed_orders():
    db = Database()
    orders = db.get_detailed_orders()
    print("Замовлення", orders)
    # Check quantity of orders equal to 1
    assert len(orders) == 1

    # Check structure of data
    assert orders[0][0] == 1
    assert orders[0][1] == "Sergii"
    assert orders[0][2] == "солодка вода"
    assert orders[0][3] == "з цукром"


@pytest.mark.database
def test_insert_customer_with_valid_data_types():
    db = Database()
    db.insert_customer("Tetyana", "Avenue Peremogu 5", "Chernihiv", "12121", "Ukraine")
    user = db.select_user_by_name("Tetyana")

    assert user[1] == "Tetyana"
    assert user[2] == "Avenue Peremogu 5"
    assert user[3] == "Chernihiv"
    assert user[4] == "12121"
    assert user[5] == "Ukraine"


@pytest.mark.database
def test_select_nonexists_user_by_name():
    db = Database()
    user = db.select_user_by_name("NonExistentUser")

    assert user is None


@pytest.mark.database
def test_delete_user_by_name():
    db = Database()
    db.delete_user_by_name("Tetyana")
    users = db.get_all_users()

    assert "Tetyana" not in [user[0] for user in users]


@pytest.mark.database
def test_invalid_data_type_insert_customer():
    db = Database()
    user = db.insert_user_with_invalid_name(0)
    users = db.get_all_users()

    assert user not in [user[0] for user in users]


@pytest.mark.database
def test_create_order():
    db = Database()
    date = datetime.now()
    order_date = date.strftime("%H:%M:%S")
    db.create_order(2, 1)
    orders = db.get_all_orders()
    order = db.get_last_inserted_order()

    assert order in orders
    assert order[1] == 2
    assert order[2] == 1
    assert order[3] == order_date


@pytest.mark.database
def test_create_order_with_invalid_ids():
    db = Database()
    db.insert_order_with_invalid_data("invalid_customer_id", "invalid_product_id")
    orders = db.get_all_orders()

    assert len(orders) == 2


@pytest.mark.database
def test_delete_order_by_id():
    db = Database()
    db.delete_order_by_id(2)
    orders = db.get_all_orders()

    assert 2 not in [order[0] for order in orders]
