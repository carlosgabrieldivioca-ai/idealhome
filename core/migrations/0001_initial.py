from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Property",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=500)),
                ("price", models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ("location", models.CharField(blank=True, max_length=1000)),
                ("typology", models.CharField(blank=True, max_length=50)),
                ("bathrooms", models.CharField(blank=True, max_length=100)),
                ("description", models.TextField(blank=True)),
                ("features", models.TextField(blank=True)),
                ("gallery", models.TextField(blank=True)),
                ("source_link", models.URLField(blank=True, max_length=1000)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-id"]},
        ),
    ]
