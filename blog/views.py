from django.shortcuts import render, get_object_or_404, redirect
from .models import Post,Comment,ContactUs,Profile
from .forms import CommentForm,BlogForm,ContactUsForm,SignUpForm
from django.views import generic
from django.http import HttpResponse
from django.contrib import messages
from django.views.generic.list import ListView
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
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


# class PostList(generic.ListView):
#     queryset = Post.objects.filter(status=1).order_by('-created_on')
#     template_name = 'index.html'

class PostInfiniteRecent(generic.ListView):
    queryset = Post.objects.filter(status=1).all()
    paginate_by = 2
    context_object_name = 'posts'
    template_name = 'infinite.html'
    ordering = ['-created_on']

def recent_post(request):
    recent_posts = Post.objects.filter(status=1).all()
    n = len(recent_posts)
    nslides = n
    params = {"no_of_slides":nslides,"range": range(1,nslides),"recent":recent_posts}
    return render(request,'index.html', params)


def blog_form(request):
    print("coming")
    form_obj = None
    if request.method == 'POST':
        new_blog_form = BlogForm(data= request.POST, files=request.FILES)
        if new_blog_form.is_valid():
            form_obj = new_blog_form.save(commit=False, )
            form_obj.save()
            print("submitted")
        else:
            messages.info(request, 'Alert! You can only a select maximum of 4 fields in Category ')
            print (new_blog_form.errors)
            # return HttpResponse('You can only select 4 fields in Category')

    else:
        new_blog_form = BlogForm()
    return render(request, 'blogform.html', {'new_blog_form': new_blog_form, 'form_obj':form_obj})


def about_us(request):
    return render(request, 'aboutus.html')


def post_detail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                        'comments': comments,
                                        'new_comment': new_comment,
                                        'comment_form': comment_form})


def contact_us(request):
    print("coming")
    contact_us_obj = None
    if request.method == 'POST':
        contact_us_form = ContactUsForm(data= request.POST)
        if contact_us_form.is_valid():
            contact_us_obj = contact_us_form.save()
            contact_us_obj.save()
            print("submitted")
        else:
            messages.info(request, 'Alert! Over exceed word limits ')
            print (new_blog_form.errors)
            # return HttpResponse('You can only select 4 fields in Category')

    else:
        contact_us_form = ContactUsForm()
    return render(request, 'contact_us.html', {'contact_us_form': contact_us_form, 'contact_us_obj':contact_us_obj})

def search(request):
    if request.method == 'GET':
        query = request.GET['query']

        if len(query) > 100:
            queryset= Post.objects.none()
            
        if len(query)== 0:
            return redirect("home")

        else:
            lookups= Q(title__icontains=query) | Q(content__icontains=query) | Q(location__icontains=query) | Q(state_choice__icontains=query) | Q(author__icontains=query) | Q(email__icontains=query) | Q(category__icontains=query)
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
        if User.objects.filter(email=email).exists() :
            messages.error(request,"This Email is already registered")
            print("email")
            # return redirect('signup')

        elif form.is_valid():
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
            user.email_user(subject, message)
            return redirect('activation_sent')


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
        messages.success(request, 'Registration completed. Please login now')

        return redirect('home')
    else:
        messages.error(request, 'Login not completed. please check your email')
        return render(request, 'home')


def login_view(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                messages.success(request,"Login successfull")
                return redirect('home')
            else:

                messages.warning(request,'invalid credentials')
        else:


            return render(request, "registration/login.html")



def logout_view(request):

    auth.logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect(request,'registration/logout.html')
    