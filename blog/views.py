from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Posts, Tag, Comment
from .forms import PostsForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .utils import searchProjects, paginateProjects
from .forms import CommentForm


def posts(request):
    posts, search_query = searchProjects(request)
    custom_range, posts = paginateProjects(request, posts, 6)

    context = {'posts' : posts, 'search_query' : search_query, 'custom_range' : custom_range }
    return render(request, 'posts/posts.html', context)

def post(request, pk ):
    PostObj = Posts.objects.get(id=pk)
    comments = PostObj.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = PostObj
            # Save the comment to the database
            new_comment.save()
            return redirect(PostObj.get_absolute_url()+'#'+str(new_comment.id))
    else:
        comment_form = CommentForm()
    return render(request, 'posts/single-post.html', {'post' : PostObj,'comments': comments,'comment_form':comment_form})

@login_required(login_url="login")
def createPost(request):
    form = PostsForm
    profile = request.user.profile
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', " ").split()
        form = PostsForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')
    context = {'form' : form}
    return render(request, "projects/project_form.html", context)

@login_required(login_url="login")
def updatePost(request, pk):
    profile = request.user.profile
    project = profile.posts_set.get(id=pk)
    form = PostsForm(instance=project)
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', " ").split()
        form = PostsForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')
    context = {'form' : form}
    return render(request, "projects/project_form.html", context)

@login_required(login_url="login")
def deletePost(request, pk):
    profile = request.user.profile
    project = profile.posts_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('account')
    context = {'object' : project}
    return render(request, 'delete_template.html', context) 


def reply_page(request):
    if request.method == "POST":

        form = CommentForm(request.POST)
        
        # print(form)

        if form.is_valid():
            post_id = request.POST.get('post_id')  # from hidden input
            parent_id = request.POST.get('parent')  # from hidden input
            post_url = request.POST.get('post_url')  # from hidden input

            print(post_id)
            print(parent_id)
            print(post_url)


            reply = form.save(commit=False)
    
            reply.post = Posts(id=post_id)
            reply.parent = Comment(id=parent_id)
            reply.save()

            return redirect(post_url+'#'+str(reply.id))

    return redirect("/")