# Generated by Django 3.2.7 on 2021-10-05 08:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Userreg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('emailid', models.CharField(max_length=30)),
                ('phoneno', models.CharField(max_length=30)),
                ('useraddress', models.CharField(max_length=30)),
                ('pincode', models.CharField(max_length=30)),
                ('birthday', models.CharField(max_length=30)),
                ('gender', models.CharField(max_length=30)),
                ('upassword', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Apbook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apdatetime', models.CharField(max_length=30)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('usid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='u_app.userreg')),
            ],
        ),
    ]
