from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class Item(models.Model):
    CATEGORY_CHOICES = [
        ('Photo Editing', 'Photo Editing Pack'),
        ('Lightroom Presets', 'Lightroom Presets Pack'),
        ('Wedding Album', 'Wedding Album Designing Pack'),
        ('Wedding Invitation', 'Wedding Invitation Pack'),
        ('Photoshop Background', 'Photoshop Background PSD Pack'),
        ('Royal Fonts', 'Royal Fonts Pack'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Photo Editing')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    main_image = models.ImageField(upload_to='items/')
    created_at = models.DateTimeField(auto_now_add=True)
    google_drive_link = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.category} - {self.title}"

    def formatted_created_at(self):
        return self.created_at.strftime('%Y-%m-%d %I:%M:%S %p')

    class Meta:
        ordering = ['-created_at']


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='item_images/')

    def __str__(self):
        return f"Image for {self.item.title}"


class ItemVideo(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='videos')
    video = models.FileField(upload_to='item_videos/')

    def __str__(self):
        return f"Video for {self.item.title}"


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    @classmethod
    def get_category_choices(cls):
        return Item.CATEGORY_CHOICES


class CategoryVideo(models.Model):
    category = models.CharField(
        max_length=50,
        choices=Category.get_category_choices(), default='Photo Editing'
    )
    video = models.FileField(upload_to='category_videos/')
    title = models.CharField(max_length=255)
    tips = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Video for {self.category} category"


class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    payment_id = models.CharField(max_length=100, unique=True)
    payment_status = models.CharField(max_length=50)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    email_sent = models.BooleanField(default=False)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # Additional fields
    email = models.EmailField(max_length=255, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username if self.user else 'Guest'}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title} in Order {self.order.id}"


