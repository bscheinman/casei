# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Order.entry'
        db.add_column('trading_order', 'entry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ncaacards.UserEntry'], null=True, blank=True), keep_default=False)

        # Adding field 'Security.team'
        db.add_column('trading_security', 'team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ncaacards.GameTeam'], null=True, blank=True), keep_default=False)

        # Adding field 'Market.game'
        db.add_column('trading_market', 'game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ncaacards.NcaaGame'], null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Order.entry'
        db.delete_column('trading_order', 'entry_id')

        # Deleting field 'Security.team'
        db.delete_column('trading_security', 'team_id')

        # Deleting field 'Market.game'
        db.delete_column('trading_market', 'game_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'ncaacards.gameteam': {
            'Meta': {'object_name': 'GameTeam'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ncaacards.NcaaGame']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ncaacards.Team']"}),
            'volume': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'ncaacards.gametype': {
            'Meta': {'object_name': 'GameType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        'ncaacards.ncaagame': {
            'Meta': {'object_name': 'NcaaGame'},
            'game_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'games'", 'to': "orm['ncaacards.GameType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'points_limit': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'position_limit': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'settings_locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'supports_cards': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'supports_stocks': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'ncaacards.team': {
            'Meta': {'object_name': 'Team'},
            'abbrev_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '6'}),
            'full_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'game_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'teams'", 'to': "orm['ncaacards.GameType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_eliminated': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'ncaacards.userentry': {
            'Meta': {'unique_together': "(('game', 'entry_name'),)", 'object_name': 'UserEntry'},
            'entry_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'extra_points': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '12', 'decimal_places': '2'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': "orm['ncaacards.NcaaGame']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'join_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'score': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '12', 'decimal_places': '2'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': "orm['auth.User']"})
        },
        'trading.execution': {
            'Meta': {'object_name': 'Execution'},
            'buy_order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'buy_executions'", 'to': "orm['trading.Order']"}),
            'execution_id': ('casei.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {}),
            'security': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'executions'", 'to': "orm['trading.Security']"}),
            'sell_order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sell_executions'", 'to': "orm['trading.Order']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'trading.market': {
            'Meta': {'object_name': 'Market'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ncaacards.NcaaGame']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        'trading.order': {
            'Meta': {'object_name': 'Order'},
            'cancel_on_game': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ncaacards.UserEntry']", 'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_buy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'order_id': ('casei.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'primary_key': 'True'}),
            'placed_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'placer': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {}),
            'quantity_remaining': ('django.db.models.fields.IntegerField', [], {}),
            'security': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders'", 'to': "orm['trading.Security']"})
        },
        'trading.security': {
            'Meta': {'unique_together': "(('market', 'name'),)", 'object_name': 'Security'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'market': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'securities'", 'to': "orm['trading.Market']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ncaacards.GameTeam']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['trading']
