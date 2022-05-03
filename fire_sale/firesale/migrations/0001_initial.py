# Generated by Django 3.2.13 on 2022-05-03 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=8192)),
                ('condition', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('bio', models.CharField(max_length=8192)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=255)),
                ('personal_information', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firesale.personalinformation')),
                ('user_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firesale.image')),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('is_accepted', models.BooleanField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firesale.item')),
                ('user_offering', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firesale.user')),
            ],
        ),
        migrations.CreateModel(
            name='ItemImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firesale.image')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firesale.item')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firesale.user'),
        ),
    ]
