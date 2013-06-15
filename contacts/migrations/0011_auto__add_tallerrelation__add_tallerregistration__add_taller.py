# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'TallerRelation'
        db.create_table('contacts_tallerrelation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('taller_registration', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contacts.TallerRegistration'])),
            ('taller', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contacts.Taller'])),
            ('preference_order', self.gf('django.db.models.fields.IntegerField')(default=100, null=True, blank=True)),
            ('assigned', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('contacts', ['TallerRelation'])

        # Adding model 'TallerRegistration'
        db.create_table('contacts_regtaller', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('email_address', self.gf('django.db.models.fields.EmailField')(db_index=True, max_length=75, blank=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('remarks', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('date_registration', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('person', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['contacts.Person'], unique=True, null=True, blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('user_add', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='regtaller-add', null=True, to=orm['auth.User'])),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user_modify', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='regtaller-modified', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('contacts', ['TallerRegistration'])

        # Adding model 'Taller'
        db.create_table('contacts_taller', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('authors', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('day_scheduled', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('time_scheduled', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('building', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('room', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('max_attendants', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('contacts', ['Taller'])


    def backwards(self, orm):
        
        # Deleting model 'TallerRelation'
        db.delete_table('contacts_tallerrelation')

        # Deleting model 'TallerRegistration'
        db.delete_table('contacts_regtaller')

        # Deleting model 'Taller'
        db.delete_table('contacts_taller')


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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 15, 16, 35, 54, 824758)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 6, 15, 16, 35, 54, 824643)'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'comments.comment': {
            'Meta': {'ordering': "('submit_date',)", 'object_name': 'Comment', 'db_table': "'django_comments'"},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '3000'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type_set_for_comment'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_pk': ('django.db.models.fields.TextField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'submit_date': ('django.db.models.fields.DateTimeField', [], {'default': 'None'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'comment_comments'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'user_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'contacts.excursion': {
            'Meta': {'object_name': 'Excursion'},
            'accommodation_address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'accommodation_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'alergies': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_mailnotpaid': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_mailregister': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date_paid': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_registration': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'email_address': ('django.db.models.fields.EmailField', [], {'db_index': 'True', 'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'paid': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['contacts.Person']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'qty_bus': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'qty_celiac': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'qty_dinner': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'qty_excursion': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'qty_vegetarian': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pendent'", 'max_length': '15', 'blank': 'True'}),
            'user_add': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'excursion-add'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modify': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'excursion-modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'contacts.mailtemplate': {
            'Meta': {'object_name': 'MailTemplate'},
            'attachment': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'attachment2': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user_add': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'add'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modify': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'contacts.person': {
            'Meta': {'ordering': "('last_name', 'first_name')", 'object_name': 'Person', 'db_table': "'contacts_people'"},
            'about': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'contact_type': ('django.db.models.fields.CharField', [], {'default': "'R'", 'max_length': '1', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_mailnotpaid': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_mailregister': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date_paid': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_registration': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'email_address': ('django.db.models.fields.EmailField', [], {'db_index': 'True', 'max_length': '75', 'blank': 'True'}),
            'external_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'home_address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'home_postalcode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'home_province': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'home_town': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_card': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'laboral_category': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1', 'blank': 'True'}),
            'laboral_centeraddress': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'laboral_centercode': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'laboral_centername': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'laboral_centerphone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'laboral_centerpostalcode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'laboral_centerprovince': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'laboral_centertown': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'laboral_cuerpo': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '2', 'blank': 'True'}),
            'laboral_degree': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'laboral_levels': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'laboral_nrp': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'laboral_years': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '1', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'math_society': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '2', 'blank': 'True'}),
            'mobile_number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'paid': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'default': "'pendent'", 'max_length': '8', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pendent'", 'max_length': '15', 'blank': 'True'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '22', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'user_add': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'contact-add'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modify': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'contact-modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'contacts.taller': {
            'Meta': {'object_name': 'Taller'},
            'authors': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'building': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'day_scheduled': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_attendants': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'room': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'time_scheduled': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'contacts.tallerregistration': {
            'Meta': {'object_name': 'TallerRegistration', 'db_table': "'contacts_regtaller'"},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date_registration': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'email_address': ('django.db.models.fields.EmailField', [], {'db_index': 'True', 'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'person': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['contacts.Person']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tallers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'taller_registrations'", 'symmetrical': 'False', 'through': "orm['contacts.TallerRelation']", 'to': "orm['contacts.Taller']"}),
            'user_add': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'regtaller-add'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_modify': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'regtaller-modified'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'contacts.tallerrelation': {
            'Meta': {'object_name': 'TallerRelation'},
            'assigned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'preference_order': ('django.db.models.fields.IntegerField', [], {'default': '100', 'null': 'True', 'blank': 'True'}),
            'taller': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contacts.Taller']"}),
            'taller_registration': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contacts.TallerRegistration']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['contacts']
