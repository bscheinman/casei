from casei.ncaacards.logic import get_team_from_identifier
from casei.ncaacards.models import NcaaGame, GameType
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


class CreateGameForm(forms.Form):
    type_choices = []
    for gtype in GameType.objects.all():
        type_choices.append((gtype, gtype))

    game_name = forms.CharField(max_length=50)
    game_type = forms.ChoiceField(type_choices)
    starting_shares = forms.CharField(max_length=10)
    starting_points = forms.CharField(max_length=10)
    game_password = forms.CharField(widget=forms.PasswordInput, required=False)
    entry_name = forms.CharField(max_length=30)
    support_cards = forms.BooleanField(required=False)
    support_stocks = forms.BooleanField(required=False)

    def clean(self):
        super(CreateGameForm, self).clean()
        cleaned_data = self.cleaned_data

        game_name = cleaned_data.get('game_name', '')
        game_type_str = cleaned_data.get('game_type', '')
        starting_shares_str = cleaned_data.get('starting_shares', '')
        starting_points_str = cleaned_data.get('starting_points', '')
        game_password = cleaned_data.get('game_password', '')
        entry_name = cleaned_data.get('entry_name', '')
        support_cards = cleaned_data.get('support_cards', False)
        support_stocks = cleaned_data.get('support_stocks', False)

        if game_name:
            try:
                g = NcaaGame.objects.get(name=game_name)
            except NcaaGame.DoesNotExist:
                pass
            else:
                self._errors['game_name'] = self.error_class(['A game with already exists with the name %s' % game_name])
                del cleaned_data['game_name']
        else:
            self._errors['game_name'] = self.error_class(['You must specify a game name'])

        if game_type_str:
            try:
                game_type = GameType.objects.get(name=game_type_str)
            except GameType.DoesNotExist:
                self._errors['game_type'] = self.error_class(['%s is not a valid game type' % game_type_str])
                del cleaned_data['game_type']
            else:
                cleaned_data['game_type'] = game_type
        else:
            self._errors['game_type'] = self.error_class(['You must specify a game type'])

        if starting_shares_str:
            try:
                starting_shares = int(starting_shares_str)
            except ValueError:
                self._errors['starting_shares'] = self.error_class(['You must enter a valid number of starting shares'])
                del cleaned_data['starting_shares']
            else:
                if starting_shares <= 0:
                    self._errors['starting_shares'] = self.error_class(['You must enter a positive number of starting shares'])
                    del cleaned_data['starting_shares']
                else:
                    cleaned_data['starting_shares'] = starting_shares
        else:
            self._errors['starting_shares'] = self.error_class(['You must specify a number of starting shares'])

        if starting_points_str:
            try:
                starting_points = int(starting_points_str)
            except ValueError:
                self._errors['starting_points'] = self.error_class(['You must enter a valid number of starting points'])
                del cleaned_data['starting_points']
            else:
                if support_stocks:
                    if starting_points <= 0:
                        self._errors['starting_points'] = self.error_class(['Games supporting stock-style trading must give entries at least 1 point to start'])
                        del cleaned_data['starting_points']
                    else:
                        cleaned_data['starting_points'] = starting_points
        else:
            self._errors['starting_points'] = self.error_class(['You must specify a number of starting points'])
        

        if not support_cards and not support_stocks:
            self._errors['support_cards'] = self.error_class(['You must select at least one trading type'])

        if not entry_name:
            self._errors['entry_name'] = self.error_class(['You must provide a name for your entry'])

        return cleaned_data
