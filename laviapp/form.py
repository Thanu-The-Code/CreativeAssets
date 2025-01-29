from django import forms
from .models import Item

class OrderForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)
    item = forms.ModelChoiceField(queryset=Item.objects.all(), 
                                  to_field_name='id', 
                                  widget=forms.HiddenInput)
from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    category = forms.ChoiceField(
        choices=Item.CATEGORY_CHOICES,
        widget=forms.Select,
        required=True
    )
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Enter title'}),
        required=True
    )

    class Meta:
        model = Item
        fields = ['category', 'title', 'description', 'price', 'main_image']




from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

