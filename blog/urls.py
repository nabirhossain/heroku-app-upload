from django.urls import path
from . import views
app_name = 'blog'
urlpatterns = [
    path('',views.index,name='index'),
    path('detail/<int:id>',views.PostDetail, name='post_detail'),

]
