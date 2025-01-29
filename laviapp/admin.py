from django.contrib import admin
from .models import Category, Item, ItemImage, ItemVideo, CategoryVideo, Order, OrderItem

# Admin class for the Category model
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)

# Admin class for the CategoryVideo model
class CategoryVideoAdmin(admin.ModelAdmin):
    list_display = ['category', 'title', 'video']
    search_fields = ['category', 'title']
    list_filter = ['category']

admin.site.register(CategoryVideo, CategoryVideoAdmin)

# Admin class for the OrderItem model inline
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ('item', 'quantity', 'price')
    readonly_fields = ('price',)

# Admin class for the Order model
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_items_names', 'full_name', 'payment_id', 'payment_status', 'total_price', 'status', 'created_at')
    inlines = [OrderItemInline]
    list_filter = ('payment_status', 'status', 'created_at')
    search_fields = ('full_name', 'user__username', 'payment_id')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        self.update_total_price(obj)

    def update_total_price(self, order):
        total_price = sum(item.price * item.quantity for item in order.items.all())
        order.total_price = total_price
        order.save()


    def order_items_names(self, obj):
        # Fetch all the item titles from the order's items
        return ", ".join([order_item.item.title for order_item in obj.items.all()])
    
    # Add a short description for the custom method
    order_items_names.short_description = 'Order Items'

# Admin class for the Item model
class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 1
    max_num = 10

class ItemVideoInline(admin.TabularInline):
    model = ItemVideo
    extra = 1
    max_num = 5

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'description')
    inlines = [ItemImageInline, ItemVideoInline]

admin.site.register(Order, OrderAdmin)
# admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemImage)
admin.site.register(ItemVideo)
