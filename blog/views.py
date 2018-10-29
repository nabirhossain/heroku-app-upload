from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, Http404
from .models import author,category,post
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator 
from django.db.models import Q

# Create your views here.
def index(request):
    post1 = post.objects.all() 
    search = request.GET.get('q')
    if search:
        post1 = post1.filter(                  
            Q(post_title__icontains = search)|
            Q(post_body__icontains = search)
        )
    paginator = Paginator(post1, 8)  
    page = request.GET.get('page')
    TotalPost = paginator.get_page(page)
    context = {
        'post1':TotalPost       
    }
    return render(request,'index.html', context) 

def PostDetail(request, id):
    post1 = get_object_or_404(post, pk=id)      
    first = post.objects.first()                
    last = post.objects.last()                 
    related = post.objects.filter(post_category=post1.post_category).exclude(id=id)[:4] 
    context ={                                 
        "post1":post1,
        "first":first,
        "last":last,
        "related":related
    }
    return render(request,'post_detail.html', context) 

