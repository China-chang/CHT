import markdown
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse, get_object_or_404

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect  # 从 django 的 http 模块引入 HttpResponse 函数
import json, math, datetime

from django.views import View

from django.utils import timezone

import logging

from django_comments.templatetags import comments

from comment.forms import CommentForm
from comment.models import Comment
from .models import *

from django.utils.decorators import method_decorator

from django import forms
from django.core.paginator import Paginator

"""
定义视图函数：
1.最少要有一个参数，用来接受请求对象
2.在函数最后必须要返回一个响应对象


"""

"""
客户端向服务器传递参数的途径：
1.提取url路径的特定部分：（get,post,put,delete）
2.查询字符串:(get)
3.请求体(表单,非表单)：(post,put)
4.请求头



"""


# 首页
# http://127.0.0.1:8000/sixi/index/
def index(request):
    # 中间省略业务逻辑处理代码

    return HttpResponse('hello')


def index2(request):
    # 中间省略业务逻辑处理代码

    return HttpResponse('world')


# 提取url路径中的数据
# /weather/shanghai/2020

def weather1(request, city, year):
    return HttpResponse('weather1')


# 获取url中的查询字符串数据
# request.GET  GET只是一个属性而已，和请求方式无关，得到一个QueryDict类型对象
# QueryDict get:只能取一键一址  getlist:获取一键多址，返回的是一个列表

def get_canshu(request):
    query_dict = request.GET
    a = query_dict.get('a')
    alist = query_dict.getlist('a')

    print(a)
    print(alist)

    print(request.META.get('CONTENT_TYPE'))
    return HttpResponse(get_canshu)


# 在Django中非get请求   请求都要进行CSRF认证

def get_data(request):
    query_dict = request.POST

    return HttpResponse('get_data')


# 获取请求体的非表单数据  json：1.列表；2.字典（{"":""}）
# bytes_data = request.body  bytes类型的字符串
# json_data_str = bytes_data.decode()
# data = json.loads(json_data_str)
# data = json.loads(request.body.decode())
# POST/get_json/
def get_json(request):
    json_dict = json.loads(request.body.decode())
    print(json_dict)
    return HttpResponse('get_json')


# 响应对象的基本使用
def response_test(request):
    # return HttpResponse(content='响应体',content_type='响应体类型',status='响应状态码')
    # return HttpResponse(content='hello', content_type='text/html', status=200)

    # data = {"name":"zs","age":18}
    data1 = [1, 2, 3, 4]
    data = {'alist': data1}
    response = JsonResponse(data)
    return response


# 重定向的使用

def redirect_test(request):
    print('重定向')
    # 如果重定向时前面路由不加/就是基于当前url拼接要生成定向的路径
    # return redirect('/index/')

    # return redirect(index)

    # 反向解析

    print(reverse('sixi:index'))
    return redirect('sixi:index')


# cookie读写操作
def cookie_test(request):
    response = HttpResponse('cookie_text')

    # 设置cookie
    # 响应对象.set_cookie(cookie键,value,max_age = None)  过期时间不指定默认为会话结束（关闭浏览器）就过期
    response.set_cookie('name', 'cht', max_age=3600)
    response.set_cookie('age', '21', max_age=3600)
    return response

    # 读取cookie数据
    name = request.COOKIES.get('name')
    print(name)
    return response


# session读写操作
def session_test(request):
    # 设置session
    # 下面这行代码会进行将session存储到redis，并且会生成一个sessionid
    # request.session['user_id'] = '1'

    # 读写session
    # 当读写session时，会先从cookie中获取到sessionid，通过sessionid获取到指定session记录，再通过指定key
    # 设置session的过期时间（默认时间为14天）   request.session.set_expiry(秒)

    # 如果cookie过期时间设置为None 过期时间为会话结束  如果设置为0 代表删除
    # 如果session过期时间设置为None 过期时间为14天  如果设置为0 代表过期时间为会话结束
    user_id = request.session.get('user_id')
    print(user_id)
    return HttpResponse('session_test')

    """类视图"""


def my_decorator(func1):
    def wrapper(request, *args, **kwargs):
        print('装饰器被调用了')
        print('本次请求的路径：%s' % request.path)
        return func1(request, *args, **kwargs)

    return wrapper


# @method_decorator(my_decorator,name='dispatch')  #装饰所有的
# @method_decorator(my_decorator, name='get')
class DemoView(View):

    # @method_decorator(my_decorator)
    def get(self, request):
        return HttpResponse('get请求')

    def post(self, request):
        return HttpResponse('post请求')

    def put(self, request):
        return HttpResponse('put请求')

    def delete(self, request):
        return HttpResponse('delete请求')


class TempView(View):

    def get(self, request):
        # 执行输入context=data,
        data = {
            'name': 'cht',
            'alist': [1, 2, 3, 4],
            'adict': {'age': 21, 'sex': 1},
            'a': 10,
            'ahtml': '<h1>大标题<h1>',
            'nowdate': timezone.now(),
        }
        username = request.session['login']

        return render(request, 'ltbase.html', {'username': username})


#

class TempView2(View):
    def get(self, request):
        return render(request, 'base1.html')


class TempView3(View):
    def get(self, request):
        return render(request, 'children.html')


# 处理注册功能
def login(request):
    # 根据不同的请求方式处理不同的需求
    if request.method == 'GET':
        # 判断客户端是否存在login对应的cookie信息
        if 'login' in request.COOKIES:
            login = request.COOKIES.get('login', '').split(',')
            # 为cookie加密的写法
            # login = request.get_signed_cookie('login',salt='chtalwj').split(',')
            username = login[0]
            password = login[1]
            return render(request, 'register.html', {'username': username, 'password': password})

        return render(request, 'register.html')
    else:
        if 'zc' in request.POST:
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')

            # 判断是否非空
            if username and password:
                user = UserInfo(username=username, password=password)
                # 插入数据库
                user.save()

                return redirect('/login/')

            return redirect('/login/')
        else:
            username = request.POST.get('username')
            password = request.POST.get('password')

            # 查询数据库
            if username and password:
                # 判断是否非空
                c = UserInfo.objects.filter(username=username, password=password).count()
                response = HttpResponse()
                if c == 1:
                    # 设置cookie
                    response = redirect('/zhanshi/')
                    response.set_cookie('login', username + ',' + password, path='/login/', max_age=24 * 60 * 60 * 7)

                    # 设置cookie
                    request.session['login'] = json.dumps(username)
                    # cookie的加密写法
                    # response.set_signed_cookie('login', username + ',' + password, path='/login/', max_age=24 * 60 * 60 * 7)
                    return response
                response.delete_cookie('login', path='/login/')

                return redirect('/login/')
        # 获取请求参数


# 发帖功能
def ft(request):
    if request.method == 'GET':
        return render(request, 'discuss.html')

    else:
        title = request.POST.get('title', '')
        desc = request.POST.get('desc', '')
        content = request.POST.get('content', '')
        category = request.POST.get('category', '')
        # 判断是否非空
        if title and desc and content and category:
            post = Post(title=title, desc=desc, content=content, cname=category)
            # 插入数据库
            post.save()

        return render(request, 'discuss.html')


# 展示主页面
def look(request, num=1):
    num = int(num)

    # 获取所有帖子信息
    postList = Post.objects.all().order_by('-created')

    # 创建分页器对象
    PageObject = Paginator(postList, 1)

    # 获取当前页的数据
    perPageList = PageObject.page(num)

    # 生成页码数列表
    # 每页开始页码
    begin = (num - int(math.ceil(10.0 / 2)))
    if begin < 1:
        begin = 1

    # 每页结束页码
    end = begin + 9
    if end > PageObject.num_pages:
        end = PageObject.num_pages

    if end <= 10:
        begin = 1
    else:
        begin = end - 9

    pageList = range(begin, end + 1)

    return render(request, 'index.html', {'postList': perPageList, 'pageList': pageList, 'currentNum': num})


# 展示主页面
def zhanshi(request, num=1):
    num = int(num)

    # 获取所有帖子信息
    postList = Post.objects.all().order_by('-created')

    # 创建分页器对象
    PageObject = Paginator(postList, 3)

    # 获取当前页的数据
    perPageList = PageObject.page(num)

    # 生成页码数列表
    # 每页开始页码
    begin = (num - int(math.ceil(10.0 / 2)))
    if begin < 1:
        begin = 1

    # 每页结束页码
    end = begin + 9
    if end > PageObject.num_pages:
        end = PageObject.num_pages

    if end <= 10:
        begin = 1
    else:
        begin = end - 9

    pageList = range(begin, end + 1)
    username = request.session['login']
    return render(request, 'main-page.html',
                  {'postList': perPageList, 'pageList': pageList, 'currentNum': num, 'username': username})


# 阅读全文功能
def detail(request, postid):
    postid = int(postid)

    # 根据postid查询帖子的详情信息
    post = Post.objects.get(id=postid)

    # Markdown 语法渲染
    md = markdown.Markdown(
        extensions=[
            # 包含 缩写、表格等常用扩展
             
            'markdown.extensions.extra',
            # 语法高亮扩展
            'markdown.extensions.codehilite',
            # 目录扩展
            'markdown.extensions.toc',
        ]
    )
    post.content = md.convert(post.content)
    # 显示评论
    username = request.session['login']
    # 取出文章评论
    comments = Comment.objects.filter(post=id)
    # 为评论引入表单
    comment_form = CommentForm()

    # 需要传递给模板的对象
    context = {
        'post': post,
        'toc': md.toc,
        'comments': comments,
        # 'pre_article': pre_article,
        # 'next_article': next_article,
        'comment_form': comment_form,
    }
    # 载入模板，并返回context对象
    # return render(request, 'post/main-body.html', context)
    return render(request, 'main-body.html', {'post': post, 'username': username,'context':context})



#
# from django.shortcuts import render
# from .models import Page
# def tree(request):
#     nodes = Page.objects.all()
#     return render(request,'tree.html', {'nodes': nodes})
#

#
# def format_comments(comment_list):
#     """
#     把相关评论的列表集合转换成如下的格式 方便在build_comments_tree里构造HTML
#     也可以在后端把构造好的列表传递给前端 用js来构造HTML
#     [
#         {
#             'id':comment_id,
#             'content':'具体评论内容',
#             'user':'评论人',
#             'parent_id':id/None,
#             'children':[
#                 {},
#                 {},
#                 ...
#             ]
#         },
#         ...
#     }
#     """
#     formated_list = []
#     tmp_list = []
#     for comment in comment_list:
#         cid = comment['id']
#         pid = comment.get('parent_id')
#         dic = {'id': cid, 'user': comment['user'], 'content': comment['content'], 'parent_id': pid, 'children': []}
#         tmp_list.append(dic)
#         if not pid:
#             formated_list.append(dic)
#         else:
#             for item in tmp_list:
#                 if item['id'] == pid:
#                     item['children'].append(dic)
#                     break
#     return formated_list
#
#
# def build_comments_tree(formated_list):
#     tpl = """
#         <div class="item">
#             <div class="comment">{0}:{1}<a href="" class="reply">回复</a></div>
#             <div class="body">{2}</div>
#         </div>
#         """
#     html = ""
#     """深度优先搜索：递归遍历所有子评论"""
#     for item in formated_list:
#         children = item.get('children')
#         if children:
#             html += tpl.format(item['user'], item['content'], build_comments_tree(children))
#         else:
#             html += tpl.format(item['user'], item['content'], "")
#     return html
#
#
# def comment_tree(request):
#     comment_list = [
#         {'id': 1, 'user': 'alex', 'content': '一级评论', 'parent_id': None},
#         {'id': 2, 'user': 'alex', 'content': '管我鸟事', 'parent_id': None},
#         {'id': 3, 'user': 'eric', 'content': '你个文盲', 'parent_id': None},
#         {'id': 4, 'user': 'egon', 'content': '好羡慕你们这些没脸的人呀', 'parent_id': None},
#         {'id': 5, 'user': 'alex', 'content': '你是流氓', 'parent_id': 3},
#         {'id': 6, 'user': 'alvin', 'content': '双击666', 'parent_id': 5},
#         {'id': 7, 'user': 'alex', 'content': '智障啊 ->_->', 'parent_id': 6},
#         {'id': 8, 'user': 'alex', 'content': '你冷酷无情', 'parent_id': 4},
#         {'id': 9, 'user': 'eric', 'content': '你无理取闹', 'parent_id': 4},
#         {'id': 10, 'user': 'standby', 'content': '赶紧买个瓜围观', 'parent_id': 8},
#         {'id': 11, 'user': 'cindy', 'content': '前排卖水了啊', 'parent_id': 10},
#         {'id': 12, 'user': 'egon', 'content': '一群土老帽...', 'parent_id': None},
#     ]
#


    # comment_list = Comment.objects.all()
    # print(comment_list)




# from django.views.generic import ListView, DetailView
#
# from .models import MPTTComment
# from .models import Post
#
#
# class IndexView(ListView):
#     model = Post
#     template_name = 'index1.html'
#
#
# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'detail1.html'

# def index_view(request):
#     if request.method == 'GET':
#         return render(request, 'form.html')
#     else:
#         if 'zc' in request.POST:
#             username = request.POST.get('username','')
#             password = request.POST.get('password','')
#
#             if username and password:
#                 user = UserInfo(username = username,password = password)
#                 user.save()
#                 return HttpResponse('注册成功')
#             return HttpResponse('注册失败')
#         else:
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#
#             # 查询数据库
#             if username and password:
#                 # 判断是否非空
#                 c = UserInfo.objects.filter(username=username, password=password).count()
#                 if c == 1:
#                     return HttpResponse('登录成功')
#
#             return HttpResponse('登录失败')
# 设置cookie
from datetime import datetime, timedelta


def set_cookie(request):
    # 创建响应对象
    response = HttpResponse('设置cookie')
    # 将数据存储在cookie中,默认有效时间   保存在浏览器缓存中，关闭浏览器数据丢失
    # response.set_cookie('username', 'chang', max_age=24 * 60 * 60 * 7, expires=datetime.now()+timedelta(days=14))
    response.set_signed_cookie('username', 'chang', salt='chtalwj', max_age=24 * 60 * 60 * 7)

    return response


# 获取cookie
def get_cookie(request):
    # str = request.COOKIES.get('username')
    str = request.get_signed_cookie('username', salt='chtalwj')
    return HttpResponse(str)


# 设置session
def set_session(request):
    # 在session中存放数据
    request.session['username'] = 'chang'
    # 输出cookie中的sessionid
    print(request.session.session_key)
    # 设置有效时间
    request.session.set_expiry(24 * 60 * 60 * 7)
    # 删除session数据
    # del request.session['username']
    return HttpResponse('设置成功！')


# 获取session
def get_session(request):
    username = request.session['username']
    return HttpResponse(username)


# # 处理登录功能
# def login(request):
#     # 根据不同的请求方式处理不同的需求
#     if request.method == 'GET':
#         return render(request, 'form.html')
#     else:
#         # 获取请求参数
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         # 查询数据库
#         if username and password:
#             # 判断是否非空
#             c = UserInfo.objects.filter(username=username, password=password).count()
#             if c == 1:
#                 return HttpResponse('登录成功！')
#
#         return HttpResponse('登录失败！')

# 查询UserInfo里面的所有数据
# def show(request):
#     userdata = UserInfo.objects.all()

# return render(request, 'show.html', {'userdata': userdata})


# 将数据进行分页
def page(num, size=5):
    # 接收当前页码数
    num = int(num)
    # 总记录数
    totalusers = UserInfo.objects.count()
    # 总页数
    totalpages = int(math.ceil(totalusers * 1.0 / size))
    # 判断是否越界
    if num < 1:
        num = 1

    if num > totalpages:
        num = totalpages

    # 计算出每页显示的记录
    users = UserInfo.objects.all()[((num - 1) * size):(num * size)]

    return users, num


def show(request):
    # 接受请求参数 num
    num = request.GET.get('num', 1)
    # 处理分页请求
    users, n = page(num)
    # 上一页的页码
    pre_page_num = n - 1
    # 下一页的页码
    next_page_num = n + 1

    return render(request, 'show.html', {'users': users, 'pre_page_num': pre_page_num, 'next_page_num': next_page_num})


# username = request.POST.get('username', 'x')
# password = request.POST.get('password', 'y')
#
# print(username)
# print(password)

# 判断
# if username == 'zhangsan' and password == '123':
#     return HttpResponse('登录成功！')

# return HttpResponse('登录失败！')


# def login(request):
#     if request.method == 'GET':
#         return render(request, 'register.html')
#
#     if request.method == 'POST':
#         # 如果登录成功，返回baidu界面
#         name = request.POST.get('name')
#         password = request.POST.get('password')
#         # 查询用户是否在数据库中
#         if UserInfo.objects.filter(username=name).exists():
#             user = UserInfo.objects.get(username=name)
#             if password(password=user.password):
#                 return render(request, 'base1.html')
#             else:
#                 return render(request, 'register.html', {'password': '用户密码错误'})
#         else:
#             return render(request, 'register.html', {'name': '用户不存在'})


# def checkusername(request):
#     result = {'code':10001,'content':''}
#     #get 请求
#     username = request.GET.get("name")
#     print(username)
#     # 判断用户是否存在
#     user = UserInfo.objects.filter(name=username).first()
#     if user:
#         # 存在
#         result = {'code': 10001, 'content': '用户名已存在'}
#     else:
#         result = {'code': 10000, 'content': '用户名可以使用'}
#
#     return JsonResponse(result)
"""新增"""

# user = UserInfo()
# user.username = 'chang'
# user.password = 123456
# user.save()

# 新增操作
# user = UserInfo.objects.create(
#     username='卢本伟',
#     password='55k'
# )
# user = Post.objects.create(
#     title='卢本伟',
#     desc='55k',
#     content='a',
#     created='2',
#     category_id='2',
# )

#

"""
基本查询
    1.get
    2.all
    3.count
"""

# gte 查询单一
# try:
#     user = UserInfo.objects.get(id=1)
# except  UserInfo.DoesNotExist:
#     pass
# logging.error(user)
#
# all查询所有
# users = UserInfo.objects.all()
# logging.error(users)
#
# count计数
# count = UserInfo.objects.count()
# logging.error(count)
#
"""
过滤查询
    1.filter  返回查询集   用<QuerySet>包起来，为空也会显示
    2.exclude  排除掉符合条件剩下的结果
    3.get  过滤单一结果
"""

# F对象：实现两个字段之间的比较也支持运算
from django.db.models import F, Q

# user = UserInfo.objects.filter(id=1)
# logging.error(user)

"""
模糊查询
    1.contains:是否包含
    2.startwith , endwith:以指定值开头或结尾
    3.isnull:是否为null
    4.in:范围查询
    5.比较查询：gt大于 , gte大于等于 , lt小于 , lte小于等于 , exclude不等于
    6.日期查询：year , month , day , week_day , hour , minute , second 对日期时间类型的属性进行运算
"""

# user = UserInfo.objects.filter(username__contains = '伟')
# logging.error(user)

# user = UserInfo.objects.filter(id__in = [2, 4])
# logging.error(user)

# user = UserInfo.objects.filter(id__gt = 6)
# logging.error(user)

# user = UserInfo.objects.exclude(username = '大司马')
# logging.error(user)

#
# # Q对象：实现  and(,)  or(|)    not(~)
# user = UserInfo.objects.filter(~Q(id=1))
# logging.error(user)
#
# """聚合查询"""
# from django.db.models import Sum, Avg, Count, Max, Min
#
# user_sum = UserInfo.objects.aggregate(Sum('id'))
# logging.error(user_sum)
#
# user_sum = UserInfo.objects.count('id')
#
# """排序"""
# # 默认升序，降序在前面加-，例如-id
# user = UserInfo.objects.order_by('id')
# logging.error(user)
#
# """关联查询"""
#
# # 一查多
# user = UserInfo.objects.get(id=1)
# #在一的模型这方会有一个 多的那方模型名小写_set 隐式字段
# words = words.WordInfo_set.all()
# logging.error(words)
#
# #多查一
# words = WordInfo.objects.get(username = 'aaa')
# user = word.huser
# logging.error(words)


"""
删除
    1.模型对象delete：物理删除，只能删除一个
    2.模型类.objects.filter().delete():可以删除多个
"""

# user = UserInfo.objects.get(id = 7)
# res = user.delete()
# logging.error(res)

# user_qs = UserInfo.objects.filter(username = 'chang')
# res = user_qs.delete()
# logging.error(res)

"""
修改更新
    1.save：修改模型类对象的属性，然后执行save()方法
    2.update：使用模型类.objects.filter().update(),会返回受影响的行数
"""
# user = UserInfo.objects.get(id = 2)
# user.username = 'luo'
# user.save()


# user_qs = UserInfo.objects.filter(id = 2).update(password = '99999')
# logging.error(user_qs)


"""
查询集
    1.all()：返回所有数据
    2.filter():返回满足条件的数据
    3.exclude():返回满足条件之外的数据
    4.order_by()：对结果进行排序
    
    查询集可以再次调用过滤器进行过滤
    
    exists():判断查询集中是否有数据，如果有则返回True，没有则返回False
    
    
    两大特性：1.惰性执行：创建查询集不会访问数据库，直到调用数据时，才会访问 数据库，调用数据的情况包括迭代、序列化、与if合用
             2.缓存：使用同一个查询集，第一次使用时会发生数据库的查询，然后Django会把结果缓存下来，再次使用这个查询集时会使用缓存的数据，减少了数据库的查询次数

    限制查询集：[a:b](表示从a查到b)
    

"""

# user = UserInfo.objects.all()
# logging.error(user)

# 试一试表单
# class biaodan(View):
#
#     def get(self, request):
#         data = {
#             'name': 'cht',
#             'alist': [1, 2, 3, 4],
#             'adict': {'age': 21, 'sex': 1},
#             'a': 10,
#             'ahtml': '<h1>大标题<h1>',
#             'nowdate': timezone.now(),
#         }
#
#         return render(request, 'register.html', context=data)
# 学到116
