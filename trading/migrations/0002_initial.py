# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Market'
        db.create_table('trading_market', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
        ))
        db.send_create_signal('trading', ['Market'])

        # Adding model 'Security'
        db.create_table('trading_security', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('market', self.gf('django.db.models.fields.related.ForeignKey')(related_name='securities', to=orm['trading.Market'])),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=6)),
        ))
        db.send_create_signal('trading', ['Security'])

        # Adding model 'Order'
        db.create_table('trading_order', (
            ('order_id', self.gf('casei.fields.UUIDField')(unique=True, max_length=32, primary_key=True)),
            ('placer', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('security', self.gf('django.db.models.fields.related.ForeignKey')(related_name='orders', to=orm['trading.Security'])),
            ('placed_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')()),
            ('quantity_remaining', self.gf('django.db.models.fields.IntegerField')()),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('is_buy', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('trading', ['Order'])

        # Adding model 'Execution'
        db.create_table('trading_execution', (
            ('security', self.gf('django.db.models.fields.related.ForeignKey')(related_name='executions', to=orm['trading.Security'])),
            ('execution_id', self.gf('casei.fields.UUIDField')(unique=True, max_length=32, primary_key=True)),
            ('buy_order', self.gf('django.db.models.fields.related.ForeignKey')(related_name='buy_executions', to=orm['trading.Order'])),
            ('sell_order', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sell_executions', to=orm['trading.Order'])),
            ('quantity', self.gf('django.db.models.fields.IntegerField')()),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('trading', ['Execution'])


    def backwards(self, orm):
        
        # Deleting model 'Market'
        db.delete_table('trading_market')

        # Deleting model 'Security'
        db.delete_table('trading_security')

        # Deleting model 'Order'
        db.delete_table('trading_order')

        # Deleting model 'Execution'
        db.delete_table('trading_execution')


    models = {
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        'trading.order': {
            'Meta': {'object_name': 'Order'},
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_buy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'order_id': ('casei.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'primary_key': 'True'}),
            'placed_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'placer': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {}),
            'quantity_remaining': ('django.db.models.fields.IntegerField', [], {}),
            'security': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders'", 'to': "orm['trading.Security']"})
        },
        'trading.security': {
            'Meta': {'object_name': 'Security'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'market': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'securities'", 'to': "orm['trading.Market']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '6'})
        }
    }

    complete_apps = ['trading']
