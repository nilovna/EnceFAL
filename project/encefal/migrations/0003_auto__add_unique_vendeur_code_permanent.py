# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Vendeur', fields ['code_permanent']
        db.create_unique(u'encefal_vendeur', ['code_permanent'])


    def backwards(self, orm):
        # Removing unique constraint on 'Vendeur', fields ['code_permanent']
        db.delete_unique(u'encefal_vendeur', ['code_permanent'])


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'encefal.exemplaire': {
            'Meta': {'object_name': 'Exemplaire'},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'date_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modification': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'etat': ('django.db.models.fields.CharField', [], {'default': "'VENT'", 'max_length': '4'}),
            'facture': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'exemplaires'", 'null': 'True', 'db_column': "'facture'", 'to': u"orm['encefal.Facture']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'livre': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'exemplaires'", 'db_column': "'livre'", 'to': u"orm['encefal.Livre']"}),
            'prix': ('django.db.models.fields.IntegerField', [], {}),
            'vendeur': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'exemplaires'", 'db_column': "'vendeur'", 'to': u"orm['encefal.Vendeur']"})
        },
        u'encefal.facture': {
            'Meta': {'object_name': 'Facture'},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'date_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modification': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'employe': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'factures'", 'blank': 'True', 'db_column': "'employe'", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'factures'", 'blank': 'True', 'db_column': "'session'", 'to': u"orm['encefal.Session']"})
        },
        u'encefal.livre': {
            'Meta': {'object_name': 'Livre'},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'auteur': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'date_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modification': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'edition': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '13', 'blank': 'True'}),
            'titre': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'vendeur': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'livres'", 'symmetrical': 'False', 'through': u"orm['encefal.Exemplaire']", 'db_column': "'vendeur'", 'to': u"orm['encefal.Vendeur']"})
        },
        u'encefal.session': {
            'Meta': {'object_name': 'Session'},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'date_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_debut': ('django.db.models.fields.DateField', [], {}),
            'date_fin': ('django.db.models.fields.DateField', [], {}),
            'date_modification': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'encefal.vendeur': {
            'Meta': {'object_name': 'Vendeur'},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'code_permanent': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12'}),
            'date_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modification': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'prenom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['encefal']