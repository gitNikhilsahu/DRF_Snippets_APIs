from django import forms
from .models import ProductModel

class ProductForm(forms.ModelForm):
    no = forms.IntegerField(min_value=101)
    class Meta:
        model = ProductModel
        fields = '__all__'