from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import *
from .models import *
from user.models import Profile
from home.models import *


# Create your views here.

def index(request):
    about = About.objects.all()
    service = Service.objects.all()
    history = History.objects.all()
    team = Team.objects.all()
    context = {
        'title':'الصفحة الرئيسيّة',

        'about':about,
        'services':service,
        'history':history,
        'team':team,
    }
    return render(request, 'pages/index.html', context)
    # return render(request, 'another/test.html')



class Counter:
    count_ = 0

    def increment(self):
        self.count_ += 1
        return ''
        
    def initial(self):
        self.count_ = 0
        return ''

def main(request):
    posts = Post.objects.filter(status=True)
    postImages = PostImage.objects.all()
    userProfiles = Profile.objects.all()
    comments=Comment.objects.filter(status=True)
    count = Counter()

    postPagination = Paginator(posts, 5)
    page = request.GET.get('page1')
    try:
        posts = postPagination.page(page)
    except PageNotAnInteger:
        posts = postPagination.page(1)
    except EmptyPage:
        posts = postPagination.page(postPagination.num_page)

    if request.method == 'POST':
        formData = CommentForm(request.POST)
        if formData.is_valid():
            newComment = formData.save(commit=False)
            newComment.userID = request.user
            post = request.POST.get('postID')
            newComment.postID = Post.objects.get(id=post, status=True)
            newComment.save()
            formData = CommentForm()
            return redirect('main')
    else:
        formData = CommentForm()
    return render(request, 'pages/main.html', 
                {'title':'أخبارنا', 'posts':posts, 'images':postImages,
                 'page1':page, 'comments':comments, 'count':count,
                 'userProfiles':userProfiles, 'commentForm':formData})




def commentUpdate(request, id):
    currentCommentObj = get_object_or_404(Comment,id=id, status=True)
    if request.method == 'POST':
        commentObj = Comment.objects.get(id=id, userID=request.user.id)
        if commentObj.status:
            formData = CommentUpdateForm(request.POST)

            if formData.is_valid():
                newComment = formData.cleaned_data['comment']
                postID = Post.objects.get(id=commentObj.postID.id)
                currentComment = commentObj.comment
                if not currentComment == newComment:
                    comment = Comment.objects.get(id=id, status=True, userID=request.user.id)
                    comment.status = False
                    comment.save()

                    data = formData.save(commit=False)
                    # data.id = id
                    data.userID = request.user
                    data.postID = postID
                    data.comment = newComment
                    data.updated = True
                    # data.dateTime = datetime.now()
                    formData.save()
                    newComment = Comment.objects.get(comment=data.comment, status=True)
                    messages.success(request, 'تمّ تعديل التّعليق بنجاح.')
                    return redirect('commentUpdateForm', id=newComment.id)
        else:
            messages.warning(request, 'هذا التّعليق غير موجود، لقد تمّ تعديله أو حذفه.')
            return redirect(request.path)
    else:
        formData = CommentUpdateForm()
                

    return render(request, 'forms/commentUpdateForm.html',
             {'title':'تعديل تعليق', 'commentUpdateForm':CommentUpdateForm, 'currentComment':currentCommentObj.comment })







@login_required(login_url='loginForm')
def deleteComment(request, id, path):
    comment = Comment.objects.get(id=id, status=True, userID=request.user.id)
    comment.status = False
    comment.save()
    messages.success(request,'تمّ حذف التعليق بنجاح')
    if path == 'post':
        return redirect(path, id=id, title=path)
    return redirect(path)




@login_required(login_url='loginForm')
def post(request, id, title):

    
    userProfiles = Profile.objects.all()
    if title == 'profile' or title == 'main' or title == 'post':
        postID = Comment.objects.get(id=id).postID.id
        post = Post.objects.get(id=postID, status=True)
        comments = Comment.objects.filter(status=True, postID=postID)
        images = PostImage.objects.filter(postID=postID)

        commentPagination = Paginator(comments, 5)
        page = request.GET.get('page1')
        try:
            comments = commentPagination.page(page)
        except PageNotAnInteger:
            comments = commentPagination.page(1)
        except EmptyPage:
            comments = commentPagination.page(commentPagination.num_page)


        imagePagination = Paginator(images, 1)
        page = request.GET.get('page2')
        try:
            images = imagePagination.page(page)
        except PageNotAnInteger:
            images = imagePagination.page(1)
        except EmptyPage:
            images = imagePagination.page(imagePagination.num_page)



        if request.method == 'POST':
            formData = CommentForm(request.POST)
            if formData.is_valid():
                newComment = formData.save(commit=False)
                newComment.userID = request.user
                newComment.postID = Post.objects.get(id=postID, status=True)
                newComment.save()
                formData = CommentForm()
        else:
            formData = CommentForm()
        return render(request, 'pages/post.html',
                {'title':'منشور-'+str(post), 'post':post, 'images':images, 'comments':comments, 'userProfiles':userProfiles, 'commentForm':formData})

    else:

        comments = Comment.objects.filter(status=True, postID=id)
        images = PostImage.objects.filter(postID=id)
        pagination = Paginator(comments, 5)
        page = request.GET.get('page1')
        try:
            comments = pagination.page(page)
        except PageNotAnInteger:
            comments = pagination.page(1)
        except EmptyPage:
            comments = pagination.page(pagination.num_page)

        imagePagination = Paginator(images, 1)
        page = request.GET.get('page2')
        try:
            images = imagePagination.page(page)
        except PageNotAnInteger:
            images = imagePagination.page(1)
        except EmptyPage:
            images = imagePagination.page(imagePagination.num_page)

        if request.method == 'POST':
            formData = CommentForm(request.POST)
            if formData.is_valid():
                newComment = formData.save(commit=False)
                newComment.userID = request.user
                postID = request.POST.get('postID')
                newComment.postID = Post.objects.get(id=postID, status=True)
                newComment.save()
                formData = CommentForm()
        else:
            formData = CommentForm()
        post = Post.objects.get(id=id, status=True)
        return render(request, 'pages/post.html',
                {'title':'منشور-'+str(post), 'post':post, 'images':images, 'comments':comments, 'userProfiles':userProfiles, 'commentForm':formData})
        




