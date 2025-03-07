# Generated by Django 2.1.7 on 2019-05-09 08:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0005_auto_20190422_0732'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnonComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(max_length=32)),
                ('author_email', models.EmailField(max_length=254)),
                ('comment_date', models.DateTimeField(auto_now_add=True)),
                ('comment_content', models.TextField(max_length=4000)),
                ('anon_parent', models.BooleanField()),
                ('anon_response', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.Response')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(blank=True, max_length=40, unique=True)),
            ],
            options={
                'ordering': ['tag_name'],
            },
        ),
        migrations.CreateModel(
            name='UserComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_date', models.DateTimeField(auto_now_add=True)),
                ('comment_content', models.TextField(max_length=4000)),
                ('anon_response', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.Response')),
                ('comment_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_date', models.DateTimeField(auto_now_add=True)),
                ('response_content', models.TextField(max_length=4000)),
            ],
        ),
        migrations.AlterField(
            model_name='article',
            name='article_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AddField(
            model_name='userresponse',
            name='parent_article',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.Article'),
        ),
        migrations.AddField(
            model_name='userresponse',
            name='response_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usercomment',
            name='user_response',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.UserResponse'),
        ),
        migrations.AddField(
            model_name='anoncomment',
            name='user_response',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.UserResponse'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to='myapp.Tag'),
        ),
    ]
