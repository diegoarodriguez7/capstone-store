from unittest import TestCase
from app import app
from models import *

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///shop_db_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

db.drop_all()
db.create_all()

new_product = Product(name='TestProduct', price=1000, stock=10, description='This is a test description',
                      image='')
db.session.add(new_product)
db.session.commit()


class ProductsTestCase(TestCase):
    """Tests for views about products."""

    def setUp(self):
        """Make demo data."""

        Product.query.delete()
        db.session.commit()

        new_product = Product(name='TestProduct', price=1000, stock=10, description='This is a test description',
                              image='https://images.unsplash.com/photo-1632258521940-b29d7d2ae9f5?ixid=MnwxMjA3fDB8MHxlZGl0b3JpYWwtZmVlZHwxMnx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1400&q=60')
        db.session.add(new_product)
        db.session.commit()

        self.product_id = new_product.id

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_all_products(self):
        with app.test_client() as client:
            resp = client.get("/admin")
            self.assertEqual(resp.status_code, 200)

            self.assertEqual(
                resp.json,
                {'product': [{
                    'id': self.product_id,
                    'name': 'TestProduct',
                    'price': 1000,
                    'stock': 10,
                    'description': 'This is a test description',
                    'image': 'https://images.unsplash.com/photo-1620165483000-a97cb8e9f7dd?ixid=MnwxMjA3fDF8MHxlZGl0b3JpYWwtZmVlZHwxNnx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1400&q=60'
                }]})

    def test_get_single_product(self):
        with app.test_client() as client:
            resp = client.get(f"/product/{self.product_id}")
            self.assertEqual(resp.status_code, 200)

            self.assertEqual(
                resp.json,
                {'product': [{
                    'id': self.product_id,
                    'name': 'TestProduct',
                    'price': 1000,
                    'stock': 10,
                    'description': 'This is a test description',
                    'image': ''
                }]})

    def test_create_product(self):
        with app.test_client() as client:
            resp = client.post(
                "/product", json={
                    'name': 'TestProduct2',
                    'price': 2000,
                    'stock': 20,
                    'description': 'This is a second test description',
                    'image': 'https://images.unsplash.com/photo-1632337950445-ba446cb0e26f?ixid=MnwxMjA3fDB8MHxlZGl0b3JpYWwtZmVlZHw0N3x8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1400&q=60'
                })
            self.assertEqual(resp.status_code, 201)

            # don't know what ID it will be, so test then remove
            self.assertIsInstance(resp.json['product']['id'], int)
            del resp.json['product']['id']

            self.assertEqual(
                resp.json,
                {"product": {'name': 'TestProduct2',
                             'price': 2000,
                             'stock': 20,
                             'description': 'This is a second test description',
                             'image': 'https://upload.wikimedia.org/wikipedia/en/thumb/6/65/Happy_fun_ball.jpg/300px-Happy_fun_ball.jpg'}})

            self.assertEqual(Product.query.count(), 2)