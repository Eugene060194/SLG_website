from django.shortcuts import render, redirect
from .forms import GeneratorForm, RegistrationUserForm, LoginUserForm
from ._generator import CompleteText
from .utils import generate_number, read_saved_text, save_text
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator

# Хранит идентификаторы сгенерированных текстов для зарегистрированных пользователей
new_texts_id = {}


def index(request):  # /
    return render(request, 'index.html')


def authorization(request):  # /auth
    if request.user.is_authenticated:
        return redirect('index')
    context = {}
    if request.method == 'POST':
        form = LoginUserForm(request=request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('mytexts')
    else:
        form = LoginUserForm()
    context['form'] = form
    return render(request, 'authorization.html', context=context)


def logout_user(request):  # /logout
    logout(request)
    return redirect('authorization')


def registration(request):  # /reg
    if request.user.is_authenticated:
        return redirect('index')
    context = {}
    if request.method == 'POST':
        form = RegistrationUserForm(request.POST)
        if form.is_valid():
            form.save()
            context['res'] = 'Регистрация прошла успешно!'
    else:
        form = RegistrationUserForm()
    context['form'] = form
    return render(request, 'registration.html', context=context)


def examples(request):  # /textexamples
    context = {'examples': True}
    all_texts = read_saved_text('main/exampletexts')
    paginator = Paginator(all_texts, 1)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    context['texts'] = page_object
    return render(request, 'savedtexts.html', context=context)


def my_texts(request):  # /mytexts
    if not request.user.is_authenticated:
        return redirect('index')
    user_directory = User.objects.get(username=request.user.username).usertext.directory
    my_all_texts = read_saved_text(user_directory)
    paginator = Paginator(my_all_texts, 1)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return render(request, 'savedtexts.html', {'texts': page_object})


def generator(request):  # /generator
    context = {}
    if request.method == 'POST':
        sov = int(request.POST.get('size_of_verse'))
        av = int(request.POST.get('amount_verse'))
        apis = int(request.POST.get('amount_phrase_in_string'))
        soc = int(request.POST.get('size_of_chorus'))
        awis = int(request.POST.get('amount_words_in_string'))
        rt = request.POST.get('rhyme_type')
        new_text = CompleteText(sov, av, apis, soc, awis, rt).output()
        if request.user.is_authenticated:
            new_text_id = generate_number()
            new_texts_id[new_text_id] = new_text
            return redirect('/newtext/{}'.format(new_text_id))
        else:
            context['new_text'] = new_text
            return render(request, 'generator_newtext.html', context=context)
    else:
        form = GeneratorForm()
        context['form'] = form
        return render(request, 'generator.html', context=context)


def generator_new_text(request, number):  # /generator/{id текста из словаря "new_texts_id"}
    context = {}
    new_text = new_texts_id[number]
    context['new_text'] = new_text
    if request.method == 'POST':
        save_text(request.user.username, number, new_text)
        new_texts_id.pop(number)
        context['res'] = 'Текст сохранён!'
    return render(request, 'generator_newtext.html', context=context)
