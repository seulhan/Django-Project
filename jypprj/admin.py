from django.contrib import admin
from jypprj.models import Member, Post, Comment, Like, PlayList

class MemberAdmin( admin.ModelAdmin ) :
    list_display = ( "id", "passwd", "name", "birthday", "gender")
    list_editable=( "passwd", "birthday", "gender")
admin.site.register( Member, MemberAdmin )

class PostAdmin(admin.ModelAdmin):
    list_display=("num","singer","title","genre","regdate","readcount")
    list_editable=("singer","title","genre","readcount")
    list_per_page = 300
admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display=("num","user_id","content","regdate")
admin.site.register(Comment, CommentAdmin)
 
class LikeAdmin(admin.ModelAdmin):
    list_display=("user_id","num")
admin.site.register( Like, LikeAdmin )

class PlayListAdmin(admin.ModelAdmin):
    list_display=("user_id","num")
admin.site.register( PlayList, PlayListAdmin )
