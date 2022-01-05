from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
#from mptt.models import MPTTModel, TreeForeignKey
# coding = utf-8
# Create your models here.  User对应数据库中的表

# 创建同步文件，在Terminal中输入以下命令：  python manage.py makemigrations
# 创建表结构并同步到数据库，输入以下命令：   python manage.py migrate
class UserInfo(models.Model):
    # 如果没有的话，默认会生成一个名称为id的列，如果要显示的自定义一个自增列
    id = models.AutoField(primary_key=True)
    # 类里面的字段代表数据表中的字段(username)，数据类型则由CharField（相当于varchar）
    username = models.CharField(max_length=100, verbose_name='用户名')
    # 数据库表中的密码字段
    password = models.CharField(max_length=100, verbose_name='密码')
    # 数据库表中的手机号字段
    # phone = models.CharField(max_length=20, verbose_name='手机号')
    ctime = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'luntan_user'  # 自定义表的名字
        verbose_name = '用户'

        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


# 创建类别表
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    cname = models.CharField(max_length=30,unique=True,verbose_name=u'类别名称')


    class Meta:
        db_table = 'luntan_category'
        verbose_name_plural=u'类别'

    def __unicode__(self):
        return u'Category:%s'%self.cname

class Tag(models.Model):
    tname = models.CharField(max_length=30,unique=True,verbose_name=u'标签名称')

    class Meta:
        db_table = 'luntan_tag'
        verbose_name_plural = u'标签'

    def __unicode__(self):
        return u'Tag:%s' % self.tname

class Post(models.Model):
    title = models.CharField(max_length=100,unique=True)
    desc = models.CharField(max_length=100)
    content = RichTextUploadingField(null = True,blank = True)
    created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
    author = models.ForeignKey(to="UserInfo",verbose_name="作者",on_delete=models.CASCADE)

    # 点赞和评论时，记着更新like_count，comment_count。自增1/自减1： F 实现
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)

    # 获取文章地址
    def get_absolute_url(self):
        return reverse('post:post_detail', args=[self.id])

    class Meta:
        db_table = 'luntan_post'
        verbose_name_plural = u'帖子'

    def __unicode__(self):
        return u'Post:%s' % self.title






class Like(models.Model):
    """点赞记录表"""
    user = models.ForeignKey(to="UserInfo", verbose_name="点赞者",on_delete=models.CASCADE)
    post = models.ForeignKey(to="Post", verbose_name="点赞的文章",on_delete=models.CASCADE)
    ctime = models.DateTimeField(auto_now_add=True, verbose_name="点赞时间")

    # 建立联合唯一索引，限定每个用户给每篇文章只能点赞一次
    class Meta:
        unique_together = [
            ('user', 'post'),
        ]
# class Answer(models.Model):
#     a_content = RichTextUploadingField(null = True,blank = True)
#     a_date = models.DateTimeField(auto_now_add=True)
#     a_post = models.ForeignKey(Post,on_delete=models.CASCADE)
#     a_user = models.ForeignKey(UserInfo,on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = 'luntan_answer'
#         verbose_name_plural = u'评论'
#
#     def __unicode__(self):
#         return u'Answer:%s' % self.a_content


#django - mptt









