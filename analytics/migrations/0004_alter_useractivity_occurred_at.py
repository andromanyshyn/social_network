# Generated by Django 4.2.5 on 2023-09-14 17:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("analytics", "0003_useractivity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="useractivity",
            name="occurred_at",
            field=models.DateTimeField(),
        ),
    ]
