from django.conf.urls import url
from django.urls import include

from . import views
#调用css
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


#url(路径，函数名，name = 给路由起个别名)

# 应用中的所有路由都写在此列表中，路由的匹配是自上而下的，在应用的最后尽量加/$
urlpatterns = [
    #url(正则，视图名）,
    url(r'^index/$', views.index,name='index'),

    url(r'^index2/$', views.index2),

    #获取url路径中的数据
    #此种正则组提取数据，实际是用位置参数形式，此种写法必须形参和实参位置数量一一对应（不建议使用）
    # url(r'^weather/([a-z]+)/(\d{4})/$', views.weather1),

    # 此种正则组提取数据，实际是用关键字参数形式，要求形参名要和正则组别名一致，顺序任意
    url(r'^weather/(?P<city>[a-z]+)/(?P<year>\d{4})/$', views.weather1),

    #获取查询字符串
    url(r'^get_canshu/$', views.get_canshu),

    #获取查询请求体中的表单数据
    url(r'^get_data/$', views.get_data),

    #获取非表单数据 json
    url(r'^get_json/$', views.get_json),

    #响应对象 response_test
    url(r'^response_test/$', views.response_test),

    #重定向使用
    url(r'^redirect_test/$', views.redirect_test),

    #cookie使用
    url(r'^cookie_test/$', views.cookie_test),

    #session使用
    url(r'^session_test/$', views.session_test),


    #  """类视图的路由"""

    #类视图中的as_view的作用：
    #将类视图中的方法转换成函数
    #它里面dispatch方法可以根据本次请求方法动态查找类中和请求方法同名但小写的方法
    url(r'^DemoView/$', views.DemoView.as_view()),


    #直接用装饰器装饰as_view方法返回的view函数，只不过这样会把类视图中的所有方法都装饰
    # url(r'^DemoView/$', views.my_decorator(views.DemoView.as_view())),

    #TempView类视图
    url(r'^TempView/$', views.TempView.as_view()),
    url(r'^TempView2/$', views.TempView2.as_view()),
    url(r'^TempView3/$', views.TempView3.as_view()),


    #zhuce 注册页面
    # url('^zhuce/$', views.zhuce),
    url(r'^login/$', views.login),

    #展示数据库数据
    url(r'^show/$', views.show),

    #设置cookie
    url(r'^set_cookie/$', views.set_cookie),
    #获取cookie
    url(r'^get_cookie/$', views.get_cookie),

    #设置session
    url(r'^set_session/$', views.set_session),
    #获取session
    url(r'^get_session/$', views.get_session),



    # url(r'^index_view/$', views.index_view),

    #展示页面
    url(r'^look/$', views.look),

    #分页
    url(r'^page/(\d+)$', views.zhanshi),

    #阅读全文
    url(r'^post/(\d+)$', views.detail),

    #发帖
    url(r'^ft/$', views.ft),


    #展示
    url(r'^zhanshi/$', views.zhanshi),


    url(r'^detail/$', views.detail),

    #发帖子
    # url(r'^comments/$', views.comments),



    #多级评论
    # 已有代码，处理一级回复
    # url('post-comment/<int:article_id>', views.post_comment, name='post_comment'),
    # # 新增代码，处理二级回复
    # url('post-comment/<int:article_id>/<int:parent_comment_id>', views.post_comment, name='comment_reply')

]
