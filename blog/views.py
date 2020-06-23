from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, ContactUs, Profile, Category
from .forms import CommentForm, BlogForm, EditForm, ContactUsForm, SignUpForm, ProfileForm, UserForm
from django.views import generic
from django.http import HttpResponse
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic import RedirectView
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, get_user_model 
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.contrib.auth.models import User,auth
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.decorators import login_required
import urllib
import json
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.contrib.auth.backends import ModelBackend
from mysite.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.db.models import Count

# class PostList(generic.ListView):
#     queryset = Post.objects.filter(status=1).order_by('-created_on')
#     template_name = 'index.html'

# class PostInfiniteRecent(generic.ListView):
#     queryset = Post.objects.filter(status=1).all()
#     paginate_by = 2
#     context_object_name = 'posts'
#     template_name = 'infinite.html'
#     ordering = ['-created_on']

def recent_post(request):
    top_posts = Post.objects.filter(status=1,).order_by('-views')
    recent_posts = Post.objects.filter(status=1,).order_by('-created_on')
    recom_posts = Post.objects.annotate(q_count=Count('like')) \
                                 .order_by('-q_count')
    n = len(top_posts)
    nslides = n
    params = {"no_of_slides":nslides,"range": range(1,nslides), "top_posts":top_posts,"recent_posts":recent_posts,"recom_posts":recom_posts}
    return render(request,'index.html', params)


@login_required(login_url='login')
def blog_form(request):
    post = None
    if request.method == 'POST':
        new_blog_form = BlogForm(data= request.POST, files=request.FILES)
        if new_blog_form.is_valid():
            
            post = new_blog_form.save(commit=False, )
            post.author = request.user
            post.save()


            for k in new_blog_form.cleaned_data['category']:
                selection = Category.objects.create(category = k)
                selection.save()
                post.category.add(selection)


        else:
            messages.info(request, 'Alert! Something Goes Wrong. Please try again ')

    else:
        new_blog_form = BlogForm()
    return render(request, 'blogform.html', {'new_blog_form': new_blog_form, 'post':post})


@login_required
def post_update(request, slug):
    instance = get_object_or_404(Post, slug=slug)
    if instance.author == request.user:
        new_blog_form = EditForm(request.POST or None, request.FILES or None, instance=instance)

        if request.method == 'POST':
        
            if new_blog_form.is_valid():
                instance = new_blog_form.save(commit=False)
                instance.save()

                messages.success(request, "Blog Updated")
                return HttpResponseRedirect(instance.get_absolute_url())
    else:
        raise PermissionDenied 
        return redirect("blog:home")


    return render(request, "blogform.html", {"instance": instance,"new_blog_form":new_blog_form})

@login_required
def post_delete(request,  slug):

    instance = get_object_or_404(Post, slug=slug)
    
    if instance.author == request.user:

        instance.delete() 
        messages.success(request, "Successfully Deleted")
        return redirect("blog:home")
    else:
        raise PermissionDenied 
        return redirect("blog:home")

    return redirect("blog:home")

def post_detail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    post.views = post.views + 1
    post.save()
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            ''' End reCAPTCHA validation '''

            if result['success']:
                # Create Comment object but don't save to database yet
                new_comment = comment_form.save(commit=False)
                # Assign the current post to the comment
                new_comment.post = post
                # Save the comment to the database
                new_comment.save()
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
    else:
        comment_form = CommentForm()    

    return render(request, template_name, {'post': post,
                                        'comments': comments,
                                        'new_comment': new_comment,
                                        'comment_form': comment_form})



class PostLikeToggle(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        obj = get_object_or_404(Post, slug=slug)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.like.all():
                obj.like.remove(user)
            else:
                obj.like.add(user)
        return url_ 

class PostLikeAPIToggle(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


    def get(self, request, slug=None, format=None):
        # slug = self.kwargs.get("slug")
        obj = get_object_or_404(Post, slug=slug)
        url_ = obj.get_absolute_url()
        user = self.request.user
        updated = False
        liked = False
        if user.is_authenticated:
            if user in obj.like.all():
                liked = False
                obj.like.remove(user)
            else:
                liked = True
                obj.like.add(user)
            updated = True
        data = {
            "updated": updated,
            "liked": liked
        }
        return Response(data)

def post_view(request, slug):

    post = get_object_or_404(Post, slug=slug)

    if not PostView.objects.filter(
                    post=post,
                    session=request.session.session_key):
        view = PostView(post=post,
                            ip=request.META['REMOTE_ADDR'],
                            created=datetime.datetime.now(),
                            session=request.session.session_key)
        view.save()
    views_count = PostView.objects.filter(post=post).values("ip").distinct().count()
    return render(request, 'post_detail.html', {"views_count":views_count, "view":view})

def contact_us(request):
    print("coming")
    contact_us_obj = None
    if request.method == 'POST':
        contact_us_form = ContactUsForm(data= request.POST)
        if contact_us_form.is_valid():
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            ''' End reCAPTCHA validation '''

            if result['success']:
                contact_us_obj = contact_us_form.save()
                contact_us_obj.save()
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
        else:
            messages.info(request, 'Alert! Over exceeded word limits ')
            print (new_blog_form.errors)
            # return HttpResponse('You can only select 4 fields in Category')

    else:
        contact_us_form = ContactUsForm()
    return render(request, 'contact_us.html', {'contact_us_form': contact_us_form, 'contact_us_obj':contact_us_obj})

def about_us(request):
    return render(request, 'aboutus.html')

def search(request):
    if request.method == 'GET':
        query = request.GET['query']

        if len(query) > 100:
            queryset= Post.objects.none()
            
        if len(query)== 0:
            return redirect("blog:home")

        else:
            lookups= Q(title__icontains=query) | Q(content__icontains=query) | Q(location__icontains=query) | Q(state__icontains=query) | Q(author__username__icontains=query) | Q(category__category__icontains=query)
            queryset = Post.objects.filter(lookups).distinct()

        if queryset.count() == 0:
            messages.warning(request, 'No search results found, Please refine your query')
        return render(request, "search.html", {"queryset":queryset, 'query':query})
        
    else:
        messages.warning(request, 'Invalid request')


def signup_view(request):
    if request.method  == 'POST':
        form = SignUpForm(request.POST)
        email = request.POST['email']
        username = request.POST['username']
        if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists() :
            messages.error(request,"This Email/username is already registered")

        elif form.is_valid():
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            ''' End reCAPTCHA validation '''
            
            if result['success']:
                user = form.save()
                user.refresh_from_db()
                user.profile.first_name = form.cleaned_data.get('first_name')
                user.profile.last_name = form.cleaned_data.get('last_name')
                user.profile.email = form.cleaned_data.get('email')

                # user can't login until link confirmed
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                subject = 'Please Activate Your Account'
                # load a template like get_template() 
                # and calls its render() method immediately.
                message = render_to_string('registration/activation_request.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    # method will generate a hash value with user related data
                    'token': account_activation_token.make_token(user),
                })
                recepient = str(form['email'].value())
                # user.email_user(subject, message)
                send_mail(subject, 
            message, EMAIL_HOST_USER, [recepient], fail_silently = False)
                return redirect('blog:activation_sent')
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')


    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def activation_sent_view(request):
    return render(request, 'registration/activation_sent.html')



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true 
        user.is_active = True
        # set signup_confirmation true
        user.profile.signup_confirmation = True
        user.save()
        login(request, user)
        messages.success(request, 'Registration completed.')

        return redirect('blog:home')
    else:
        messages.error(request, 'Login not completed. please check your email')
        return render(request, 'blog:home')


def login_view(request):

    if request.method == 'POST':
        userinput = request.POST['username']
        try:
            username = User.objects.get(email=userinput).username
        except User.DoesNotExist:
            username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request,"Login successfull")
            return redirect('blog:home')
        else:

            messages.error(request,'Invalid credentials, Please check username/email or password. ')


    return render(request, "registration/login.html")


def logout_view(request):
    auth.logout(request)
    messages.success(request, "Logged out successfully!")
    return render(request,'registration/logout.html')
    


@login_required(login_url='login')
def userprofileposts(request, user_id):
    # profile = get_object_or_404(Profile, pk=id)
    user = request.user
    user_posts = Post.objects.filter(author = request.user).order_by('-created_on')
    template = 'registration/user_profile_posts.html'
    return render(request, template, {'user_posts':user_posts,'user': user,})


@login_required
@transaction.atomic
def update_profile(request, user_id):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Your profile was successfully updated!')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'registration/user_profile_update.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def get_user_profile(request, user_id):
    profile = Profile.objects.get(user_id= user_id)
    user = User.objects.get(id = user_id)
    posts = Post.objects.filter(author_id = user_id).order_by('-created_on')

    return render(request, 'registration/user_profile.html',{"user":user,"profile":profile,"posts":posts})

def get_category(request, category):
    query = category
    lookups= Q(category__category__icontains=query)

    posts = Post.objects.filter(lookups).distinct().order_by('-created_on')

    return render(request, 'get_category.html', {"posts":posts,'query':query})

  
def get_state(request, slug_st):
    query = slug_st
    posts = Post.objects.filter(slug_st=query).order_by('-created_on')

    return render(request, 'get_state.html', {"posts":posts,"query":query})

def get_location(request, slug_lc):
    query = slug_lc
    lookups = Q(location__icontains=query)
    posts_sr= Post.objects.filter(lookups).distinct().order_by('-created_on')

    return render(request, 'get_location.html', {"query":query,"posts_sr":posts_sr})

def explore(request):
    categories = Category.objects.values_list('category',flat=True).distinct()
    posts = Post.objects.filter(status=1).all().order_by('-updated_on')

    return render(request, 'infinite.html', {"categories":categories,"posts":posts})

def terms_view(request):
    return render(request, 'terms.html')

def privacy_view(request):
    return render(request, 'privacy.html')