# Generated by Django 4.0.7 on 2022-08-22 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='글 제목')),
                ('contents', models.TextField(verbose_name='글 내용')),
                ('write_dttm', models.DateTimeField(auto_now_add=True, verbose_name='글 작성일')),
                ('board_name', models.CharField(default='Python', max_length=32, verbose_name='게시판 종류')),
                ('update_dttm', models.DateTimeField(auto_now=True, verbose_name='마지막 수정일')),
                ('hits', models.PositiveIntegerField(default=0, verbose_name='조회수')),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user', verbose_name='작성자')),
            ],
            options={
                'verbose_name': '게시판',
                'verbose_name_plural': '게시판',
                'db_table': 'board',
            },
        ),
    ]
