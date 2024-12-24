from django.shortcuts import render
from weblogapp.models import Post,Comments
from weblogapp.forms import CommentForm,SubscribeForm
from django.http import HttpResponseRedirect
from django.urls import reverse



# Create your views here.


def index(request):
    posts = Post.objects.all()
    top_posts = Post.objects.all().order_by('-view_count')[0:3]
    recent_post = Post.objects.all().order_by('-last_update')[0:3]
    # used for render the subscrie form 
    featured_blog = Post.objects.filter(is_featured=True)
    subscribe_form = SubscribeForm()
    subscribe_successfull = None

    if featured_blog:
        featured_blog = featured_blog[0]
        

    if request.POST:
       subscribe_form=SubscribeForm(request.POST)
       if subscribe_form.is_valid():
           subscribe_form.save()
           subscribe_successfull = "Subscribed Successfull"
           subscribe_form = SubscribeForm()


    context ={
        'posts':posts,
        'top_posts':top_posts,
        'recent_post':recent_post,
        'subscribe_form':subscribe_form,
        'subscribe_successfull':subscribe_successfull,
        'featured_blog':featured_blog,
    }
    return render(request,'weblogapp/index.html',context)



def post_page(request,slug):
    post = Post.objects.get(slug=slug)
    # used for increment the views funcionality in the post 
    comments = Comments.objects.filter(post=post,parent=None)
    form = CommentForm()

    if request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            parent_obj = None
            if request.POST.get('parent'):
                # Save the reply
                parent = request.POST.get('parent')
                parent_obj = Comments.objects.get(id=parent)
                if parent_obj:
                    comment_reply = comment_form.save(commit=False)
                    comment_reply.parent = parent_obj  # Set the parent comment
                    comment_reply.post = post         # Associate with the current post
                    comment_reply.save()
                    return HttpResponseRedirect(reverse('post_page', kwargs={'slug': slug}))
            else:
                # Save as a new comment (not a reply)
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.save()
                return HttpResponseRedirect(reverse('post_page', kwargs={'slug': slug}))
            



    if post.view_count is None:
        post.view_count =1
    else:
        post.view_count = post.view_count+1
        post.save()

    context ={
        'post':post,
        'form':form,
        'comments':comments,
        }
    
    return render(request,'weblogapp/post.html',context)


