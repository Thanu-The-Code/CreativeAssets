from django.test import TestCase
from django.contrib.auth.models import User
from laviapp.models import Item, Order, OrderItem
from decimal import Decimal
from datetime import datetime


class ItemModelTest(TestCase):
    def setUp(self):
        """Create a test item"""
        self.item = Item.objects.create(
            title="Test Item",
            category="Photo Editing",
            description="Test description",
            price=Decimal("19.99"),
            main_image="path/to/image.jpg"
        )

    def test_item_creation(self):
        """Test the creation of an item"""
        self.assertEqual(self.item.title, "Test Item")
        self.assertEqual(self.item.category, "Photo Editing")
        self.assertEqual(str(self.item), "Photo Editing - Test Item")
        self.assertEqual(self.item.price, Decimal("19.99"))
        
    def test_formatted_created_at(self):
        """Test formatted creation date"""
        self.assertEqual(self.item.formatted_created_at(), self.item.created_at.strftime('%Y-%m-%d %I:%M:%S %p'))


class OrderModelTest(TestCase):
    def setUp(self):
        """Create a test order and user"""
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.item = Item.objects.create(
            title="Test Item",
            category="Photo Editing",
            description="Test description",
            price=Decimal("19.99"),
            main_image="path/to/image.jpg"
        )
        self.order = Order.objects.create(
            user=self.user,
            payment_id="1234",
            payment_status="completed",
            total_price=Decimal("19.99"),
            status="completed",
            email="testuser@example.com",
            full_name="Test User",
            mobile_number="1234567890"
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            item=self.item,
            price=Decimal("19.99"),
            quantity=1
        )

    def test_order_creation(self):
        """Test the creation of an order"""
        self.assertEqual(self.order.user.username, "testuser")
        self.assertEqual(self.order.payment_status, "completed")
        self.assertEqual(self.order.total_price, Decimal("19.99"))

    def test_order_item_creation(self):
        """Test the creation of an order item"""
        self.assertEqual(self.order_item.item.title, "Test Item")
        self.assertEqual(self.order_item.quantity, 1)
        self.assertEqual(self.order_item.price, Decimal("19.99"))


class OrderItemModelTest(TestCase):
    def setUp(self):
        """Create an order item linked to an order"""
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.item = Item.objects.create(
            title="Test Item",
            category="Photo Editing",
            description="Test description",
            price=Decimal("19.99"),
            main_image="path/to/image.jpg"
        )
        self.order = Order.objects.create(
            user=self.user,
            payment_id="1234",
            payment_status="completed",
            total_price=Decimal("19.99"),
            status="completed",
            email="testuser@example.com",
            full_name="Test User",
            mobile_number="1234567890"
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            item=self.item,
            price=Decimal("19.99"),
            quantity=1
        )

    def test_order_item_str(self):
        """Test the string representation of an order item"""
        self.assertEqual(str(self.order_item), "1 of Test Item in Order 1")
