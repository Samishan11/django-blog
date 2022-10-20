
from django.urls import path
from . import views
urlpatterns = [
    path('',views.home),
    path('addblog/',views.addblog),
    path('updateblog/<int:id>/',views.update),
    path('blog/<int:id>/',views.blogdetail),
    path('deleteblog/<int:id>/',views.deleleteblog),
    path('deletecmnt/<int:id>/',views.deleteComment),
    path('like/<int:id>/',views.like),
    path('dislike/<int:id>/',views.dislike),
    path('replycomment/<int:id>/',views.replycomment),
    path('catagory?/',views.catagory),
    path('catagory/animal/',views.animalblog),
    path('catagory/nature/',views.natureblog),
    path('catagory/travel/',views.travelblog),
]
