# inventory/forms.py
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'quantity', 'price']
        widgets = {
            'name': forms.TextInput(attrs={
                'required': True,
                'oninvalid': "this.setCustomValidity('Please enter a product name.')",
                'oninput': "this.setCustomValidity('')"
            }),
            'quantity': forms.NumberInput(attrs={
                'required': True,
                'min': 1,
                'oninvalid': "this.setCustomValidity('Quantity must be at least 1.')",
                'oninput': "this.setCustomValidity('')"
            }),
            'price': forms.NumberInput(attrs={
                'required': True,
                'min': 0.01,
                'step': '0.01',
                'oninvalid': "this.setCustomValidity('Price must be greater than zero.')",
                'oninput': "this.setCustomValidity('')"
            }),
        }
