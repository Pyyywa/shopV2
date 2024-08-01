from catalog.models import Product, Version
from django.forms import ModelForm, BooleanField, ValidationError, HiddenInput


class StyleFormMixin(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class ProductForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        exclude = ('views_count', 'slug','owner')

    BLACKLIST = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно',
                 'обман', 'полиция', 'радар']

    def clean_product_name(self):
        cleaned_data = self.cleaned_data["product_name"]
        for word in self.BLACKLIST:
            if word in cleaned_data.lower():
                raise ValidationError(f'Наименование не должно содержать слово {word}')
        return cleaned_data

    def clean_desc(self):
        cleaned_data = self.cleaned_data["desc"]
        for word in self.BLACKLIST:
            if word in cleaned_data.lower():
                raise ValidationError(f'Описание не должно содержать слово {word}')
        return cleaned_data


class VersionForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Version
        fields = '__all__'
