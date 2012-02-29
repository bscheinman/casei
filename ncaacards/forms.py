from django import forms
import re


class TradeForm(forms.Form):
    side = forms.ChoiceField(choices=[('buy', 'Buy'), ('sell', 'Sell')])
    price = forms.CharField(max_length=10)
    quantity = forms.CharField(max_length=10)

    def clean(self):
        super(TradeForm, self).clean()
        cleaned_data = self.cleaned_data

        side = cleaned_data.get('side')
        price = cleaned_data.get('price')
        quantity = cleaned_data.get('quantity')

        if not side in ['buy', 'sell']:
            self._errors['side'] = self.error_class(['Invalid side type %s' % side])
            del cleaned_data['side']

        if price:
            price_pattern = r'\d+(\.\d{2})?'
            if not re.search(price_pattern, price):
                self._errors['price'] = self.error_class(['%s is not a valid price' % price])
                del cleaned_data['price']

        if quantity:
            try:
                q = int(quantity)
            except ValueError:
                self._errors['quantity'] = self.error_class(['You must enter a valid integer quantity'])
                del cleaned_data['quantity']
            else:
                if q <= 0:
                    self._errors['quantity'] = self.error_class(['Trade quantity must be greater than zero'])
                    del cleaned_data['quantity']

        return cleaned_data
