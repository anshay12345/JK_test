# Generated by Django 4.2.16 on 2024-12-02 16:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0002_embeddings'),
    ]

    operations = [
        migrations.AddField(
            model_name='embeddings',
            name='content',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]