from django.shortcuts import render, redirect
from .models import Item, ItemImage 


from django.shortcuts import render, get_object_or_404
from .models import Item

from django.contrib.auth import authenticate, login
from .form import LoginForm

from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from razorpay import Client

# Create your views here.

def home(request):
    items = Item.objects.all()[:6]  # Fetch the first 6 items
    return render(request, 'laviapp/home.html', {'items': items})


def about(request):
    return render(request, 'laviapp/about.html')

def shop(request):
    return render(request, 'laviapp/shop.html')

def contact(request):
    return render(request, 'laviapp/contact.html')



from django.shortcuts import render
from .models import Item, CategoryVideo, Category

def more_items(request):
    # Fetch all items for the 'More Items' page
    items = Item.objects.all()
    categories = [choice[0] for choice in Item.CATEGORY_CHOICES]
    selected_category = None  # No category selected

    # Fetch tips from CategoryVideo for all categories
    category_tips = []

    # If a category is selected, fetch tips for that category
    if selected_category:
        # Fetch CategoryVideo entries for the selected category
        category_videos = CategoryVideo.objects.filter(category=selected_category)
        category_tips = [video.tips for video in category_videos]  # Get all tips for the selected category
    else:
        category_videos = CategoryVideo.objects.all()
        category_tips = [video.tips for video in category_videos]

    return render(request, 'laviapp/more_items.html', {
        'items': items,
        'categories': categories,
        'selected_category': selected_category,
        'category_tips': category_tips,  # Pass category-specific tips from the database
    })


def filtered_items(request, category):
    # Fetch items based on the selected category
    items = Item.objects.filter(category=category)
    categories = [choice[0] for choice in Item.CATEGORY_CHOICES]
    selected_category = category  # Set the selected category

    # Fetch tips from CategoryVideo for the selected category
    category_videos = CategoryVideo.objects.filter(category=category)
    category_tips = [video.tips for video in category_videos]  # Get all tips for the selected category

    return render(request, 'laviapp/more_items.html', {
        'items': items,
        'categories': categories,
        'selected_category': selected_category,
        'category_tips': category_tips,  # Pass category-specific tips from the database
    })




import json
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt  # Allows AJAX requests to bypass CSRF protection (use with caution)
def send_contact_email(request):
    if request.method == 'POST':
        try:
            # Parse the JSON request body
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            phone = data.get('phone', 'Not provided')
            message = data.get('message')

            # Compose the email with HTML formatting
            subject = f"Contact Form Submission from {name}"

            email_message = f"""
            <html>
            <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; color: #333;">
                <div style="background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);">
                    <h2 style="color: #f39c12; text-align: center;">New Contact Form Submission</h2>
                    <p><strong>Name:</strong> {name}</p>
                    <p><strong>Email:</strong> {email}</p>
                    <p><strong>Phone:</strong> {phone}</p>
                    <p><strong>Message:</strong></p>
                    <p style="background-color: #f9f9f9; padding: 15px; border-radius: 4px;">{message}</p>
                    <p style="font-size: 14px; color: #777;">This message was sent via the contact form on your website.</p>
                </div>
            </body>
            </html>
            """
            recipient_email = "thaneeshgvalvanshi25@gmail.com"  # Your recipient email

            # Send the email with HTML content
            send_mail(
                subject,
                '',  # We don't need plain text body as it's HTML formatted
                email,  # From email (use the user's email for reply-to)
                [recipient_email],  # Recipient list
                fail_silently=False,
                html_message=email_message  # Sending the HTML message
            )

            return JsonResponse({'status': 'success', 'message': 'Email sent successfully!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)




from django.shortcuts import render, get_object_or_404
from .models import Item, ItemImage, CategoryVideo

def item_detail(request, pk):
    # Fetch the item using the primary key (pk)
    item = get_object_or_404(Item, pk=pk)

    # Fetch associated images and videos for the item
    more_images = ItemImage.objects.filter(item=item)
    more_videos = item.videos.all()

    # Get category-specific video (if exists)
    category_video = CategoryVideo.objects.filter(category=item.category).first()

    # Fetch tips related to the category (if available)
    category_video_tips = category_video.tips if category_video else None

    # Render the item detail page with the appropriate context
    return render(request, 'laviapp/item_detail.html', {
        'item': item,
        'more_images': more_images,
        'more_videos': more_videos,
        'category_video': category_video,
        'category_video_tips': category_video_tips,  # Add tips to context
    })




def item_details(request, item_id):
    # Fetch the item from the database
    item = get_object_or_404(Item, id=item_id)

    # Return the response rendering the item details template
    return render(request, 'laviapp/item_details.html', {'item': item})



def success(request):
    return render(request, 'laviapp/success.html')

def buy_now(request, item_id):
    # Get the item by ID
    item = get_object_or_404(Item, id=item_id)
    
    # Pass the item to the purchase details template
    return render(request, 'laviapp/purchase_details.html', {'item': item})

from razorpay.errors import BadRequestError, ServerError
import razorpay
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from .models import Item, Order, OrderItem



# Razorpay Order Creation
def create_razorpay_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            total_amount = data.get('total_amount')
            item_id = data.get('item_id')  # Single item for "buy now"
            email = data.get('email')
            full_name = data.get('full_name')
            mobile_number = data.get('mobile_number')

            if not (total_amount and item_id and email and full_name and mobile_number):
                return JsonResponse({'success': False, 'message': 'Missing required fields.'})

            # Setup Razorpay client
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

            # Create Razorpay order
            razorpay_order = client.order.create({
                'amount': int(float(total_amount) * 100),  # Convert to paise
                'currency': 'INR',
                'payment_capture': 1,
            })

            # Save the order in the database
            order = Order.objects.create(
                payment_id=razorpay_order['id'],
                payment_status='pending',
                total_price=total_amount,
                email=email,
                full_name=full_name,
                mobile_number=mobile_number,
            )

            # Save associated item(s) as OrderItem
            item = get_object_or_404(Item, id=item_id)
            OrderItem.objects.create(
                order=order,
                item=item,
                price=item.price,
                quantity=1  # Default to 1 for a single item purchase
            )

            return JsonResponse({
                'success': True,
                'order_id': razorpay_order['id'],
                'amount': razorpay_order['amount'],
            })

        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})



# Payment Success Handling
def razorpay_success(request):
    if request.method == 'POST':
        try:
            # Get payment details from the request
            data = json.loads(request.body)
            razorpay_payment_id = data.get('razorpay_payment_id')
            razorpay_order_id = data.get('razorpay_order_id')
            razorpay_signature = data.get('razorpay_signature')
            email = data.get('email')

            # Fetch the order using Razorpay order ID
            order = get_object_or_404(Order, payment_id=razorpay_order_id)

            # Verify payment (Razorpay signature verification)
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            try:
                client.utility.verify_payment_signature({
                    'razorpay_order_id': razorpay_order_id,
                    'razorpay_payment_id': razorpay_payment_id,
                    'razorpay_signature': razorpay_signature,
                })
            except razorpay.errors.SignatureVerificationError:
                return JsonResponse({'success': False, 'message': 'Payment verification failed.'})

            # Update the order status
            order.status = 'completed'
            order.payment_status = 'success'
            order.save()

            # Send email to the user
            order_items = OrderItem.objects.filter(order=order)
            email_body = f"Dear {order.full_name},\n\nThank you for your purchase. Below are the details of your order:\n\n"
            
            for order_item in order_items:
                item = order_item.item
                email_body += f"Item: {item.title}\n"
                if item.google_drive_link:
                    email_body += f"Download Link: {item.google_drive_link}\n\n"
                else:
                    email_body += (
                        "Download Link: Currently unavailable.\n"
                        "If you have any questions or need further assistance, please feel free to reach out to us.\n\n"
                    )

            # Add a professional closing message
            email_body += (
                "We are here to assist you with any concerns.\n"
                "Feel free to contact us at support@creativeassets.com or call our support team.\n\n"
                "Best regards,\n"
                "CreativeAssets Team"
            )

            send_mail(
                'Your Purchased Items',
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            return JsonResponse({'success': True, 'order_id': order.id})

        except Exception as e:
            return JsonResponse({'success': False, 'message': f'An error occurred: {str(e)}'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})




from django.http import Http404

def success(request):
    # Get the Razorpay order ID or the database order ID from the URL parameters
    order_id = request.GET.get('order_id')  # Razorpay order ID or database primary key

    try:
        # Try to fetch the order by primary key first
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        try:
            # If not found, try fetching it by Razorpay order ID (payment_id)
            order = Order.objects.get(payment_id=order_id)
        except Order.DoesNotExist:
            raise Http404("No Order matches the given query.")

    # Fetch associated order items
    order_items = OrderItem.objects.filter(order=order)
    total_price = sum([item.price for item in order_items])

    return render(request, 'laviapp/success.html', {
        'order': order,
        'order_items': order_items,
        'total_price': total_price,
        'email': order.email  # Pass email to the template
    })




from django.shortcuts import render
from .models import Order

def my_orders(request):
    if request.method == "POST":
        # Get the identifier from the user (e.g., email or mobile number)
        identifier = request.POST.get("identifier", "").strip()

        if identifier:
            # Fetch orders based on email or mobile number and order by most recent
            orders = (Order.objects.filter(email=identifier) | Order.objects.filter(mobile_number=identifier)) \
                .distinct() \
                .order_by('-created_at')  # Orders are now sorted by most recent

            # Pass orders and identifier to the template
            return render(request, 'laviapp/my_orders.html', {'orders': orders, 'identifier': identifier})
        else:
            # Handle case where no identifier is provided
            return render(request, 'laviapp/my_orders.html', {'error': "Please provide an email or mobile number."})
    
    # For GET requests, show the page without any orders
    return render(request, 'laviapp/my_orders.html')



