# Generated by Django 3.2.18 on 2023-03-05 06:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0004_video_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoAllProxy',
            fields=[
            ],
            options={
                'verbose_name': 'All Video',
                'verbose_name_plural': 'All Videos',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('videos.video',),
        ),
    ]
