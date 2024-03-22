# Generated by Django 5.0.1 on 2024-03-17 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebTabs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DraggableData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forms_name', models.CharField(blank=True, max_length=100, null=True)),
                ('field_name', models.CharField(blank=True, max_length=100, null=True)),
                ('field_type', models.CharField(blank=True, max_length=100, null=True)),
                ('x_axis', models.CharField(default=None, max_length=255)),
                ('y_axis', models.CharField(default=None, max_length=255)),
                ('color', models.CharField(default='value', max_length=50)),
                ('padding_size', models.CharField(default=None, max_length=255)),
            ],
        ),
    ]
