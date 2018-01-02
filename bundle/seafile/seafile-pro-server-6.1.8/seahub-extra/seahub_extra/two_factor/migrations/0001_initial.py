# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import seahub_extra.two_factor.models.base
import seahub.base.fields
import seahub_extra.two_factor.models.totp
import seahub_extra.two_factor.utils


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneDevice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', seahub.base.fields.LowerCaseCharField(help_text='The user that this device belongs to.', unique=True, max_length=255)),
                ('name', models.CharField(help_text='The human-readable name of this device.', max_length=64)),
                ('confirmed', models.BooleanField(default=True, help_text='Is this device ready for use?')),
                ('number', models.CharField(max_length=40)),
                ('key', models.CharField(default=seahub_extra.two_factor.utils.random_hex, help_text='Hex-encoded secret key', max_length=40, validators=[seahub_extra.two_factor.models.base.key_validator])),
                ('method', models.CharField(max_length=4, verbose_name='method', choices=[('call', 'Phone Call'), ('sms', 'Text Message')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StaticDevice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', seahub.base.fields.LowerCaseCharField(help_text='The user that this device belongs to.', unique=True, max_length=255)),
                ('name', models.CharField(help_text='The human-readable name of this device.', max_length=64)),
                ('confirmed', models.BooleanField(default=True, help_text='Is this device ready for use?')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StaticToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=16, db_index=True)),
                ('device', models.ForeignKey(related_name='token_set', to='two_factor.StaticDevice')),
            ],
        ),
        migrations.CreateModel(
            name='TOTPDevice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', seahub.base.fields.LowerCaseCharField(help_text='The user that this device belongs to.', unique=True, max_length=255)),
                ('name', models.CharField(help_text='The human-readable name of this device.', max_length=64)),
                ('confirmed', models.BooleanField(default=True, help_text='Is this device ready for use?')),
                ('key', models.CharField(default=seahub_extra.two_factor.models.totp.default_key, help_text='A hex-encoded secret key of up to 40 bytes.', max_length=80, validators=[seahub_extra.two_factor.models.totp.key_validator])),
                ('step', models.PositiveSmallIntegerField(default=30, help_text='The time step in seconds.')),
                ('t0', models.BigIntegerField(default=0, help_text='The Unix time at which to begin counting steps.')),
                ('digits', models.PositiveSmallIntegerField(default=6, help_text='The number of digits to expect in a token.', choices=[(6, 6), (8, 8)])),
                ('tolerance', models.PositiveSmallIntegerField(default=1, help_text='The number of time steps in the past or future to allow.')),
                ('drift', models.SmallIntegerField(default=0, help_text='The number of time steps the prover is known to deviate from our clock.')),
                ('last_t', models.BigIntegerField(default=-1, help_text='The t value of the latest verified token. The next token must be at a higher time step.')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'TOTP device',
            },
        ),
    ]
