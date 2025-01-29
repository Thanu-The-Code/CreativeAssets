from django.test import TestCase
from laviapp.form import OrderForm, ItemForm
from laviapp.models import Item
from decimal import Decimal


class OrderFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Create a shared test item for all tests"""
        cls.item = Item.objects.create(
            title="Test Item",
            category="Photo Editing",
            description="Test description",
            price=Decimal("19.99"),
            main_image="path/to/image.jpg"
        )

    def test_order_form_valid(self):
        """Test a valid order form with all required fields"""
        form_data = {
            'item': self.item.id,
            'quantity': 2
        }
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_order_form_invalid(self):
        """Test an invalid order form (missing 'item' field)"""
        form_data = {'quantity': 2}
        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('item', form.errors)


class ItemFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Create a shared test item for all tests"""
        cls.item = Item.objects.create(
            title="Test Item",
            category="Photo Editing",
            description="Test description",
            price=Decimal("19.99"),
            main_image="path/to/image.jpg"
        )

    def test_item_form_valid(self):
        """Test a valid item form with all fields provided"""
        form_data = {
            'category': 'Photo Editing',
            'title': 'New Item',
            'description': 'New item description',
            'price': '29.99',
            'main_image': 'path/to/image.jpg',
        }
        form = ItemForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_item_form_invalid(self):
        """Test an invalid item form with missing 'title' field"""
        form_data = {'category': 'Photo Editing'}
        form = ItemForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
