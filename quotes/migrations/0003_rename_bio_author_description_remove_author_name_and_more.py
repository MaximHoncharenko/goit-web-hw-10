# Generated by Django 5.1.5 on 2025-01-18 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0002_alter_tag_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='bio',
            new_name='description',
        ),
        migrations.RemoveField(
            model_name='author',
            name='name',
        ),
        migrations.AddField(
            model_name='author',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='author',
            name='birth_place',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='author',
            name='fullname',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
