from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpResponse, Http404

from django.contrib.auth.decorators import login_required
from django.db import transaction

from django.contrib.auth import login, authenticate

# Used to send mail from within Django
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator

from mimetypes import guess_type

from grumblr.forms import *
from grumblr.models import *
from django.utils import timezone
from django.contrib.auth.models import User


@login_required
def home(request):
    context = {}

    posts = Post.objects.all().order_by('-time')
    context['posts'] = posts

    if request.method == 'GET':
        context['form'] = PostForm()
        context['commentForm'] = CommentForm()
        return render(request, 'globalStream.html', context)

    form = PostForm(request.POST)
    context['form'] = form
    context['commentForm'] = CommentForm()

    if not form.is_valid():
        return render(request, 'globalStream.html', context)


@login_required
@transaction.atomic
def add_comment(request, id):
    errors = []
    context = {}

    if not 'post' in request.POST or not request.POST['post']:
        errors.append('Comment can not be empty.')
    elif len(request.POST['post']) > 42:
        errors.append('no more than 42 words.')
    else:
        new_comment = Comment(post=Post.objects.get(id=id),
                              text=request.POST['post'],
                              user=request.user,
                              time=timezone.now())
        new_comment.save()

    context['commentForm'] = CommentForm()
    context['form'] = PostForm()
    comments = Comment.objects.all().order_by('-time')
    context['comments'] = comments
    context['errors'] = errors
    return HttpResponse("")


@login_required
@transaction.atomic
def add_post(request):
    errors = []
    context = {}

    if not 'post' in request.POST or not request.POST['post']:
        errors.append('Hey, you have to write something...')
    elif len(request.POST['post']) > 42:
        errors.append('Do not write too many words...')
    else:
        new_post = Post(text=request.POST['post'], user=request.user, time=timezone.now())
        new_post.save()

    context['commentForm'] = CommentForm()
    context['form'] = PostForm()
    posts = Post.objects.all().order_by('-time')
    context['posts'] = posts
    context['errors'] = errors
    return render(request, 'globalStream.html', context)


@login_required
@transaction.atomic
def profile(request, id):
    context = {}
    try:
        current_user = User.objects.get(id=id)
        posts = Post.objects.filter(user=current_user).order_by('-time')
        profile = Profile.objects.get(user=current_user)
        if current_user != request.user:
            if current_user not in request.user.profile.follower.all():
                context['follow'] = 'follow'
            else:
                context['unfollow'] = 'unfollow'
        context['commentForm'] = CommentForm()
        context['current_user'] = current_user
        context['profile'] = profile
        return render(request, 'profile.html', context)
    except ObjectDoesNotExist:
        return home(request)


@login_required
def relationship(request, id):
    context = {}
    wanted_posts = list()
    for post in Post.objects.all().order_by('-time'):
        if post.user in request.user.profile.follower.all():
            # show post in order
            wanted_posts.append(post)
            context['posts'] = wanted_posts
            context['commentForm'] = CommentForm()
    return render(request, 'follower-stream.html', context)


@login_required
def edit_relationship(request, id):
    if User.objects.get(id=id) not in request.user.profile.follower.all():
        request.user.profile.follower.add(User.objects.get(id=id))
        return profile(request, id)
    else:
        request.user.profile.follower.remove(User.objects.get(id=id))
        return profile(request, id)


@login_required
@transaction.atomic
def edit_profile(request, id):
    # profile_to_edit = get_object_or_404(Profile, user=request.user)

    if request.method == 'GET':
        form = ProfileForm(instance=request.user.profile)
        context = {'form': form, 'id': id}
        return render(request, 'edit-profile.html', context)

    # if method is POST, get form data to update the model
    form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

    if not form.is_valid():
        context = {'form': form, 'id': id}
        return render(request, 'edit-profile.html', context)

    form.save()
    current_user = User.objects.get(id=id)
    current_user.set_password(form.cleaned_data['password'])
    current_user.email = form.cleaned_data['email']
    current_user.save()

    current_user = authenticate(username=request.user.username,
                                email=form.cleaned_data['email'],
                                password=form.cleaned_data['password'])

    login(request, current_user)

    return redirect(reverse('profile', args=[id]))


@login_required
def get_photo(request, id):
    profile = get_object_or_404(Profile, id=id)
    if not profile.picture:
        raise Http404

    content_type = guess_type(profile.picture.name)
    return HttpResponse(profile.picture, content_type=content_type)


@transaction.atomic
def register(request):
    context = {}

    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'registration.html', context)

    form = RegistrationForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'registration.html', context)

    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'],
                                        email=form.cleaned_data['email1'],
                                        password=form.cleaned_data['password1'])
    new_user.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            first_name=form.cleaned_data['first_name'],
                            last_name=form.cleaned_data['last_name'],
                            email=form.cleaned_data['email1'],
                            password=form.cleaned_data['password1'])

    new_user.profile.first_name = form.cleaned_data['first_name']
    new_user.profile.last_name = form.cleaned_data['last_name']
    new_user.profile.email = form.cleaned_data['email1']
    new_user.profile.password = form.cleaned_data['password1']

    login(request, new_user)

    return redirect('/grumblr/')


@transaction.atomic
def password(request):
    errors = []
    context = {}

    if request.method == 'GET':
        context['form'] = EmailForm()
        return render(request, 'forget-password.html', context)

    form = EmailForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'forget-password.html', context)

    try:
        user = User.objects.get(email=form.cleaned_data['email'])
        token = default_token_generator.make_token(user)
        email_body = """
    Welcome to the Grumblr. Please click the link below to verify your email address and complete the registration of your account:

    http://%s%s
    """ % (request.get_host(), "/grumblr/confirm/" + user.username + "/" + token)

        send_mail(subject="Verify your email address",
                  message=email_body,
                  from_email="yyi1@andrew.cmu.edu",
                  recipient_list=[user.email])
        context['email'] = form.cleaned_data['email']
        return render(request, 'forget-password.html', context)
    except ObjectDoesNotExist:
        errors.append("We couldn't find your account with that information")
        context['errors'] = errors
        return render(request, 'forget-password.html', context)


@transaction.atomic
def confirm_registration(request, username, token):
    try:
        confirmed_user = User.objects.get(username=username)
        token2 = default_token_generator.make_token(confirmed_user)
        if token == token2:
            login(request, confirmed_user)
            return redirect('/grumblr/')
        else:
            return home(request)
    except ObjectDoesNotExist:
        return home(request)


@login_required
def get_json_post(request):
    return HttpResponse(serializers.serialize("json", Post.objects.all().order_by('-time')),
                        content_type='application/json')


@login_required
def get_json_comment(request):
    return HttpResponse(serializers.serialize("json", Comment.objects.all().order_by('-time')),
                        content_type='application/json')


@login_required
def get_post(request):
    posts = Post.objects.all().order_by('time')
    return render(request, 'posts.json', {'posts': posts}, content_type='application/json')


@login_required
def get_profile_post(request, id):
    posts = Post.objects.filter(user=User.objects.get(id=id)).order_by('time')
    return render(request, 'posts.json', {'posts': posts}, content_type='application/json')


@login_required
def get_follower_post(request, id):
    context = {}
    wanted_posts = list()
    for post in Post.objects.all().order_by('time'):
        if post.user in request.user.profile.follower.all():
            # show post in order
            wanted_posts.append(post)
            context['posts'] = wanted_posts
    return render(request, 'posts.json', context, content_type='application/json')
