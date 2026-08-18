from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(model_name="property", name="address", field=models.CharField(blank=True, max_length=500)),
        migrations.AddField(model_name="property", name="district", field=models.CharField(blank=True, max_length=100)),
        migrations.AddField(model_name="property", name="municipality", field=models.CharField(blank=True, max_length=150)),
        migrations.AddField(model_name="property", name="parish", field=models.CharField(blank=True, max_length=250)),
    ]
