from django.shortcuts import render, redirect
from django.template import loader
from django.http.response import HttpResponse, HttpResponseRedirect
from Jyp.settings import PAGE_SIZE, PAGE_BLOCK
from jypprj.models import  Post, Member, Comment, Like, PlayList
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
import re

import logging
logger = logging.getLogger('jypprj')


#메인
@csrf_exempt
def mainpage( request ) :
    template = loader.get_template( "mainpage.html" )
    memid = request.session.get("memid")
    post=Post.objects.all()

    posts = post.distinct().order_by("-readcount")[0:10]
    posts_ballad = post.filter(Q(genre__icontains="발라드")).distinct().order_by("-readcount")[0:8]
    posts_dance = post.filter(Q(genre__icontains="댄스")).distinct().order_by("-readcount")[0:8]
    posts_rap = post.filter(Q(genre__icontains="랩")|Q(genre__icontains="힙합")).distinct().order_by("-readcount")[0:8]
    posts_rnb = post.filter(Q(genre__icontains="R&B/Soul")).distinct().order_by("-readcount")[0:8]
        
    if memid :
        context = {
            "memid" : memid,
            "posts" : posts,
            "posts_ballad" : posts_ballad,
            "posts_dance" : posts_dance,
            "posts_rap" : posts_rap,
            "posts_rnb" : posts_rnb,
            }
    else :
        context = {
            "posts":posts,
            "posts" : posts,
            "posts_ballad" : posts_ballad,
            "posts_dance" : posts_dance,
            "posts_rap" : posts_rap,
            "posts_rnb" : posts_rnb,
            }
    return HttpResponse( template.render( context, request ) )

# 추천음악
@csrf_exempt
def recommend( request ) :
    template = loader.get_template( "recommend.html" )
    memid = request.session.get("memid")
    genre = request.GET.get("genre")
    likes = Like.objects.all()
    playlists = PlayList.objects.all()
    result = 0
    member = ""
    post=Post.objects.all()
    posts = post.distinct().order_by("-readcount")[0:100]
    
    try :
        member = Member.objects.get(id=memid)
        result = 0
        if genre == "ballad" :
            posts = post.filter(Q(genre__icontains="발라드")).distinct().order_by("-readcount")[0:100]
        elif genre == "dance" :
            posts = post.filter(Q(genre__icontains="댄스")).distinct().order_by("-readcount")[0:100]
        elif genre == "rap" :
            posts = post.filter(Q(genre__icontains="랩")|Q(genre__icontains="힙합")).distinct().order_by("-readcount")[0:100]
        elif genre == "rnb" :
            posts = post.filter(Q(genre__icontains="R&B/Soul")).distinct().order_by("-readcount")[0:100]
        else :
            posts = post.distinct().order_by("-readcount")[0:100]
    except ObjectDoesNotExist :
        result = 1
    
    if memid :
        like = likes.filter( user_id = memid )
        playlist = playlists.filter( user_id = memid )
        context = {
            "memid" : memid,
            "posts" : posts,
            "genre" : genre,
            "member" : member,
            "like" : like,
            "playlist" : playlist,
           }
    else :
        context = {
            "posts" : posts,
            "genre" : genre,
           }

    return HttpResponse( template.render( context, request ) )

# 장르별 전체음악
@csrf_exempt
def allgenre( request ) :
    template = loader.get_template( "allgenre.html" )
    memid = request.session.get("memid")
    genre = request.GET.get("genre")
    # likes = Like.objects.all()
    # playlists = PlayList.objects.all()
    page = request.GET.get("page")
    if not page :
        page = "1"
    page = int(page)
    
    
    start = (page - 1) * int(PAGE_SIZE)
    end = start + int(PAGE_SIZE)
    count = Post.objects.all().count()
    
    if end > count :
        end = count
        
    number = 0 + (page-1) * int(PAGE_SIZE)       # 50 - (2-1) * 10
    
    startpage = page // PAGE_BLOCK * PAGE_BLOCK + 1  # 5 / 10
    if page % PAGE_BLOCK == 0 :
        startpage -= PAGE_BLOCK
    
    endpage = startpage + PAGE_BLOCK - 1                # 11 + 10 - 1
    pagecount = count // PAGE_SIZE                      
    
    if count % PAGE_SIZE > 0 :
        pagecount += 1
    if endpage > pagecount :
        endpage = pagecount

    pages = range(startpage, endpage+1)
    
    post=Post.objects.all()
    
    if genre == "ballad" :
        posts = post.filter(Q(genre__icontains="발라드")).distinct().order_by("-readcount")[start:end]
    elif genre == "dance" :
        posts = post.filter(Q(genre__icontains="댄스")).distinct().order_by("-readcount")[start:end]
    elif genre == "rap" :
        posts = post.filter(Q(genre__icontains="랩")|Q(genre__icontains="힙합")).distinct().order_by("-readcount")[start:end]
    elif genre == "soul" :
        posts = post.filter(Q(genre__icontains="R&B/Soul")).distinct().order_by("-readcount")[start:end]
    elif genre == "trot" :
        posts = post.filter(Q(genre__icontains="트로트")).distinct().order_by("-readcount")[start:end]
    elif genre == "fork" :
        posts = post.filter(Q(genre__icontains="포크/블루스")).distinct().order_by("-readcount")[start:end]
    elif genre == "rock" :
        posts = post.filter(Q(genre__icontains="록/메탈")).distinct().order_by("-readcount")[start:end]
    elif genre == "indi" :
        posts = post.filter(Q(genre__icontains="인디음악")).distinct().order_by("-readcount")[start:end]
    else :
        posts = post.distinct().order_by("-readcount")[start:end]

    
        # dtos = Board.objects.order_by("-ref", "restep")[start:end]
    if memid :
        
        try:
            like = Like.objects.get(user_id = memid)
            playlist = PlayList.objects.get( user_id = memid )
        except :
            like =  {"user_id":"adminadmin", "num":"-1"}
            playlist = {"user_id":"adminadmin", "num":"-1"}
            
        
        context = {
            "memid" : memid,
            "posts" : posts,
            "genre" : genre,
            "page" : page,
            "number" : number,
            "startpage" : startpage,
            "endpage" : endpage,
            "pageblock" : PAGE_BLOCK,
            "pagecount" : pagecount,
            "pages" : pages,
            "like" : like,
            "playlist" : playlist,
            }
    else :
        context = {
            "posts" : posts,
            "genre" : genre,
            "page" : page,
            "number" : number,
            "startpage" : startpage,
            "endpage" : endpage,
            "pageblock" : PAGE_BLOCK,
            "pagecount" : pagecount,
            "pages" : pages,
           }
    return HttpResponse( template.render( context, request ) )

#음악세부정보
@csrf_exempt
def musicdetail(request):
    template = loader.get_template("musicdetail.html")
    memid = request.session.get("memid")
    commentss=Comment.objects.all()
    
    
    if memid:
        if request.method == "GET":
            num = request.GET.get("num")
            post = Post.objects.get(num=num)
            comments = commentss.filter(num=post.num).order_by("-regdate")
            post.readcount +=1
            post.save()
           
            like = Like.objects.get(user_id = memid)
            playlist = PlayList.objects.get( user_id = memid )

            member = Member.objects.get(id = memid)
            
            context = {
                "playlist":playlist,
                "like" : like,
                "memid" : memid,
                "post":post,
                "comments":comments,
                "num":num,
                
            }
        else:
            member = Member.objects.get(id=memid)
            num=request.POST["num"]
            content = request.POST.get("ctxt","")
            post = Post.objects.get(num=num)
            
            if memid:
                if content != "":
                    dto =Comment(
                        num=post.num,
                        content=content,
                        user_id=member,
                        )
                    dto.save()
                    logger.info(member.gender+","+member.birthday[0:2]+","+post.title+","+post.singer+","+post.genre+",C")
                    return redirect(request.POST["next"])
                else:
                    pass
            else:
                pass
        
    else :
        if request.method == "GET":
            num = request.GET.get("num")
            post = Post.objects.get(num=num)
        else:
            num=request.POST["num"]
            post = Post.objects.get(num=num)
        comments = commentss.filter(num=post.num).order_by("-regdate")
        post.readcount +=1
        post.save()
        
        context = {
            "post":post,
            "comments":comments,
            "num":num,
        }
    
    return render(request,"musicdetail.html",context)

# 좋아요 추가
@csrf_exempt
def Like_set(request):
    memid = request.session.get("memid")
    num = request.GET.get("num")
    member = Member.objects.get(id=memid)
    post = Post.objects.get(num = num)
    likes = Like.objects.all()
    
    if likes.filter(user_id = memid):
        like=Like.objects.get(user_id = memid)
        if  str(post.num) not in str(like.num):
            like.num = str(like.num) +" "+str(post.num)
            like.save()
            logger.info(member.gender+","+member.birthday[0:2]+","+post.title+","+post.singer+","+post.genre+",L")
    else:
        dto =Like(
        num = post.num,
        user_id = member,
        )
        dto.save()
    
    return redirect(request.GET.get('next'))
# 좋아요 삭세
@csrf_exempt
def Like_del(request):
    memid = request.session.get("memid")
    num = request.GET.get("num")
    member = Member.objects.get(id=memid)
    post = Post.objects.get(num = num)
    like = Like.objects.get(user_id=member.id)
    like.num = like.num.replace(post.num, "")
    like.save()
    
    
    return redirect(request.GET.get('next'))

# 플레이리스트 추가
@csrf_exempt
def playlist_set( request ) :
    memid = request.session.get( "memid" )
    num = request.GET.get("num")
    member = Member.objects.get(id=memid)
    post = Post.objects.get(num = num)
    
    plays = PlayList.objects.all()
    
    if plays.filter(user_id = memid):
        play=PlayList.objects.get(user_id = memid)
        if  str(post.num) not in str(play.num):
            play.num = str(play.num) +" "+str(post.num)
            play.save()
            logger.info(member.gender+","+member.birthday[0:2]+","+post.title+","+post.singer+","+post.genre+",P")
    else:
        dto = PlayList(
            num = post.num,
            user_id = member,
            )
        
        dto.save()
    
    return redirect(request.GET.get('next'))

# 플레이리스트 삭제
@csrf_exempt
def playlist_del( request ):
    memid = request.session.get("memid")
    num = request.GET.get("num")
    member = Member.objects.get(id=memid)
    post = Post.objects.get(num = num)
    playlist = PlayList.objects.get(user_id=member.id)
    playlist.num = playlist.num.replace(post.num, "")
    playlist.save()
    
    
    
    return redirect(request.GET.get('next'))

# 로그인 페이지
@csrf_exempt
def loginpage( request ) :
    template = loader.get_template( "loginpage.html" )
    next = request.GET.get('next')
    context = {"next":next,}
    return HttpResponse( template.render( context, request ) )

# 로그인 확인
@csrf_exempt
def loginpro( request ) :
    id = request.POST["id"]
    passwd = request.POST["passwd"]
    msg = ""
    template = loader.get_template( "loginpage.html" )
    url_path = request.POST.get('next')
    path = []
    path = url_path.split("?next=")
    try :
        # 아이디가 있을 때
        dto = Member.objects.get( id = id )
        
        if passwd == dto.passwd :
            # 비밀번호 일치
            request.session["memid"] = id
            if url_path:
                return redirect(path[-1])
            else : 
                return redirect("mainpage")
        else: 
            msg="비밀번호가 틀립니다."

    except ObjectDoesNotExist :
        # 아이디가 없을 때
        msg = "입력하신 아이디가 없습니다."
    context = {
        "msg" : msg,
        }
    return HttpResponse( template.render( context, request ) )

# 로그아웃
def logout( request ) :
    del( request.session["memid"] )
    return redirect("mainpage")
   

# 비번 찾기
def pw_recover( request ) :
    template = loader.get_template( "pw_recover.html" )
    id = request.GET.get("id")
    birthday = request.GET.get("birthday")
    passwd = ""
    result = 0
    msg = ""
    try :
        # 아이디가 있을 때
        dto = Member.objects.get( id = id )
        try :
            #생년월일 있을 때
            # dtos = Member.objects.get( birthday = birthday )
            if dto.birthday == birthday :
                passwd = dto.passwd
                result = 0
            else :
                msg = "아이디와 생년월일이 일치하지 않습니다."
                result = 1
        except ObjectDoesNotExist :
            #생년월일 없을 때
            msg = "존재하지 않는 생년월일입니다."
            result = 1
    except ObjectDoesNotExist :
        # 아이디 없을 때
        msg = "존재하지 않는 아이디입니다."
        result = 1
    context = {
        "id" : id,
        "msg" : msg,
        "passwd" : passwd,
        "result" : result,
        }
    return HttpResponse( template.render( context, request ) )

# 회원탈퇴
@csrf_exempt
def deletepro( request ) :
    id = request.session.get( "memid" )
    passwd = request.POST.get( "passwd" )
    dto = Member.objects.get( id = id )
    if passwd == dto.passwd :
        dto.delete()
        del( request.session["memid"] )
        return redirect( "mainpage" )
    else :
        template = loader.get_template( "deletepage.html" )
        context = {
            "msg" : "비밀번호를 잘못 입력하였습니다."
            }
        return HttpResponse( template.render( context, request ) )
    
# 회원정보 페이지
def memberpage( request ) :
    template = loader.get_template( "memberpage.html" )
    memid = request.session.get("memid")
    result = 0
    comments = Comment.objects.all()
    posts = Post.objects.all()
    count = 0
    
    try :
        comment = comments.filter(user_id=memid).order_by("-regdate")
        member = Member.objects.get(id=memid) 
        result = 0
    except ObjectDoesNotExist :
        result = 1
    context = {
            "memid" : memid,
            "comment" : comment,
            "result" : result,
            "posts":posts,
            "count":count,
            "member":member,
            }   
    return HttpResponse( template.render( context, request ) )

#회원가입
def registerpage(request):
    template = loader.get_template("registerpage.html")
    
    context={}
    return  HttpResponse(template.render(context,request))

#회원가입
@ csrf_exempt
def registerpro( request ) :
    id = request.POST["id"]
    dto = Member(
        id = request.POST["id"],
        passwd = request.POST["passwd"],
        name = request.POST["name"],
        birthday = request.POST["birthday"],
        gender = request.POST["gender"],
        )
    dto.save()
    member = Member.objects.get(id=id)
    playlist = PlayList(
        num = "",
        user_id = member,
        )
    playlist.save()
    like = Like(
        num = "",
        user_id = member,
        )
    like.save()
    
    return redirect("mainpage")

# 아이디 중복확인
@csrf_exempt
def idconfirm( request ) :
    id = request.POST["id"]
    members = Member.objects.all()
    check = False
    reg = re.compile(r'[a-zA-Z1-9]')
    for member in members :
        if id == member.id :
            check= True
            break;
        
    if check : 
        return HttpResponse("중복되는 아이디 입니다.")
    else :
        if reg.match(id):
            return HttpResponse("사용가능한 아이디입니다.")
        else:
            return HttpResponse("영어와 숫자만 입력해주세요.")
    
    # template = loader.get_template( "idconfirm.html" )
    # id = request.GET["id"]
    # result = 0
    # try :
        # Member.objects.get(id=id)
        # result = 1
    # except ObjectDoesNotExist :
        # result = 0
    # context = {
        # "result" : result,
        # "id" : id
        # }
    # return HttpResponse( template.render( context, request ) )

# 회원가입-닉네임 중복확인
@csrf_exempt
def nameconfirm( request ) :
    nickname = request.POST["nickname"]
    dtos = Member.objects.all()
    check = False
    for dto in dtos :
        if nickname == dto.name :
            check= True
            break;
        
    if check : 
        return HttpResponse("중복되는 닉네임 입니다.")
    else :
        return HttpResponse("사용가능한 닉네임입니다.")
    
    
    
    # template = loader.get_template( "nameconfirm.html" )
    # name = request.GET["name"]
    # result = 0
    # try :
        # Member.objects.get(name=name)
        # result = 1
    # except ObjectDoesNotExist : 
        # result = 0
    # context = {
        # "result" : result,
        # "name" : name
        # }
    # return HttpResponse( template.render( context, request ) )

# 수정-닉네임 중복확인
@csrf_exempt
def nameconfirm1( request ) :
    template = loader.get_template( "nameconfirm1.html" )
    name = request.GET["name"]
    result = 0
    try :
        Member.objects.get(name=name)
        result = 1
    except ObjectDoesNotExist : 
        result = 0
    context = {
        "result" : result,
        "name" : name
        }
    return HttpResponse( template.render( context, request ) )



def modify( request ) :
    memid = request.session.get( "memid" )
    template = loader.get_template( "modify.html" )
    context = {
            "memid":memid,
            }
    return HttpResponse( template.render( context, request ) )

#회원정보 수정
@csrf_exempt
def modifyview( request ) :
    memid = request.session.get( "memid" )
    passwd = request.POST["passwd"]
    dto = Member.objects.get( id = memid )
    if passwd == dto.passwd :
        template = loader.get_template( "modifyview.html" )        
        context = {
            "dto" : dto,
            "memid":memid,
            }
    else :
        template = loader.get_template( "modify.html" )
        context = {
            "msg" : "입력하신 비밀번호가 다릅니다.",
            "memid":memid,
            }
    return HttpResponse( template.render( context, request ) )

@csrf_exempt
def modifypro( request ) :
    memid = request.session.get( "memid" )
    dto = Member.objects.get( id = memid )
    dto.passwd = request.POST["passwd"]
    dto.name = request.POST["name"]
    dto.gender = request.POST["gender"]
    dto.save()    
    return redirect( "mainpage" )


#댓글 삭제
def comment_del(request):
    memid = request.session.get("memid")
    num = request.GET.get("num")
    regdate = request.GET.get("regdate")
    comments = Comment.objects.all()
    comment = comments.filter(regdate__icontains=regdate,num=num,user_id=memid)
    comment.delete()
    comments=Comment.objects.order_by("-regdate")
    return redirect(request.GET.get('next'))

#검색
@csrf_exempt
def search(request):
    template = loader.get_template("search.html")
    memid = request.session.get("memid")
    if request.method == "POST":
        sword = request.POST.get("sword","")
        # sselect=request.POST.get("sselect","제목")
    else:
        sword = request.GET.get("sword","")
        # sselect=request.GET.get("sselect","제목")
    
    post =  Post.objects.all()
    msg =""
    
    if sword=="":
            msg="입력된 검색어가 없습니다."
            context={"msg":msg}
    else:
       
        posts = post.filter(Q(title__icontains=sword)|Q(singer__icontains=sword)).distinct().order_by("title")
        count = post.filter(Q(title__icontains=sword)|Q(singer__icontains=sword)).distinct().count()
                
        context={
            "count":count,
            "posts":posts,
            "sword":sword, 
            
            "msg" : msg,
            "memid":memid,
            }
    
    return HttpResponse(template.render(context,request))

# 보관함 (내 댓글, 좋아요 한 노래 리스트, 재생목록에 추가한 노래 리스트)
def storage(request) :
    template = loader.get_template("storage.html")
    memid = request.session.get("memid")
    select = request.GET.get("select")
    comments = Comment.objects.all()
    posts = Post.objects.all()
    result = 0
    count = 0
    member=""
    comment=""
    playlist = ""
    like = ""
    
    if select == "playlist" :
        try :
            playlist = PlayList.objects.get( user_id = memid )
            result = 0
        except ObjectDoesNotExist :
            result = 1
    elif select == "commentlist" : 
        try :
            comment = comments.filter(user_id=memid).order_by("-regdate")
            member = Member.objects.get(id=memid) 
            result = 0
        except ObjectDoesNotExist :
            result = 1
    else :
        try :
            like = Like.objects.get( user_id = memid )
            result = 0
        except ObjectDoesNotExist :
            result = 1
    context = {
            "memid" : memid,
            "comment" : comment,
            "result" : result,
            "posts":posts,
            "count":count,
            "member":member,
            "select":select,
            "like" : like,
            "playlist" : playlist,
            }   
    return HttpResponse( template.render( context, request ) )







