from django.shortcuts import render, get_object_or_404
from .models import Post,Comment,ContactUs
from .forms import CommentForm,BlogForm,ContactUsForm
from django.views import generic
from django.http import HttpResponse
from django.contrib import messages
from django.views.generic.list import ListView
from math import ceil
from django.db.models import Q

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
            
        else:
            lookups= Q(title__icontains=query) | Q(content__icontains=query) | Q(location__icontains=query) | Q(state_choice__icontains=query) | Q(author__icontains=query) | Q(email__icontains=query) | Q(category__icontains=query)
            queryset = Post.objects.filter(lookups).distinct()

        if queryset.count() ==0:
            messages.warning(request, 'No search results found, Please refine your query')
        
        return render(request, "search.html", {"queryset":queryset, 'query':query})
            
            

    else:
        messages.info(request, 'Alert!')

