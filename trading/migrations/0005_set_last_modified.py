# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        for order in orm.Order.objects.all():
            order.last_modified = order.placed_time
            order.save()


    def backwards(self, orm):
        "Write your backwards methods here."


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
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '6'})
        }
    }

    complete_apps = ['trading']
