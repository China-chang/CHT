# Generated by Django 3.1.2 on 2020-12-20 14:07

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cname', models.CharField(max_length=30, unique=True, verbose_name='类别名称')),
            ],
            options={
                'verbose_name_plural': '类别',
                'db_table': 'luntan_category',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tname', models.CharField(max_length=30, unique=True, verbose_name='标签名称')),
            ],
            options={
                'verbose_name_plural': '标签',
                'db_table': 'luntan_tag',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100, verbose_name='用户名')),
                ('password', models.CharField(max_length=100, verbose_name='密码')),
                ('ctime', models.DateTimeField()),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'db_table': 'luntan_user',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('desc', models.CharField(max_length=100)),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('like_count', models.IntegerField(default=0)),
                ('comment_count', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sixi.userinfo', verbose_name='作者')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sixi.category')),
                ('tag', models.ManyToManyField(to='sixi.Tag')),
            ],
            options={
                'verbose_name_plural': '帖子',
                'db_table': 'luntan_post',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255, verbose_name='评论内容')),
                ('ctime', models.DateTimeField(auto_now_add=True, verbose_name='评论时间')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pid', to='sixi.comment')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sixi.post', verbose_name='文章')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sixi.userinfo', verbose_name='评论者')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ctime', models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sixi.post', verbose_name='点赞的文章')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sixi.userinfo', verbose_name='点赞者')),
            ],
            options={
                'unique_together': {('user', 'post')},
            },
        ),
    ]
