# Generated by Django 4.2.19 on 2025-03-02 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('product_id', models.CharField(max_length=255)),
                ('product_type', models.CharField(max_length=50)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'unique_together': {('user_id', 'product_id', 'product_type')},
            },
        ),
    ]
