# Generated by Django 4.2.16 on 2024-12-01 17:25

from django.db import migrations, models
import django.db.models.deletion
import pgvector.django.vector


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Embeddings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('embedding', pgvector.django.vector.VectorField(dimensions=1536)),
                ('embedding_creation_date', models.DateTimeField(auto_now_add=True)),
                ('uploaded_document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='embeddings', to='document.uploadeddocument')),
            ],
        ),
    ]
