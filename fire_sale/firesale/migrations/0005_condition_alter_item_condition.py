# Generated by Django 4.0.4 on 2022-05-05 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('firesale', '0004_auto_20220505_1145'),
    ]

    operations = [
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='item',
            name='condition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firesale.condition'),
        ),
    ]