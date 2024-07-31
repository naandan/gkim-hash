from django.db import migrations

def create_general_setting(apps, schema_editor):
    GeneralSetting = apps.get_model('setting', 'Setting')
    GeneralSetting.objects.create()

class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_general_setting),
    ]