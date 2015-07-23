# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, verbose_name='\u7c7b\u522b\u540d\u79f0')),
                ('isIncome', models.BooleanField(verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe6\x94\xb6\xe5\x85\xa5', choices=[(True, '\u6536\u5165'), (False, '\u652f\u51fa')])),
                ('p_category', models.ForeignKey(related_name='child', verbose_name='\u7236\u7c7b\u540d\u79f0', blank=True, to='jizhang.Category', null=True)),
                ('user', models.ForeignKey(verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.DecimalField(verbose_name=b'\xe9\x87\x91\xe9\xa2\x9d', max_digits=10, decimal_places=2)),
                ('comment', models.CharField(max_length=200, verbose_name=b'\xe6\xb3\xa8\xe9\x87\x8a', blank=True)),
                ('pub_date', models.DateField(verbose_name=b'\xe6\x97\xa5\xe6\x9c\x9f')),
                ('category', models.ForeignKey(verbose_name=b'\xe5\x88\x86\xe7\xb1\xbb', to='jizhang.Category')),
            ],
        ),
    ]
