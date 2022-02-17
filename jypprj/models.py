from django.db import models
from jypprj.choice import GENDER_CHOICE


class Post(models.Model):
    num = models.CharField(verbose_name="글번호",null=True,unique=True, blank=True,max_length=250)
    singer = models.CharField(verbose_name="가수",null=True, max_length=20, blank=True)
    title = models.CharField(verbose_name="노래제목",null=True, max_length=40, blank=True)
    regdate= models.DateTimeField( auto_now_add=True, verbose_name="작노래제목성일", blank=True )
    readcount= models.IntegerField( verbose_name="조회수", default=0 , blank=True)
    genre =models.CharField(verbose_name="장르",null=True,max_length=20, blank=True)
    

class Member(models.Model):
    id = models.CharField(verbose_name="아이디", primary_key=True, max_length=20)
    passwd = models.CharField(verbose_name="비밀번호",null=False, max_length=30)
    name = models.CharField(verbose_name="닉네임",null=False,unique=True, max_length=20)
    birthday = models.CharField(verbose_name="생년월일",null=False, max_length=10)
    gender = models.CharField(choices=GENDER_CHOICE,null=False,max_length=10)
    com_genre = models.CharField(verbose_name="추천장르",null=True, blank=True,max_length=20)
    
class Comment(models.Model):
    content= models.CharField(verbose_name="내용",null=True,max_length=200)
    regdate= models.DateTimeField( auto_now_add=True, verbose_name="작성일", blank=True )
    num = models.CharField(verbose_name="작성위치",null=True,max_length=250)
    user_id = models.ForeignKey(Member,on_delete=models.CASCADE,related_name="member")
    
class Like(models.Model):
    user_id = models.ForeignKey(Member,on_delete=models.CASCADE,related_name="like_member")
    num = models.CharField(verbose_name="글번호",null=False, blank=True,max_length=250)
    
class PlayList(models.Model) :
    user_id = models.ForeignKey(Member,on_delete=models.CASCADE,related_name="playlist_member")
    num = models.CharField(verbose_name="글번호",null=False, blank=True,max_length=250)
    

