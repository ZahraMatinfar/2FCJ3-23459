# Generated by Django 5.1.1 on 2024-09-17 23:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(db_index=True, default=True, help_text='Designates whether this item should be treated as active. Unselected this instead of deleting.', verbose_name='Active status')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Creation On')),
                ('updated_time', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Modified On')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ads', to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'verbose_name': 'Ad',
                'verbose_name_plural': 'Ads',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(db_index=True, default=True, help_text='Designates whether this item should be treated as active. Unselected this instead of deleting.', verbose_name='Active status')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Creation On')),
                ('updated_time', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Modified On')),
                ('text', models.TextField(verbose_name='Text')),
                ('ad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='ads.ad', verbose_name='Ad')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
                'constraints': [models.UniqueConstraint(fields=('ad', 'user'), name='unique_comment_per_ad_user')],
            },
        ),
    ]
