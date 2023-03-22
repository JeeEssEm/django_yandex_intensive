# Generated by Django 3.2.8 on 2023-03-22 15:37

import catalog.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re
import sorl.thumbnail.fields
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название, длина не более 150 символов', max_length=150, verbose_name='название')),
                ('is_published', models.BooleanField(default=True, verbose_name='опубликовано')),
                ('slug', models.SlugField(help_text='Человекочитаемый формат URL', max_length=200, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), 'Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.', 'invalid')], verbose_name='слаг')),
                ('weight', models.PositiveIntegerField(default=100, help_text='Введите массу, значение не больше 32767 и не меньше 1', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(32767)], verbose_name='Масса')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название, длина не более 150 символов', max_length=150, verbose_name='название')),
                ('is_published', models.BooleanField(default=True, verbose_name='опубликовано')),
                ('slug', models.SlugField(help_text='Человекочитаемый формат URL', max_length=200, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), 'Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.', 'invalid')], verbose_name='слаг')),
            ],
            options={
                'verbose_name': 'тег',
                'verbose_name_plural': 'теги',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название, длина не более 150 символов', max_length=150, verbose_name='название')),
                ('is_published', models.BooleanField(default=True, verbose_name='опубликовано')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('text', tinymce.models.HTMLField(validators=[catalog.validators.ValidateMustContain('превосходно', 'роскошно')], verbose_name='описание')),
                ('is_on_main', models.BooleanField(default=False, verbose_name='на главной странице')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.category', verbose_name='категория')),
                ('tags', models.ManyToManyField(to='catalog.Tag')),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'товары',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', sorl.thumbnail.fields.ImageField(upload_to='catalog/', verbose_name='прикрепите изображение')),
                ('item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='main_image', to='catalog.item', verbose_name='товар')),
            ],
            options={
                'verbose_name': 'изображение',
                'verbose_name_plural': 'изображения',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', sorl.thumbnail.fields.ImageField(upload_to='catalog/', verbose_name='прикрепите изображение')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery', to='catalog.item', verbose_name='товар')),
            ],
            options={
                'verbose_name': 'изображение',
                'verbose_name_plural': 'изображения',
                'abstract': False,
            },
        ),
    ]
