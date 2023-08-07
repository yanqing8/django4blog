from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Article
from .forms import ArticleForm
from comment.models import Comment


# Create your views here.

# render函数参数和语法如下：
# render(request, template_name, context=None, content_type=None, status=None, using=None)
# 一般情况下我们只需要用到前两个参数 template_name（定义了模板文件的位置、名称）, context（定义了需要传入模板文件的上下文），其他的参数使用默认值就可以了。
# 简单说明下render函数的几个参数：
# request: 浏览器向服务器发送的请求对象，包含用户信息、请求内容和请求方式等（不用改，）。
# template_name: 要使用的模板的文件名, 可选的参数
# context: 添加到模板上下文的一个字典. 默认是一个空字典. 如果字典中的某个值是可调用的, 视图将在渲染模板之前调用它.
# content_type: 生成的文档要使用的MIME类型. 默认为DEFAULT_CONTENT_TYPE设置的值. 默认为"text/html"
# status: 响应的状态码. 默认为200
# using: 用于加载模板的模板引擎的名称

def hello(request):
    return HttpResponse("Hello world! ")


# 更新文章
def article_update(request, id):
    """
    更新文章的视图函数
    通过POST方法提交表单，更新title、body字段
    GET方法进入初始表单页面
    id： 文章的 id
    """
    # 获取需要修改的具体文章对象
    article = Article.objects.get(id=id)
    # 判断用户是否为 POST 提交表单数据
    if request.method == 'POST':
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticleForm(data=request.POST)
        if article_post_form.is_valid():
            # 保存新写进来的 title、body 数据
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("detail", id=id)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果是GET请求，获取数据
    else:
        # 创建表单实例
        article_post_form = ArticleForm()
        context = {'article': article, 'article_post_form': article_post_form}
        # 返回模板
        return render(request, 'article/update.html', context)


# 删文章
def article_delete(request, id):
    if request.method == 'POST':
        # 根据 id 获取需要删除的文章
        article = Article.objects.get(id=id)
        # 调用.delete()方法删除文章
        article.delete()
        return redirect("list")
    else:
        return HttpResponse("仅允许post请求")


# 写文章的视图
def article_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticleForm(data=request.POST)
        # 判断提交的数据是否满足模型要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            # 作者为当前请求的用户名
            new_article.author = request.user
            # 将文章保存到数据库中
            new_article.save()
            # 完成后返回到文章列表
            return redirect('list')
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        article_post_form = ArticleForm()
        context = {'article_post_form': article_post_form}
        # 返回模板
        return render(request, 'article/create.html', context)


# 文章列表
def article_list(request):
    # 取出所有博客文章
    # articles = Article.objects.all()
    # articles_list = Article.objects.all()
    # 根据GET请求中查询条件
    # 返回不同排序的对象数组
    search = request.GET.get('search')
    order = request.GET.get('order')
    if search:
        if order == 'total_views':
            # 用 Q对象 进行联合搜索
            articles_list = Article.objects.filter(Q(title__icontains=search) | Q(body__icontains=search)).order_by('-total_views')
        else:
            articles_list = Article.objects.filter(Q(title__icontains=search) | Q(body__icontains=search))
    else:
        # 将 search 参数重置为空
        search = ''
        if order == 'total_views':
            articles_list = Article.objects.all().order_by('-total_views')
        else:
            articles_list = Article.objects.all()

    # 每页显示 3 篇文章
    paginator = Paginator(articles_list, 3)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给articles
    articles = paginator.get_page(page)

    # 需要传递给模板（templates）的对象
    context = {'articles': articles, 'order': order, 'search': search}
    # render函数：载入模板，并返回context对象
    return render(request, 'article/list.html', context)


# 文章详情
def article_detail(request, id):
    # 取出相应的文章
    article = Article.objects.get(id=id)
    # 浏览量 +1
    article.total_views += 1
    article.save(update_fields=['total_views'])
    # 取出文章评论
    comments = Comment.objects.filter(article=id)
    # 需要传递给模板的对象
    context = {'article': article, 'comments': comments}
    # 载入模板，并返回context对象
    return render(request, 'article/detail.html', context)
