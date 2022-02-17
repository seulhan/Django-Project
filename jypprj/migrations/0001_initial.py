# Generated by Django 3.2.7 on 2021-11-29 19:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='아이디')),
                ('passwd', models.CharField(max_length=30, verbose_name='비밀번호')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='닉네임')),
                ('birthday', models.CharField(max_length=10, verbose_name='생년월일')),
                ('gender', models.CharField(choices=[('남성', '남성'), ('여성', '여성')], max_length=10)),
                ('com_genre', models.CharField(blank=True, max_length=20, null=True, verbose_name='추천장르')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.CharField(blank=True, max_length=200, null=True, unique=True, verbose_name='글번호')),
                ('singer', models.CharField(blank=True, max_length=20, null=True, verbose_name='가수')),
                ('title', models.CharField(blank=True, max_length=40, null=True, verbose_name='노래제목')),
                ('regdate', models.DateTimeField(auto_now_add=True, verbose_name='작노래제목성일')),
                ('readcount', models.IntegerField(blank=True, default=0, verbose_name='조회수')),
                ('genre', models.CharField(blank=True, max_length=20, null=True, verbose_name='장르')),
            ],
        ),
        migrations.CreateModel(
            name='PlayList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.CharField(blank=True, max_length=200, verbose_name='글번호')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='playlist_member', to='jypprj.member')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.CharField(blank=True, max_length=200, verbose_name='글번호')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like_member', to='jypprj.member')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=200, null=True, verbose_name='내용')),
                ('regdate', models.DateTimeField(auto_now_add=True, verbose_name='작성일')),
                ('num', models.IntegerField(null=True, verbose_name='작성위치')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member', to='jypprj.member')),
            ],
        ),
    ]
