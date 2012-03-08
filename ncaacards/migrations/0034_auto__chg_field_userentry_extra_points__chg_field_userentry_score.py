# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'UserEntry.extra_points'
        db.alter_column('ncaacards_userentry', 'extra_points', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2))

        # Changing field 'UserEntry.score'
        db.alter_column('ncaacards_userentry', 'score', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2))


    def backwards(self, orm):
        
        # Changing field 'UserEntry.extra_points'
        db.alter_column('ncaacards_userentry', 'extra_points', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'UserEntry.score'
        db.alter_column('ncaacards_userentry', 'score', self.gf('django.db.models.fields.IntegerField')())


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
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ncaacards.Team']"})
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
            'points_limit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'position_limit': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'settings_locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'supports_cards': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'supports_stocks': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'ncaacards.scoretype': {
            'Meta': {'unique_together': "(('ordering', 'game_type'),)", 'object_name': 'ScoreType'},
            'default_score': ('django.db.models.fields.IntegerField', [], {}),
            'game_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'score_types'", 'to': "orm['ncaacards.GameType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {})
        },
        'ncaacards.scoringsetting': {
            'Meta': {'object_name': 'ScoringSetting'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ncaacards.NcaaGame']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'points': ('django.db.models.fields.IntegerField', [], {}),
            'scoreType': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ncaacards.ScoreType']"})
        },
        'ncaacards.team': {
            'Meta': {'object_name': 'Team'},
            'abbrev_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '6'}),
            'full_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'game_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'teams'", 'to': "orm['ncaacards.GameType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'ncaacards.teamscorecount': {
            'Meta': {'object_name': 'TeamScoreCount'},
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scoreType': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ncaacards.ScoreType']"}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'counts'", 'to': "orm['ncaacards.Team']"})
        },
        'ncaacards.tradecomponent': {
            'Meta': {'object_name': 'TradeComponent'},
            'count': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'offer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'components'", 'to': "orm['ncaacards.TradeSide']"}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ncaacards.GameTeam']"})
        },
        'ncaacards.tradeoffer': {
            'Meta': {'object_name': 'TradeOffer'},
            'accept_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'accepting_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'accepted_trades'", 'null': 'True', 'to': "orm['ncaacards.UserEntry']"}),
            'ask_side': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'ask_offer'", 'unique': 'True', 'to': "orm['ncaacards.TradeSide']"}),
            'bid_side': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'bid_offer'", 'unique': 'True', 'to': "orm['ncaacards.TradeSide']"}),
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'proposed_trades'", 'to': "orm['ncaacards.UserEntry']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'offer_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'ncaacards.tradeside': {
            'Meta': {'object_name': 'TradeSide'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'points': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'ncaacards.tradingblock': {
            'Meta': {'object_name': 'TradingBlock'},
            'entry': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'trading_block'", 'unique': 'True', 'to': "orm['ncaacards.UserEntry']"}),
            'game_teams_available': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'available_blocks'", 'symmetrical': 'False', 'to': "orm['ncaacards.GameTeam']"}),
            'game_teams_desired': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'desired_blocks'", 'symmetrical': 'False', 'to': "orm['ncaacards.GameTeam']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
        'ncaacards.userteam': {
            'Meta': {'object_name': 'UserTeam'},
            'count': ('django.db.models.fields.IntegerField', [], {}),
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'teams'", 'to': "orm['ncaacards.UserEntry']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ncaacards.GameTeam']"})
        }
    }

    complete_apps = ['ncaacards']
