from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from laviapp.models import Item, ItemImage, Order, OrderItem
from unittest import mock
import json


class ItemListViewTest(TestCase):

    def setUp(self):
        """Set up test data for Item"""
        self.item1 = Item.objects.create(
            title="Test Item 1",
            category="Photo Editing",
            description="Test description 1",
            price=19.99,
            main_image="path/to/image1.jpg"
        )
        self.item2 = Item.objects.create(
            title="Test Item 2",
            category="Lightroom Presets",
            description="Test description 2",
            price=29.99,
            main_image="path/to/image2.jpg"
        )

    def test_item_list_view(self):
        """Test the Item List view"""
        response = self.client.get(reverse('item_list'))  # Assuming URL name is 'item_list'
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'laviapp/item_list.html')
        self.assertContains(response, self.item1.title)
        self.assertContains(response, self.item2.title)


class OrderCreateViewTest(TestCase):

    def setUp(self):
        """Set up test user and item"""
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.item = Item.objects.create(
            title="Test Item",
            category="Photo Editing",
            description="Test description",
            price=19.99,
            main_image="path/to/image.jpg"
        )
        self.client.login(username='testuser', password='testpassword')

    def test_order_create_view_get(self):
        """Test GET request for the order creation view"""
        response = self.client.get(reverse('order_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'laviapp/order_create.html')

    def test_order_create_view_post_valid(self):
        """Test POST request for order creation with valid data"""
        form_data = {
            'item': self.item.id,
            'quantity': 2
        }
        response = self.client.post(reverse('order_create'), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('order_detail', kwargs={'order_id': 1}))


class ItemDetailViewTest(TestCase):

    def setUp(self):
        """Set up test data for Item and related items"""
        self.item = Item.objects.create(
            title="Test Item",
            category="Photo Editing",
            description="Test description",
            price=19.99,
            main_image="path/to/image.jpg"
        )
        self.item_image = ItemImage.objects.create(
            item=self.item,
            image="path/to/extra_image.jpg"
        )

    def test_item_detail_view(self):
        """Test that the item detail page loads correctly"""
        response = self.client.get(reverse('item_detail', kwargs={'pk': self.item.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'laviapp/item_detail.html')
        self.assertContains(response, self.item.title)
        self.assertContains(response, self.item_image.image)


class ContactEmailTest(TestCase):

    @mock.patch('django.core.mail.send_mail')  # Mock the send_mail function to prevent actual email sending
    def test_send_contact_email_valid(self, mock_send_mail):
        """Test the contact email view"""
        data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'phone': '1234567890',
            'message': 'Test message for contact form.'
        }
        response = self.client.post(reverse('send_contact_email'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'success', 'message': 'Email sent successfully!'})
        mock_send_mail.assert_called_once()  # Verify that the email function was called


class RazorpaySuccessViewTest(TestCase):

    def setUp(self):
        """Set up test data for Order"""
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.item = Item.objects.create(
            title="Test Item",
            category="Photo Editing",
            description="Test description",
            price=19.99,
            main_image="path/to/image.jpg"
        )
        self.order = Order.objects.create(
            user=self.user,
            payment_id="razorpay_order_123",
            payment_status="pending",
            total_price=39.98,
            status="pending",
            email="test@example.com",
            full_name="Test User",
            mobile_number="1234567890"
        )

    @mock.patch('razorpay.Client.utility.verify_payment_signature')  # Mock the Razorpay signature verification
    def test_razorpay_success(self, mock_verify_payment_signature):
        """Test the Razorpay payment success handling"""
        data = {
            'razorpay_payment_id': 'payment_id_123',
            'razorpay_order_id': 'razorpay_order_123',
            'razorpay_signature': 'razorpay_signature_123',
            'email': 'test@example.com'
        }
        response = self.client.post(reverse('razorpay_success'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True, 'order_id': self.order.id})
        self.order.refresh_from_db()  # Refresh the order from the database
        self.assertEqual(self.order.status, 'completed')
        self.assertEqual(self.order.payment_status, 'success')
