学习笔记
基本应用
创建项目:
django-admin startproject 项目名称

目录结构:
manage.py是项目管理文件，通过它管理项目。
与项目同名的目录，此处为test1。
_init_.py是一个空文件，作用是这个目录test1可以被当作包使用。
settings.py是项目的整体配置文件。
urls.py是项目的URL配置文件。
wsgi.py是项目与WSGI兼容的Web服务器入口，详细内容会在布署中讲到
创建应用:  
python manage.py startapp 应用名称

应用的目录结构:
_init.py_是一个空文件，表示当前目录booktest可以当作一个python包使用。
tests.py文件用于开发测试用例，在实际开发中会有专门的测试人员，这个事情不需要我们来做。
models.py文件跟数据库操作相关。
views.py文件跟接收浏览器请求，进行处理，返回页面相关。
admin.py文件跟网站的后台管理相关。
migrations文件夹保存迁移文件记录。
安装应用:
在settings.py文件中设置:

INSTALLED_APPS = {‘应用名称’}

 

开发服务器:
python manage.py runserver ip:端口

例：

python manage.py runserver

可以不写IP和端口，默认IP是127.0.0.1，默认端口为8000

 
ORM(Object Relation Mapping)框架
通过类和类对象操作关系数据库中对应的数据表, 根据设计的类自动生成数据库中对应的表格

定义模型类:
模型类定义在models.py文件中，继承自models.Model类。不需要定义主键列，在生成时会自动添加，并且值为自动增长。

from django.db import models
class BookInfo(models.Model):
    btitle = models.CharField(max_length=20)
    bpub_date = models.DateField()
模型迁移:
1)    生成迁移文件: python manage.py makemigrations

2） 根据第一步生成的迁移文件在数据库中创建表: python manage.py migrate

 
后台管理:
使用Django的管理模块，需要按照如下步骤操作：

1)   管理界面本地化

打开settings.py文件，找到语言编码、时区的设置项，将内容改为如下：

LANGUAGE_CODE = 'zh-hans'  #使用中国语言

TIME_ZONE = 'Asia/Shanghai'  #使用中国上海时间

2)   创建管理员

python manage.py createsuperuser

在浏览器中输入: http://127.0.0.1:8000/admin/进行数据库的页面访问

3)   注册模型类

要在应用的admin.py文件中写入代码:
from django.contrib import admin
from booktest.models import BookInfo,HeroInfo
admin.site.register(BookInfo)
admin.site.register(HeroInfo)
 

4)   自定义管理页面

在应用的admin.py文件中自定义类继承admin.ModelAdmin类

属性list_display表示要显示哪些属性
class BookInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'btitle', 'bpub_date']
 

修改模型类BookInfo的注册代码如下
admin.site.register(BookInfo, BookInfoAdmin)
 

 

模型
Django中模型类的方法与数据库操作对应:
save(): 生成insert, update语句

delete(): 生成delete语句

all(), get(): 生成select语句

 

修改数据库:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test2', #数据库名字，
        'USER': 'root', #数据库登录用户名
        'PASSWORD': 'mysql', #数据库登录密码
        'HOST': 'localhost', #数据库所在主机
        'PORT': '3306', #数据库端口
    }
}
 
注意: MySQL的数据库不会自动生成, 需要手动创建

还需要在项目的__init__.py文件中加上:

import pymysql
pymysql.install_as_MySQLdb()
定义属性：
django会为表创建自动增长的主键列，每个模型只能有一个主键列，如果使用选项设置某属性为主键列后django不会再创建自动增长的主键列. 默认创建的主键列属性为id，可以使用pk代替，pk全拼为primary key。注意：pk是主键的别名，若主键名为id2，那么pk是id2的别名。

定义属性方式: 属性=models.字段类型(选项)

字段类型：
使用时需要引入django.db.models包，字段类型如下：

AutoField：自动增长的IntegerField，通常不用指定，不指定时Django会自动创建属性名为id的自动增长属性。
BooleanField：布尔字段，值为True或False。
NullBooleanField：支持Null、True、False三种值。
CharField(max_length=字符长度)：字符串。
参数max_length表示最大字符个数。
TextField：大文本字段，一般超过4000个字符时使用。
IntegerField：整数。
DecimalField(max_digits=None, decimal_places=None)：十进制浮点数。
参数max_digits表示总位数。
参数decimal_places表示小数位数。
FloatField：浮点数。
DateField[auto_now=False, auto_now_add=False])：日期。
参数auto_now表示每次保存对象时，自动设置该字段为当前时间，用于"最后一次修改"的时间戳，它总是使用当前日期，默认为false。
参数auto_now_add表示当对象第一次被创建时自动设置当前时间，用于创建的时间戳，它总是使用当前日期，默认为false。
参数auto_now_add和auto_now是相互排斥的，组合将会发生错误。
TimeField：时间，参数同DateField。
DateTimeField：日期时间，参数同DateField。
FileField：上传文件字段。
ImageField：继承于FileField，对上传的内容进行校验，确保是有效的图片。
字段中的选项：
通过选项实现对字段的约束，选项如下：

null：如果为True，表示允许为空，默认值是False。
blank：如果为True，则该字段允许为空白，默认值是False。
对比：null是数据库范畴的概念，blank是表单验证范畴的。
db_column：字段的名称，如果未指定，则使用属性的名称。
db_index：若值为True, 则在表中会为此字段创建索引，默认值是False。
default：默认值。
primary_key：若为True，则该字段会成为模型的主键字段，默认值是False，一般作为AutoField的选项使用。
unique：如果为True, 这个字段在表中必须有唯一值，默认值是False。
 

条件运算符：
1） 字段__exact：表示等于，也可以直接用等号表示：

list=BookInfo.objects.filter(id__exact=1)

2） 字段__contains：是否包含

说明：如果要包含%无需转义，直接写即可。

list = BookInfo.objects.filter(btitle__contains='传')

3） startswith、endswith：以指定值开头或结尾

list = BookInfo.objects.filter(btitle__endswith='部')

以上运算符都区分大小写，在这些运算符前加上i表示不区分大小写，如iexact、icontains、istartswith、iendswith.

4） isnull空查询

list = BookInfo.objects.filter(btitle__isnull=False)

5） in：是否包含在范围内

list = BookInfo.objects.filter(id__in=[1, 3, 5])

6） gt、gte、lt、lte：大于、大于等于、小于、小于等于

list = BookInfo.objects.filter(id__gt=3)

7） 不等于的运算符，使用exclude()过滤器

list = BookInfo.objects.exclude(id=3)

8） 日期查询

year、month、day、week_day、hour、minute、second：对日期时间类型的属性进行运算

list = BookInfo.objects.filter(bpub_date__year=1980)

例：查询1980年1月1日后发表的图书。

list = BookInfo.objects.filter(bpub_date__gt=date(1980, 1, 1))

F（Field）对象， 用于两个属性之间的比较：
from django.db.models import F

语法：F(属性名)

list = BookInfo.objects.filter(bread__gte=F('bcomment'))  阅读量大于评论数的书本

list = BookInfo.objects.filter(bread__gt=F('bcomment') * 2)  F对象使用算数

Q对象：
多个过滤器逐个调用表示逻辑与关系，同sql语句中where部分的and关键字

list=BookInfo.objects.filter(bread__gt=20,id__lt=3) 或 list=BookInfo.objects.filter(bread__gt=20).filter(id__lt=3)

Q对象和 | 运算符一起使用表示逻辑or， 语法：Q(属性名__运算符=值)

Q对象可以使用&、|连接，&表示逻辑与，|表示逻辑或

list = BookInfo.objects.filter(Q(bread__gt=20) | Q(pk__lt=3))

Q对象前可以使用~操作符，表示非not

list = BookInfo.objects.filter(~Q(pk=3))

聚合函数：
聚合函数包括：Avg，Count，Max，Min，Sum，被定义在django.db.models中

list = BookInfo.objects.aggregate(Sum('bread'))，aggregate的返回值是一个字典类型，格式如下：{'属性名__聚合类小写:值}， 如{'bread__sum':3}

计数count不使用aggregate， list = BookInfo.objects.count()，返回的数字

查询集:
查询集表示从数据库中获取的对象集合，在管理器上调用某些过滤器方法会返回查询集，查询集可以含有零个、一个或多个过滤器。过滤器基于所给的参数限制查询的结果，从Sql的角度，查询集和select语句等价，过滤器像where和limit子句。

返回查询集的过滤器如下：
all()：返回所有数据。
filter()：返回满足条件的数据。
exclude()：返回满足条件之外的数据，相当于sql语句中where部分的not关键字。
order_by()：对结果进行排序。
返回单个值的过滤器如下：
get()：返回单个满足条件的对象
如果未找到会引发"模型类.DoesNotExist"异常。
如果多条被返回，会引发"模型类.MultipleObjectsReturned"异常。
count()：返回当前查询结果的总条数。
aggregate()：聚合，返回一个字典。
判断某一个查询集中是否有数据：
exists()：判断查询集中是否有数据，如果有则返回True，没有则返回False。
两大特性:
惰性执行：创建查询集不会访问数据库，直到调用数据时，才会访问数据库，调用数据的情况包括迭代、序列化、与if合用。
缓存：使用同一个查询集，第一次使用时会发生数据库的查询，然后把结果缓存下来，再次使用这个查询集时会使用缓存的数据。
查询集的缓存:
每个查询集都包含一个缓存来最小化对数据库的访问。

在新建的查询集中，缓存为空，首次对查询集求值时，会发生数据库查询，django会将查询的结果存在查询集的缓存中，并返回请求的结果，接下来对查询集求值将重用缓存中的结果。

list=BookInfo.objects.all()
[book.id for book in list]
[book.id for book in list]
 

限制查询集
可以对查询集进行取下标或切片操作，等同于sql中的limit和offset子句。

注意：不支持负数索引。

对查询集进行切片后返回一个新的查询集，不会立即执行查询。

如果获取一个对象，直接使用[0]，等同于[0:1].get()，但是如果没有数据，[0]引发IndexError异常，[0:1].get()如果没有数据引发DoesNotExist异常。

list=BookInfo.objects.all()[0:2]
 

模型类关系
关系字段类型
关系型数据库的关系包括三种类型：

ForeignKey：一对多，将字段定义在多的一端中。
ManyToManyField：多对多，将字段定义在任意一端中。
OneToOneField：一对一，将字段定义在任意一端中。
可以维护递归的关联关系，使用'self'指定，详见"自关联"。
一对多关系
参见booktest应用中的BookInfo类和HeroInfo类。

hbook = models.ForeignKey("BookInfo")
 

多对多关系
设计一个新闻类和新闻类型类，一个新闻类型下可以用很多条新闻，一条新闻也可能归属于多种新闻类型。

 
class TypeInfo(models.Model):
  tname = models.CharField(max_length=20) #新闻类别

class NewsInfo(models.Model):
  ntitle = models.CharField(max_length=60) #新闻标题
  ncontent = models.TextField() #新闻内容
  npub_date = models.DateTimeField(auto_now_add=True) #新闻发布时间
  ntype = models.ManyToManyField('TypeInfo') #通过ManyToManyField建立TypeInfo类和NewsInfo类之间多对多的关系
 
 

关联查询
通过对象执行关联查询
在定义模型类时，可以指定三种关联关系，最常用的是一对多关系:

由一到多的访问语法：

# 一对应的模型类对象.多对应的模型类名小写_set

b = BookInfo.objects.get(id=1)
b.heroinfo_set.all()
 

由多到一的访问语法:

# 多对应的模型类对象.多对应的模型类中的关系类属性名

h = HeroInfo.objects.get(id=1)
h.hbook  # 获得一对应的模型类对象
 

访问一对应的模型类关联对象的id语法:

多对应的模型类对象.关联类属性_id

h = HeroInfo.objects.get(id=1)
h.book_id
 

 

通过模型类执行关联查询
由多模型类条件查询一模型类数据:
语法如下：

关联模型类名小写__属性名__条件运算符=值
例：查询图书，要求图书中英雄的描述包含'八'。

list = BookInfo.objects.filter(heroinfo__hcontent__contains='八')
由一模型类条件查询多模型类数据:
语法如下：

一模型类关联属性名__一模型类属性名__条件运算符=值
例：查询书名为“天龙八部”的所有英雄。

list = HeroInfo.objects.filter(hbook__btitle='天龙八部')
 

 

自关联:
对于地区信息、分类信息等数据，表结构非常类似，每个表的数据量十分有限，为了充分利用数据表的大量数据存储功能，可以设计成一张表，内部的关系字段指向本表的主键，这就是自关联的表结构。

说明：关系属性使用self指向本类，要求null和blank允许为空，因为一级数据是没有父级的。

#定义地区模型类，存储省、市、区县信息
class AreaInfo(models.Model):
    atitle=models.CharField(max_length=30)#名称
    aParent=models.ForeignKey('self',null=True,blank=True)#关系
视图定义如下:

def index(request):
    currentArea = AreaInfo.objects.get(atitle='桂林市', aParent__isnull=False)
    return render(request, 'booktest/index.html', dict(currentArea=currentArea))
 html页面如下:

 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>index</title>
</head>
<body>
    <p>当前地区: {{ currentArea.atitle }}</p>
    <hr>
    <p>上级地区: {{ currentArea.aParent.atitle }}</p>
    <hr>
    <p>下级地区: </p>
    <ul>
        {% for downArea in currentArea.areainfo_set.all %}
            <li>{{ downArea.atitle }}</li>
        {% endfor %}

    </ul>
</body>
</html>
 
 

模型类扩展:
模型实例方法
str()：在将对象转换成字符串时会被调用。
save()：将模型对象保存到数据表中，ORM框架会转换成对应的insert或update语句。
delete()：将模型对象从数据表中删除，ORM框架会转换成对应的delete语句。
 

模型类的属性
属性objects：管理器，是models.Manager类型的对象，用于与数据库进行交互。

当没有为模型类定义管理器时，Django会为每一个模型类生成一个名为objects的管理器，自定义管理器后，Django不再生成默认管理器objects。

为模型类BookInfo定义管理器books语法如下：

class BookInfo(models.Model):
    ...
    books = models.Manager()
 

管理器Manager
管理器是Django的模型进行数据库操作的接口，Django应用的每个模型类都拥有至少一个管理器。Django支持自定义管理器类，继承自models.Manager。

自定义管理器类主要用于两种情况：

1.修改原始查询集，重写all()方法
2.向管理器类中添加额外的方法，如向数据库中插入数据。
 

1.修改原始查询集，重写all()方法。

a）打开booktest/models.py文件，定义类BookInfoManager

 
#图书管理器
class BookInfoManager(models.Manager):
    def all(self):
        #默认查询未删除的图书信息
        #调用父类的成员语法为：super().方法名
        return super().all().filter(isDelete=False)
 
 

 

b）在模型类BookInfo中定义管理器

class BookInfo(models.Model):
    ...
    books = BookInfoManager()
 

2.在管理器类中定义创建对象的方法

对模型类对应的数据表进行操作时，推荐将这些操作数据表的方法封装起来，放到模型管理器类中。

打开booktest/models.py文件，定义方法create:

 
class BookInfoManager(models.Manager):
    ...
    #创建模型类，接收参数为属性赋值
    def create_book(self, title, pub_date):
        #创建模型类对象self.model可以获得模型类
        book = self.model()
        book.btitle = title
        book.bpub_date = pub_date
        book.bread=0
        book.bcommet=0
        book.isDelete = False
        # 将数据插入进数据表
        book.save()
        return book
 
 

 

元选项
在模型类中定义类Meta，用于设置元信息，如使用db_table自定义表的名字。

数据表的默认名称为： <app_name>_<model_name>, 例如: booktest_bookinfo

指定BookInfo模型类生成的数据表名为bookinfo:

 
class BookInfo(models.Model):
    """书籍类"""
    btitle = models.CharField(max_length=50)
    bpubDate = models.DateField()
    bread = models.IntegerField(default=0)
    bcomment = models.IntegerField(default=0)
    isDelete = models.BooleanField(default=False)
    objects = BookManager()
    
    class Meta:
        db_table = "bookinfo"
 
 

 

 视图
 视图负责接受Web请求HttpRequest，进行逻辑处理，返回Web响应HttpResponse给请求者。

使用视图的过程
(1)在"应用/views.py"中定义视图。(2)配置URLconf，将视图函数和url对应起来。

URLconf
用户通过在浏览器的地址栏中输入网址请求网站，对于Django开发的网站，向哪一个视图进行处理请求，是由url匹配找到的。

 配置
1）在settings.py中通过ROOT_URLCONF指定url配置，默认已经有此配置。ROOT_URLCONF='项目名称.urls'

 2）打开项目的urls.py可以看到默认配置。

 
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('booktest.urls')),
]
 
语法
语法一：包含，一般在自定义应用中创建一个urls.py来定义url。

这种语法用于test3/urls.py中，目的是将应用的urls配置到应用内部，数据更清晰并且易于维护。

url(正则,include('应用.urls'))

语法二：定义，指定URL和视图函数的对应关系。

在应用内部创建urls.py文件，指定请求地址与视图的对应关系。

url(正则,'视图函数名称')

说明1：正则部分推荐使用r，表示字符串不转义，这样在正则表达式中使用\只写一个就可以。 说明2：不能在开始加反斜杠，推荐在结束加反斜杠(index, index/)。

 

获取值
请求的url被看做是一个普通的python字符串，进行匹配时不包括域名、get或post参数。 如请求地址如下：

http://127.0.0.1:8000/delete1/?a=10

 

可以在匹配过程中从url中捕获参数，每个捕获的参数都作为一个普通的python字符串传递给视图。

方式一：提取位置参数
直接使用小括号，通过位置参数传递给视图。

1）为了提取参数，修改上面的正则表达式如下：

url(r'^delete(\d+)/$',views.show_arg),
2）修改视图show_arg如下：

注意：参数的名字是任意的如a1、b8，尽量做到见名知意。

def show_arg(request,id):
    return HttpResponse('show arg %s'%id)
 

方式二：关键字参数
在正则表达式部分为组命名。

1）修改正则表达式如下：

其中?P部分表示为这个参数定义的名称为id，可以是其它名称，起名做到见名知意。

url(r'^delete(?P<id1>\d+)/$',views.show_arg),
2）修改视图show_arg如下：

注意：视图show_arg此时必须要有一个参数名为id1，否则报错。

def show_arg(request,id1):
    return HttpResponse('show %s'%id1)
内置错误视图
Django内置处理HTTP错误的视图，主要错误及视图包括：

404错误：page not found视图
500错误：server error视图
如果想看到错误视图而不是调试信息，需要修改setting.py文件的DEBUG项。

DEBUG = False
ALLOWED_HOSTS = ['*', ]
 

自定义错误视图
在templates文件加下新建404.html或者500.html页面即可

 

HttpReqeust对象
服务器接收到http协议的请求后，会根据报文创建HttpRequest对象，这个对象不需要我们创建，直接使用服务器构造好的对象就可以。视图的第一个参数必须是HttpRequest对象，在django.http模块中定义了HttpRequest对象的API。

属性
下面除非特别说明，属性都是只读的。

path：一个字符串，表示请求的页面的完整路径，不包含域名和参数部分。
method：一个字符串，表示请求使用的HTTP方法，常用值包括：'GET'、'POST'。
在浏览器中给出地址发出请求采用get方式，如超链接。
在浏览器中点击表单的提交按钮发起请求，如果表单的method设置为post则为post请求。
encoding：一个字符串，表示提交的数据的编码方式。
如果为None则表示使用浏览器的默认设置，一般为utf-8。
这个属性是可写的，可以通过修改它来修改访问表单数据使用的编码，接下来对属性的任何访问将使用新的encoding值。
GET：QueryDict类型对象，类似于字典，包含get请求方式的所有参数。
POST：QueryDict类型对象，类似于字典，包含post请求方式的所有参数。
FILES：一个类似于字典的对象，包含所有的上传文件。
COOKIES：一个标准的Python字典，包含所有的cookie，键和值都为字符串。
session：一个既可读又可写的类似于字典的对象，表示当前的会话，只有当Django 启用会话的支持时才可用，详细内容见"状态保持"。
QueryDict对象
定义在django.http.QueryDict
HttpRequest对象的属性GET、POST都是QueryDict类型的对象
与python字典不同，QueryDict类型的对象用来处理同一个键带有多个值的情况
方法get()：根据键获取值
如果一个键同时拥有多个值将获取最后一个值
如果键不存在则返回None值，可以设置默认值进行后续处理
　　　　dict.get('键',默认值), 可以简写为dict['键']

 

方法getlist()：根据键获取值，值以列表返回，可以获取指定键的所有值
如果键不存在则返回空列表[]，可以设置默认值进行后续处理, 
dict.getlist('键',默认值)
GET属性
请求格式：在请求地址结尾使用?，之后以"键=值"的格式拼接，多个键值对之间以&连接。

例如: http://www.itcast.cn/?a=10&b=20&c=python 其中的请求参数为：a=10&b=20&c=python

分析请求参数，键为'a'、'b'、'c'，值为'10'、'20'、'python'。
在Django中可以使用HttpRequest对象的GET属性获得get方方式请求的参数。
GET属性是一个QueryDict类型的对象，键和值都是字符串类型。
键是开发人员在编写代码时确定下来的。
值是根据数据生成的。
 

POST属性
使用form表单请求时，method方式为post则会发起post方式的请求，需要使用HttpRequest对象的POST属性接收参数，POST属性是一个QueryDict类型的对象。

问：表单form如何提交参数呢？

答：表单控件name属性的值作为键，value属性的值为值，构成键值对提交。

如果表单控件没有name属性则不提交。
对于checkbox控件，name属性的值相同为一组，被选中的项会被提交，出现一键多值的情况。
键是表单控件name属性的值，是由开发人员编写的。
值是用户填写或选择的。
1）打开booktest/views.py文件，创建视图show_reqarg

 
def show_reqarg(request):
    if request.method == 'GET':
        a = request.GET['a']
        b = request.GET['b']
        c = request.GET['c']
        print(a, b, c)
        return render(request, 'booktest/index.html')
    else:
        hobby = request.POST.getlist("hobby")
        print(hobby)
        return render(request, 'booktest/index.html')
 
2）修改templates/booktest目录下的index.html，添加代码如下：

 
<!DOCTYPE html>
<html lang="en">

    <head>
        <meta charset="UTF-8">
        <title>index</title>
    </head>

    <body>
        3.提交数据的两种方式： get方式:
        <br/>
        <a href="/show_reqarg/?a=1&b=2&c=python">get方式提交数据</a><br/> post方式:
        <br/>
        <form method="post" action="/show_reqarg/">
            {% csrf_token %}
            姓名：<input type="text" name="uname"><br/> 性别：男
            <input type="radio" name="gender" value="男" /> 女
            <input type="radio" name="gender" value="女" /><br/> 爱好： 吃饭
            <input type="checkbox" name="hobby" value="吃饭" /> 睡觉
            <input type="checkbox" name="hobby" value="睡觉" /> 打豆豆
            <input type="checkbox" name="hobby" value="打豆豆" /><br>
            <input type="submit" value="提交">
        </form>
    </body>

</html>
 
 

 
HttpResponse对象
视图在接收请求并处理后，必须返回HttpResponse对象或子对象。在django.http模块中定义了HttpResponse对象的API。HttpRequest对象由Django创建，HttpResponse对象由开发人员创建。

属性
content：表示返回的内容。
charset：表示response采用的编码字符集，默认为utf-8。
status_code：返回的HTTP响应状态码。
content-type：指定返回数据的的MIME类型，默认为'text/html'。
方法
_init_：创建HttpResponse对象后完成返回内容的初始化。
set_cookie：设置Cookie信息。
set_cookie(key, value='', max_age=None, expires=None)

cookie是网站以键值对格式存储在浏览器中的一段纯文本信息，用于实现用户跟踪。
max_age是一个整数，表示在指定秒数后过期。
expires是一个datetime或timedelta对象，会话将在这个指定的日期/时间过期。
max_age与expires二选一。
如果不指定过期时间，在关闭浏览器时cookie会过期。
delete_cookie(key)：删除指定的key的Cookie，如果key不存在则什么也不发生。
write：向响应体中写数据。
子类JsonResponse
在浏览器中使用javascript发起ajax请求时，返回json格式的数据，此处以jquery的get()方法为例。类JsonResponse继承自HttpResponse对象，被定义在django.http模块中，创建对象时接收字典作为参数。

JsonResponse对象的content-type为'application/json'。