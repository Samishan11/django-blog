from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from blog.models import Blog, Comment, LikeBlog, Replycomment

# Create your views here.
def home(request):
    blog = Blog.objects.all()
    animal = Blog.objects.filter(catagory="animal")
    travel = Blog.objects.filter(catagory="travel")
    nature = Blog.objects.filter(catagory="nature")
    blogid = request.GET.get("blogid")
    print(blogid)
    like = LikeBlog.objects.filter(blog=blogid).count()
    data = {
        "blog": blog,
        "like": like,
        "nature": nature,
        "tavel": travel,
        "animal": animal,
    }
    return render(request, "index.html", data)


def catagory(request):
    blog = Blog.objects.all()
    animal = Blog.objects.filter(catagory="animal")
    travel = Blog.objects.filter(catagory="travel")
    nature = Blog.objects.filter(catagory="nature")
    data = {   "blog": blog,}
    if  nature:
        return render(request, "catagory.html", {"nature": nature})
    elif animal:
        return render(request, "catagory.html", {"animal": animal})
    elif travel:
         return render(request, "index.html", {"travel":animal})
    else:
        return render(request, "index.html", data)

def animalblog(request):
    animal = Blog.objects.filter(catagory="animal")
    return render(request, "animalBlog.html", {"animal":animal})
def natureblog(request):
    nature = Blog.objects.filter(catagory="nature")
    return render(request, "naturebolg.html", {"nature": nature})
def travelblog(request):
    travel = Blog.objects.filter(catagory="travel")
    return render(request, "travelblog.html", {"travel": travel})

@login_required
def addblog(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        catagory = request.POST.get("catagory")
        image1 = request.FILES.get("image_1")
        Blog.objects.create(
            name=name, desc=description, catagory=catagory, image1=image1
        ).save()
    return render(request, "addblog.html")


def update(request, id):
    blog = Blog.objects.get(id=id)
    if request.method == "POST":
        blog.name = request.POST.get("name")
        blog.desc = request.POST.get("description")
        blog.catagory = request.POST.get("catagory")
        blog.image1 = request.FILES.get("image_1")
        blog.save()
    return render(request, "updateblog.html", {"blog": blog})


def blogdetail(request, id):
    blog = Blog.objects.get(id=id)
    comment = Comment.objects.filter(blog=blog ,parent=None)
    like = LikeBlog.objects.filter(blog=blog).count()
    replycomment = Comment.objects.filter(blog=blog).exclude(parent=None)
    replies = {}
    for reply in replycomment:
        if reply.parent.id not in replies.keys():
            replies[reply.parent.id]=[reply]
        else:
            replies[reply.parent.id].append(reply)
    # commentid  = Comment.objects.get(id=id)

    if request.method == "POST" and "comment" in request.POST:
        comment = request.POST.get("comment")
        parentId = request.POST.get('_COMMENT_ID')
        if parentId == None:
            cmnt = Comment.objects.create(blog=blog, text=comment)
        else:
            parent = Comment.objects.get(id=parentId)
            cmnt = Comment.objects.create(blog=blog, text=comment , parent=parent)
        cmnt.save()
        return redirect("/blog/" + str(blog.id) + "/")

    # if request.method == "POST" and "replycomment" in request.POST:
    #     commentid = request.GET.get("comment")
    #     text = request.POST.get("replycomment")
    #     print("commentid", commentid)
    #     Replycomment.objects.create(comment=commentid, text=text)
    #     return redirect("/blog/" + str(blog.id) + "/")

    return render(
        request, "blogdetail.html", {"blog": blog,'replies':replies, "comment": comment, "like": like}
    )

def deleteComment(requset, id):
    # blog = Blog.objects.get(id=id)
    id = requset.POST.get('_COMMENT_ID')
    id.delete()
    return redirect('/')

def replycomment(request,id):
    blog = Blog.objects.get(id=id)
    if request.method == "POST":
        comment = request.POST.get('_COMMENT_ID')
        print("Coment iD:",comment)
        text = request.POST.get("replycomment")
        Replycomment.objects.create(comment=comment, text=text)
    return redirect("/blog/" + str(blog.id) + "/")

def deleleteblog(request, id):
    blog = Blog.objects.get(id=id)
    blog.delete()
    return redirect("/")


def like(request, id):
    blog = Blog.objects.get(id=id)
    if request.method == "POST":
        like = 0
        if not "like":
            like = like + 1
        else:
            like = like - 1
        LikeBlog.objects.create(blog=blog, like=like)
    return redirect("/blog/" + str(blog.id) + "/")

def dislike(request, id):
    blog = Blog.objects.get(id=id)
    like = request.POST.get('like')
    like.delete()
    return redirect( "/")