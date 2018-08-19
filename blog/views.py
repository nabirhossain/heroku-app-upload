from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, Http404
from .models import author,category,post # মডেল  থেকে  সকল  ফিল্ড  ইম্পোর্ট করে নিতে হবে
from django.contrib.auth import authenticate, login, logout #  ইউজার অথেনটিকেশন এর জন্য authenticate, login, logout মডিউল গুলো ইম্পোর্ট করে নিতে হবে
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator  #  সাইটে পেজিনেশন এড করার জন্য EmptyPage, PageNotAnInteger, Paginator মডিউল গুলো ইম্পোর্ট করে নিতে হবে
from django.db.models import Q #  জ্যাঙ্গোর বিল্ট-ইন Q লুক আপ কল করা হয়েছে
from .forms import CreateForm, registerUser, createAuthor, categoryForm
from django.contrib import messages

## registration with email imports
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
# close registration import
# token import
from .token import activation_token
# close token
# Create your views here.
def index(request):
    post1 = post.objects.all() #  পোষ্ট মডেলের সমস্ত অবজেক্ট নিয়ে এসে post1 ভেরিয়েবলে রাখবে
    search = request.GET.get('q') # get  ম্যথডের মাধ্যমে সেন্ড করা q কে রিসিভ করে search ভ্যেরিয়েবুলে রাখা হয়েছে
    if search:
        post1 = post1.filter(                   # post1 ভ্যরিয়েবলে ফিল্টার করে post1 ভ্যেরিয়েবলেই রাখা হয়েছে
            Q(post_title__icontains = search)|
            Q(post_body__icontains = search)
        )
    paginator = Paginator(post1, 8)  #  প্রতি পেজে ৪ টি করে পোষ্ট দেখানো হবে
    page = request.GET.get('page')
    TotalPost = paginator.get_page(page)
    context = {
        #'post1':post1       #  কন্টেক্সট ভেরিয়েবলে সেগুলো ষ্টোর করা
        'post1':TotalPost       # post1 হিসেবে ইনডেক্স ট্যামপ্লেটে ভ্যেরিয়েবল পাঠানো হয়েছে
    }
    return render(request,'index.html', context) #  কনটেক্সট ভেরিয়েবলটি ট্যামপ্লেটে পাঠানো

def getAuthor(request, name):
    p_author = get_object_or_404(User, username=name)  # ইউজারের নাম ইউজার মডেল থেকে নিয়ে এসে p_author ভ্যেরিয়াবলে রাখা হয়েছে
    auth = get_object_or_404(author, auth_name=p_author.id) #  পোষ্ট দাতার নাম author মডেল থেকে নিয়ে এসে auth ভ্যেরিয়াবলে রাখা হয়েছে
    post1 = post.objects.filter(post_author=auth.id) #  post_author এর  আইডি অনুসারে post মডেল থেকে ফিল্টার করে পোষ্টগুলো নিয়ে এসে post1 ভ্যেরিয়াবলে রাখা হয়েছে
    paginator = Paginator(post1, 8)  # প্রতি পেজে ৪ টি করে পোষ্ট দেখানো হবে
    page = request.GET.get('page')
    TotalPost = paginator.get_page(page)
    context = {                                       # auth এবং post1 ভ্যারিয়েবলগুলো কন্টেক্সট ভ্যেরিয়েবলে ঢুকিয়ে দেওয়া হয়েছে
        'auth':auth,
        'post1':TotalPost,
    }
    return render(request,'author.html', context) #  কন্টেক্সট ভ্যেরিয়েবলে থাকা ভ্যালুগুলো ট্যামপ্লেটে পাঠানো হয়েছে

def PostDetail(request, id):
    post1 = get_object_or_404(post, pk=id)      #   প্রাইমারি কী অনুসারে পোষ্ট মডেল থেকে আইডি অনুসারে পোষ্ট দেখানোর কুয়েরী চালনা
    first = post.objects.first()                # পোষ্ট মডেলের প্রথম পোষ্টটি দেখানোর  কুয়েরী
    last = post.objects.last()                  # পোষ্ট মডেলের  সর্বশেষ পোষ্টটি দেখানোর  কুয়েরী
    related = post.objects.filter(post_category=post1.post_category).exclude(id=id)[:4]  # আমাদের পোষ্টের রিলেটেড পোষ্ট গুলো দেখানোর  জন্য এই ভেরিয়েবলটি  নেওয়া হয়েছে
    context ={                                  #  কন্টেক্সট ভ্যেরিয়েবলে উপরের ভ্যারিয়েবলগুলো ঢুকিয়ে দেওয়া হয়েছে
        "post1":post1,
        "first":first,
        "last":last,
        "related":related
    }
    return render(request,'post_detail.html', context) #  কন্টেক্সট ভ্যেরিয়েবলে থাকা ভ্যালুগুলো ট্যামপ্লেটে পাঠানো হয়েছে

def PostTopic(request, name):
    topic = get_object_or_404(category, name=name)       #  ক্যাটাগরি মডেল থেকে ক্যাটাগরির নাম উপরের name প্যারামিটারের যুক্ত করে দিয়েছি
    post1 = post.objects.filter(post_category=topic.id)  #  একই ক্যাটাগরির পোষ্ট দেখার জন্য ফিল্টারের মধ্যে post_category মডেলের সাথে ক্যাটাগরির id যুক্ত করে দিয়েছি
    paginator = Paginator(post1, 8)  # প্রতি পেজে ৪ টি করে পোষ্ট দেখানো হবে
    page = request.GET.get('page')
    TotalPost = paginator.get_page(page)
    return render(request,'category.html', {"post1":TotalPost, "topic":topic }) #   দুটি  ভ্যারিয়েবলকে ট্যামপ্লেটে পাঠানো হয়েছে

def LogIn(request):      #(অথেনটিকেশন এর জন্য from django.contrib.auth import authenticate, login, logout এই মডিউলটি এড  করে নিতে হবে )
    if request.user.is_authenticated:                    # ইউজার যদি অথেন্টিকেটেড হয়
        return redirect('blog:index')                    # তাহলে index  পেজে রিডাইরেক্ট হবে
    else:                                               #  আর যদি ইউজার অথেন্টিকেটেড না হয়
        if request.method == "POST":                     #  যদি রিকোয়েস্ট ম্যাথডটি পোষ্ট হয়
            user = request.POST.get('user')      #  লগ ইন ট্যামপ্লেটের ইউজার নেমকে user ভ্যেরিয়েবলে নিয়ে  নেবে
            password = request.POST.get('pass')  #  লগ ইন ট্যামপ্লেটের  পাসওয়ার্ড নেমকে password ভ্যেরিয়েবলে নিয়ে  নেবে
            auth = authenticate(request, username=user, password=password)  # auth ভেরিয়েবলে ইউজারের  ইউজার নেম ও পাসওয়ার্ড  দ্বারা অথেনটিকেশন চেক করা হবে
            if auth is not None:                 #  যদি  অথেনটিকেশন None না হয়
                login(request, auth)             # তবে আমরা লগ ইন করব
                return redirect('blog:index')    #  সফলভাবে লগ ইন হলে index পেজে রিডাইরেক্ট হবে (get_object_or_404 এর পরে redirect মডিউলটি এড করে নিতে হবে)
            else:
                messages.add_message(request, messages.ERROR, 'username or password not match')
                return render(request, 'login.html')
    return render(request,'login.html')         #  আর যদি সফলভাবে লগ ইন না হয় তাহলে সে login পেজে পাঠিয়ে দিবে

def LogOut(request):
    logout(request)               # পেজ থেকে লগ আউট করে নিয়ে  আসবে
    return redirect('blog:index') # পেজ থেকে লগ আউট করে index পেজে রিডাইরেক্ট করবে

def CreatePost(request):
    if request.user.is_authenticated: #  যদি ইউজার  লগ ইন অবস্থায় থাকে তাহলে পোষ্ট তৈরি করতে পারবে
        u = get_object_or_404(author, auth_name= request.user.id) # author  মডেলের  রেজিষ্টার্ড ইউজারকে নিয়ে এসে u ভ্যারিয়েবলে রাখবে
        form = CreateForm(request.POST or None, request.FILES or None)  # ফরমটি যদি পোষ্ট হয়
        if form.is_valid():  # ফরমটি যদি ভ্যালিড হয়
            instance = form.save(commit=False)  # তাহলে instance ভেরিয়েবলে সেভ করে রাখবে
            instance.post_author = u
            instance.save()  # instance  টি সেভ করবে
            return redirect('blog:index')  # অতঃপর ইনডেক্স পেজে রিডাইরেক্ট করবে
        return render(request, 'create.html', {"form": form})
    else:                                # আর যদি ইউজার লগ ইন করা না থাকে তাহলে লগইন পেজে নিয়ে যাবে
        return redirect('blog:login')

def PostUpdate(request, id):
    if request.user.is_authenticated:
        u = get_object_or_404(author, auth_name= request.user.id)
        post1 = get_object_or_404(post, id=id)
        form = CreateForm(request.POST or None, request.FILES or None, instance=post1)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.post_author = u
            instance.save()
            messages.success(request, "Post updated successfully")
            return redirect('blog:profile')
        return render(request, 'create.html', {"form": form})
    else:
        return redirect('blog:login')

def PostDelete(request, id):
    if request.user.is_authenticated:
        post1 = get_object_or_404(post, id=id)
        post1.delete()
        messages.warning(request, 'post deleted successfully')
        return redirect('blog:profile')
    else:
        return redirect('blog:login')


def profile(request):
    if request.user.is_authenticated:  # যদি ইউজার  লগ ইন অবস্থায় থাকে তাহলে পোষ্ট তৈরি করতে পারবে
        #user = get_object_or_404(author, auth_name= request.user.id)
        user = get_object_or_404(User, id= request.user.id)
        author_profile = author.objects.filter(auth_name = user.id)
        if author_profile:
            authorUser = get_object_or_404(author, auth_name = request.user.id)
            post1 = post.objects.filter(post_author = authorUser.id)
            return render(request, 'profile.html', {"post1":post1}, {"user":authorUser})
        else:
            form = createAuthor(request.POST or None, request.FILES or None)
            if form.is_valid():
                instance = form.save(commit = False)
                instance.auth_name = user
                instance.save()
                return redirect('blog:profile')
            return render(request, 'createAuthor.html', {"form":form})
    else:
        return redirect('blog:login')


def register(request):
    form =registerUser(request.POST or None)
    if form.is_valid():
        instance = form.save(commit = False)
        instance.is_active = False                                  #  ইউজার একটিভ না করা পর্যন্ত একটিভ হবে না
        instance.save()
        site = get_current_site(request)
        mail_subject = "confirmation message for blog"
        message = render_to_string('confirmation_email.html',{
            'user': instance,
            'domain': site.domain,
            'uid' : instance.id,
            'token': activation_token.make_token(instance)
        })
        to_email = form.cleaned_data.get('email')
        to_list = [to_email]
        from_email = settings.EMAIL_HOST_USER
        send_mail(mail_subject, message, from_email, to_list, fail_silently=True)
        return HttpResponse("<h1>Thanks for your registration. A confirmation link was sent to your mail</h1>")
        #messages.success(request, 'Registration has been successfully completed')
        #return redirect('blog:login')
    return render(request, 'register.html', {"form":form})

def ShowTopic(request):
    query = category.objects.all()
    return render(request, "AllTopic.html", {"topic":query})




def AddCategory(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            form = categoryForm(request.POST or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                messages.success(request, "topics created successfully")
                return redirect('blog:category')
            return render(request, "CreateTopics.html", {"form": form})
        else:
            raise Http404("Access denied")
    else:
        return redirect('blog:login')


"""
"""
def activate(request, uid, token):
    try:
        user = get_object_or_404(User, pk=uid)
    except:
        raise Http404("No user found")
    if user is not None and activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse("<h1>Account is activated. Now you can <a href='/login'>login</a></h1>")
    else:
        return HttpResponse("<h3>Invalid activation</h3>")











