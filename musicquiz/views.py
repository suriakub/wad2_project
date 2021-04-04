from django.shortcuts import render, redirect
from musicquiz.forms import UserProfileForm
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from musicquiz.models import UserProfile, MusicCategory, Comment


def index(request):
    context_dict = {}
    return render(request, 'musicquiz/index.html', context=context_dict)


def about(request):
    context_dict = {}
    return render(request, 'musicquiz/about.html', context=context_dict)


def categories(request):
    context_dict = {'categories': MusicCategory.objects.all()}
    return render(request, 'musicquiz/categories.html', context=context_dict)


def show_category(request, category_slug):
    context_dict = {}

    try:
        category = MusicCategory.objects.get(slug=category_slug)
        comments = Comment.objects.filter(category=category)
        context_dict['category'] = category
        context_dict['comments'] = None

    except MusicCategory.DoesNotExist:
        context_dict['category'] = None
        context_dict['comments'] = None

    if request.is_ajax():
        template = 'musicquiz/components/comments.html'
        category = MusicCategory.objects.get(slug=category_slug)
        context_dict['comments'] = Comment.objects.filter(category=category)
    else:
        template = 'musicquiz/category.html'

    return render(request, template, context=context_dict)


def quiz(request):
    context_dict = {}
    return render(request, 'musicquiz/quiz.html', context=context_dict)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('logout'))


@login_required
def register_profile(request):
    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('musicquiz:index')
        else:
            print(form.errors)
    context_dict = {'form': form}
    return render(request, 'musicquiz/profile_registration.html', context_dict)


@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')

    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm({
        'picture': userprofile.picture
    })

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)

        if form.is_valid():
            form.save(commit=True)
            return redirect('musicquiz:profile', user.username)

        else:
            print(form.errors)

    return render(request, 'musicquiz/profile.html', {'userprofile': userprofile, 'selecteduser': user, 'form': form})


def error(request):
    context_dict = {}
    return render(request, 'musicquiz/error.html', context=context_dict)
