from django.shortcuts import render,redirect
from django.urls import reverse
from .forms import RegisterForm,UserForm
from .models import User,Book,Word
from .Nlp.Nlp import load_model
from gensim.models import word2vec

# Create your views here.


def index(request):
    error = ''
    if request.method == 'POST':
        # 获取用户选择的分类
        key = request.POST['info']
    else:
        # 默认显示文章分类
        key = '热门推荐'
    if key == '热门推荐':
        data = Book.objects.filter(types__regex='英语美文')[0:6]
    else:
        data = Book.objects.filter(types__regex=key)
    return render(request, 'index.html', locals())


#登录界面，session判断是否已经登录，表单验证
def login(request):

    if request.session.get('is_login', None):
        return redirect(reverse('myauth:index'))

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(name=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name

                    return redirect(reverse('myauth:index'))
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
                return render(request, 'login.html', locals())

    login_form = UserForm()
    return render(request, 'login.html', locals())


#注册界面，表单验证，存入数据库，密码无加密
def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("myauth:index")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'register.html', locals())
            else:
                same_name_user = User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'register.html', locals())
                same_email_user = User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'register.html', locals())
                # 当一切都OK的情况下，创建新用户
                new_user = User()
                new_user.name = username
                new_user.password = password1
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect('myauth:slogin')  # 自动跳转到登录页面

    register_form = RegisterForm()
    return render(request, 'register.html', locals())

#退出界面
def logout(request):
    if not request.session.get("is_login" ,None):
        return redirect(reverse('myauth:index'))
    request.session.flush()
    return redirect(reverse("myauth:index"))


# 文章推荐
def recommd2(request):
    # 获取当前用户名
    user_name = request.session['user_name']
    # 获取当前用户生词表的单词
    user_word = Word.objects.filter(user_id=request.session['user_id']).values('word')

    #判断用户是否添加了生词
    if user_word:
        # 将data设置为真
        data = 1
        # 加载算法模型
        model = word2vec.Word2Vec.load('/Users/oukoto/Desktop/单词推荐算法/Engpro/myapp/Nlp/text8.model')
        # 判断该用户的最后一个单词是否能用算法运行成功
        try:
            last_word = list(user_word)[-1]['word']
            result = model.most_similar(last_word)
        # 否则设置一个默认值
        except:
            last_word = 'man'
            result = model.most_similar(last_word)
        # 返回相似列表中第一个单词
        result = result[0][0]
        # 从数据库中包含运算出来的相似单词的文章，
        similar_data = Book.objects.filter(content__icontains=result)

    else:
        data = ''
    return render(request, 'recommd2.html', locals())

# 文章详情
def details(request,id):
    # 从数据库中查询图书的id,传给页面
    book_data = Book.objects.filter(id=id)
    return render(request,'show_book.html',locals())


# 查询文章
def search(request):
    if request.method == 'POST':
        search_title = request.POST['book_search']
        data = Book.objects.filter(title__contains=search_title)
        if not data:
            data = ''
        return render(request, 'search.html', locals())


#生词表
def word(request):
    # 查询当前的用户id的生词表
    word_data = Word.objects.filter(user_id=request.session['user_id'])

    if request.method == 'POST':
        add_word = request.POST.get('add_word')
        word_save = Word(user_id=request.session['user_id'],word=add_word)   #将用户id与添加的单词保存
        word_save.save()

    return render(request,'word.html',locals())


