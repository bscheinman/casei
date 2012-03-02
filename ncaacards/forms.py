from django import forms
from decimal import *


class TradeForm(forms.Form):
    team_identifier = forms.CharField(max_length=10)
    side = forms.ChoiceField(choices=[('buy', 'Buy'), ('sell', 'Sell')])
    price = forms.CharField(max_length=10)
    quantity = forms.CharField(max_length=10)

    def clean(self):
        super(TradeForm, self).clean()
        cleaned_data = self.cleaned_data

        team_identifier = cleaned_data.get('team_identifier')
        side = cleaned_data.get('side')
        price = cleaned_data.get('price')
        quantity = cleaned_data.get('quantity')

        if not side in ['buy', 'sell']:
            self._errors['side'] = self.error_class(['Invalid side type %s' % side])
            del cleaned_data['side']

        if team_identifier:
            team = get_team_from_identifier(team_identifier)
            if team:
                cleaned_data['team'] = team
            else:
                self._errors['team_identifier'] = self.error_class(['Invalid team identifier %s' % team_identifier])
                del cleaned_data['team_identifier']

        if price:
            try:
                p = Decimal(price)
                cleaned_data['price'] = p
            except ValueError:
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
                else:
                    cleaned_data['quantity'] = q

        return cleaned_data
