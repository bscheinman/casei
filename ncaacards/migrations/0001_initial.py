# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'NcaaGame'
        db.create_table('ncaacards_ncaagame', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('starting_shares', self.gf('django.db.models.fields.IntegerField')(default=100)),
            ('starting_money', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('ncaacards', ['NcaaGame'])

        # Adding model 'UserEntry'
        db.create_table('ncaacards_userentry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ncaacards.NcaaGame'])),
            ('entry_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('ncaacards', ['UserEntry'])

        # Adding model 'Team'
        db.create_table('ncaacards_team', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('abbrev_name', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('score', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('ncaacards', ['Team'])

        # Adding model 'UserTeam'
        db.create_table('ncaacards_userteam', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ncaacards.UserEntry'])),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ncaacards.Team'])),
            ('count', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('ncaacards', ['UserTeam'])

        # Adding model 'TradingBlock'
        db.create_table('ncaacards_tradingblock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entry', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['ncaacards.UserEntry'], unique=True)),
        ))
        db.send_create_signal('ncaacards', ['TradingBlock'])

        # Adding M2M table for field teams_desired on 'TradingBlock'
        db.create_table('ncaacards_tradingblock_teams_desired', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tradingblock', models.ForeignKey(orm['ncaacards.tradingblock'], null=False)),
            ('team', models.ForeignKey(orm['ncaacards.team'], null=False))
        ))
        db.create_unique('ncaacards_tradingblock_teams_desired', ['tradingblock_id', 'team_id'])

        # Adding M2M table for field teams_available on 'TradingBlock'
        db.create_table('ncaacards_tradingblock_teams_available', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tradingblock', models.ForeignKey(orm['ncaacards.tradingblock'], null=False)),
            ('team', models.ForeignKey(orm['ncaacards.team'], null=False))
        ))
        db.create_unique('ncaacards_tradingblock_teams_available', ['tradingblock_id', 'team_id'])

        # Adding model 'TradeSide'
        db.create_table('ncaacards_tradeside', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dollar_amount', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('ncaacards', ['TradeSide'])

        # Adding model 'TradeOffer'
        db.create_table('ncaacards_tradeoffer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('bid_side', self.gf('django.db.models.fields.related.OneToOneField')(related_name='bid_offer', unique=True, to=orm['ncaacards.TradeSide'])),
            ('ask_side', self.gf('django.db.models.fields.related.OneToOneField')(related_name='ask_offer', unique=True, to=orm['ncaacards.TradeSide'])),
        ))
        db.send_create_signal('ncaacards', ['TradeOffer'])

        # Adding model 'TradeComponent'
        db.create_table('ncaacards_tradecomponent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ncaacards.Team'])),
            ('count', self.gf('django.db.models.fields.IntegerField')()),
            ('offer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ncaacards.TradeSide'])),
        ))
        db.send_create_signal('ncaacards', ['TradeComponent'])


    def backwards(self, orm):
        
        # Deleting model 'NcaaGame'
        db.delete_table('ncaacards_ncaagame')

        # Deleting model 'UserEntry'
        db.delete_table('ncaacards_userentry')

        # Deleting model 'Team'
        db.delete_table('ncaacards_team')

        # Deleting model 'UserTeam'
        db.delete_table('ncaacards_userteam')

        # Deleting model 'TradingBlock'
        db.delete_table('ncaacards_tradingblock')

        # Removing M2M table for field teams_desired on 'TradingBlock'
        db.delete_table('ncaacards_tradingblock_teams_desired')

        # Removing M2M table for field teams_available on 'TradingBlock'
        db.delete_table('ncaacards_tradingblock_teams_available')

        # Deleting model 'TradeSide'
        db.delete_table('ncaacards_tradeside')

        # Deleting model 'TradeOffer'
        db.delete_table('ncaacards_tradeoffer')

        # Deleting model 'TradeComponent'
        db.delete_table('ncaacards_tradecomponent')


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
        'ncaacards.ncaagame': {
            'Meta': {'object_name': 'NcaaGame'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'starting_money': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'starting_shares': ('django.db.models.fields.IntegerField', [], {'default': '100'})
        },
        'ncaacards.team': {
            'Meta': {'object_name': 'Team'},
            'abbrev_name': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'ncaacards.tradecomponent': {
            'Meta': {'object_name': 'TradeComponent'},
            'count': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'offer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ncaacards.TradeSide']"}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ncaacards.Team']"})
        },
        'ncaacards.tradeoffer': {
            'Meta': {'object_name': 'TradeOffer'},
            'ask_side': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'ask_offer'", 'unique': 'True', 'to': "orm['ncaacards.TradeSide']"}),
            'bid_side': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'bid_offer'", 'unique': 'True', 'to': "orm['ncaacards.TradeSide']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'ncaacards.tradeside': {
            'Meta': {'object_name': 'TradeSide'},
            'dollar_amount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'ncaacards.tradingblock': {
            'Meta': {'object_name': 'TradingBlock'},
            'entry': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['ncaacards.UserEntry']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'teams_available': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'available_blocks'", 'symmetrical': 'False', 'to': "orm['ncaacards.Team']"}),
            'teams_desired': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'desired_blocks'", 'symmetrical': 'False', 'to': "orm['ncaacards.Team']"})
        },
        'ncaacards.userentry': {
            'Meta': {'object_name': 'UserEntry'},
            'entry_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ncaacards.NcaaGame']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'ncaacards.userteam': {
            'Meta': {'object_name': 'UserTeam'},
            'count': ('django.db.models.fields.IntegerField', [], {}),
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ncaacards.UserEntry']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ncaacards.Team']"})
        }
    }

    complete_apps = ['ncaacards']
