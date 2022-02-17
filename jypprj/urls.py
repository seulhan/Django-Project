from django.urls import path
from jypprj import views 
from django.views.generic.base import TemplateView

urlpatterns = [
    path("mainpage", views.mainpage, name="mainpage"),
    path("comment_del", views.comment_del, name="comment_del"),
    path( "search", views.search, name="search" ), 
    path("allgenre", views.allgenre, name="allgenre"),
    path("musicdetail", views.musicdetail, name="musicdetail"),
    path("Like_set", views.Like_set, name="Like_set"),
    path("Like_del", views.Like_del, name="Like_del"),
    path("playlist_set", views.playlist_set, name="playlist_set"),
    path("playlist_del", views.playlist_del, name="playlist_del"),
    path("recommend", views.recommend, name="recommend"),
    
    path( "loginpage", views.loginpage, name="loginpage" ),
    path( "loginpro", views.loginpro, name="loginpro" ), 
    path( "logout", views.logout, name="logout" ),
    path( "recover", TemplateView.as_view( template_name="recover.html") ),
    path( "pw_recover", views.pw_recover, name="pw_recover" ),
    path( "deletepage", TemplateView.as_view( template_name="deletepage.html") ),
    path( "deletepro", views.deletepro, name="deletepro" ),
    path( "memberpage", views.memberpage, name="memberpage" ),
    path( "registerpage", views.registerpage, name="registerpage" ),
    path( "storage", views.storage, name="storage" ),
    
    path("registerpage", views.registerpage, name="registerpage"),
    path("registerpage", TemplateView.as_view(template_name="registerpage.html")), 
    path("registerpro", views.registerpro, name="registerpro"),
    path("idconfirm", views.idconfirm, name="idconfirm"),
    path("nameconfirm", views.nameconfirm, name="nameconfirm"),
    path("nameconfirm1", views.nameconfirm1, name="nameconfirm1"),
    
    path("modify", views.modify,name="modify"),
    path("modifyview", views.modifyview, name="modifyview"), 
    path("modifypro", views.modifypro, name="modifypro"),
    
    
    
    

]

