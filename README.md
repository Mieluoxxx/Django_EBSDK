

# 文心小课堂

## 一、Django使用基本配置

### 第一讲、创建Django文件

#### 1.安装 Django 

```cmd
pip install django
# 安装不同的Django版本如下：
# pip install django==2.2
```

#### 2.创建项目

```cmd
django-admin startproject YourProject #创建一个空白的django项目
cd YourProject                        #进入项目文件夹
```

#### 3.运行开发服务器

```cmd
python manage.py migrate  		  	  #进行文件迁移
python manage.py runserver			  #启动Django的开发服务器。在本地环境中运行网站
```

#### 4. [localhost:8000](localhost:8000)，欢迎界面


#### 5.创建一个自定义的APP

Django App 一般分为三大类（根据来源）：

- **内置**：即 Django 框架自带的应用，包括 admin（后台管理）、auth（身份鉴权）、sessions（会话管理）等等

- **自定义**：即用来实现我们自身业务逻辑的应用，这里我们将创建一个新闻展示应用

- **第三方**：即社区提供的应用，数量极其丰富，功能涵盖几乎所有方面，能够大大减少开发成本

  1. 注册应用

     ```python
     INSTALLED_APPS = [
         'django.contrib.admin',
         'django.contrib.auth',
         'django.contrib.contenttypes',
         'django.contrib.sessions',
         'django.contrib.messages',
         'django.contrib.staticfiles',
         'NewApp',							#我们创建的app
     ]
     ```

  2. 创建自定义APP

     ```cmd
     python manage.py startapp new			#创建新app名为new
     ```

  3. 全局路由表

     ```python
     from django.contrib import admin
     from django.urls import path, include
     
     urlpatterns = [
         path('admin/', admin.site.urls),
         path('', include('news.urls')),		#添加路由映射
     ]
     ```

### 第二讲、成功打开页面

#### html+url+views三件套

创建Html文件、配置路径、视图定义

```python
from django.http import HttpResponse

def index(request):
    return HttpResponse('Hello World!')		   #页面显示'Hello World!'
```

创建templates 文件夹，下置index.html 页面。（！+tab）

添加全局路径settings.py中：

```python
import os
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, '')],	#添加模板文件路径
        'APP_DIRS': True,
      ...
    },
]
```

urls:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),						#通过url设置对应的映射
]

```

views:

```python
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')
#通过url映射到这个视图函数，该视图函数返回到html页面
```



## 二、前端

### 第一讲、页面分区

#### 1.导航栏+上部分内容+下部分内容

```html
	<!-- 导航栏 -->
    <div style="background-color: #ffffff; padding: 15px 250px;"></div>
    
    <div style="display: flex; flex-direction: column; height: 100vh;">
        <!-- 上部分 -->
      <div style="background-color: rgb(248,247,252); flex: 25%;text-align: center;"></div>
      
      <!-- 下部分 -->
      <div style="background-color: rgb(248,247,252); display: flex; flex-direction: column; flex: 75%;">
        <!-- 下方-----上半部分 -->
        <div style="flex: 50%; display: flex;">
            <!-- 左上分区 -->
            <div style="flex: 50%;"></div>
            <!-- 右上分区 -->
            <div style="flex: 50%;"></div>
        </div>
    
        <!-- 下方-----下半部分 -->
        <div style="flex: 50%; display: flex;">
            <!-- 左下分区 -->
            <div style="flex: 50%;"></div>
            <!-- 右下分区 -->
            <div style="flex: 50%;"></div>
        </div>
      </div>
    </div>

```

#### 2.引入静态资源

settings：

```python
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, '')]
```

html:

```html
{% load static %}
<link  rel="stylesheet" href="{% static 'css/index.css' %}">
```



### 第二讲、js前端获取页面内容并传参

#### 1.获取信息并传递

```javascript
let question = "";//全局变量
function submitQuestion(buttonElement) {
   			const questionInput = document.getElementById('question').value.trim();
            // 将问题赋值给 question 变量
            question = questionInput;

            fetch(`/ask?question=${encodeURIComponent(question)}`)
                .then(response => response.json())
                .then(data => {
                
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
        }
```

#### 2.小细节：

1.去除输入框中内容的前后空格

```javascript
const questionInput = document.getElementById('question').value.trim();
```

2.判空，如果输入框内容为空，不执行操作

```javascript
if (questionInput === "") {
                return; 
            }
```

3.相应时间较长，应避免用户在等待响应时重复点击

```javascript
// 禁用按钮，并更改文本以表示正在加载
            buttonElement.innerText = '正在加载...';
            buttonElement.disabled = true;
            
            。。。
// 恢复按钮状态
            buttonElement.innerText = '开始学习';
            buttonElement.disabled = false;
```

4.前端接收json数据

```javascript
const moduleTitles = [];
const moduleContents = [];
const sectionElement = document.getElementById("mySection");  
for (let i = 0; i < data.length; i++) {
    let moduleTitle = data[i]["模块主题"];
    let moduleContent = data[i]["本模块内容简介"];
    moduleTitles.push(moduleTitle);
    moduleContents.push(moduleContent);
    document.getElementById(`title-box${i + 1}`).innerText = moduleTitle;
    document.getElementById(`content-box${i + 1}`).innerText = moduleContent;
```



## 三、后端

#### 1.接收前端传递参数

```python
question = request.GET.get('question', '')
```

#### 2.调用文心一言大模型

[AI Studio-帮助文档 (baidu.com)](https://ai.baidu.com/ai-doc/AISTUDIO/slmkadt9z)

使用个人的accesstoken,获取文心大模型的api调用

```python
import erniebot
erniebot.api_type = 'aistudio'
erniebot.access_token = "{YOUR-ACCESS-TOKEN}"
```

例：

首先安装文心api包

```cmd
pip install erniebot	
```

然后(推荐)使用jupyter notebook也就是.ipynb文件进行测试**或者**编写.py文件再运行

```python
import erniebot									#引入文心api包
erniebot.api_type = 'aistudio'					#定义使用的令牌的aistudio平台的
erniebot.access_token = "2aXX...XX9"			#引入自己的令牌:https://aistudio.baidu.com/usercenter/token
model = 'ernie-bot'								#定义使用的模型是ernie-bot
message_content ="你好，文心一言"				   #传给文心的文本
messages = [									#将文本和其他参数封装成消息，便于传给文心
    {
        'role': 'user',
        'top_p': '0.001',
        'content': message_content				#传输的文本
    }
]
response = erniebot.ChatCompletion.create(		# 调用文心一言回答问题，下方是相关参数
    model=model,
    messages=messages,
)
answer = response.result						#将回答的文本传给answer变量
print(answer)									#输出查看
```

#### 3.prompt训练

目的：让大模型更好的为我们所用

内容：教导prompt基本原则与现场测试

两个例子：

```
1.我想学习一门课程，内容关于机器学习，请帮我指定一个学习路线，给出4个模块

2. The task scenario is: I need you to refine the knowledge points I provide into four small modules to help me learn.
The best way to refine is to follow a good learning path, and you need to stand from the perspective of a teacher to help me learn the knowledge well. 
对每个模块进行介绍，让读者能够直观的知道该模块的学习内容 我提供的知识点为：机器学习
示例json文件如下，参考它的格式：[{"模块主题": "", "本模块内容简介": ""},]
Strictly follow the format I provided 
每个模块的介绍在30个中文汉字左右。
 The output is just pure JSON format, with no other descriptions.
```

秘诀：

①指定角色

②告诉大模型你是谁，你在哪，你要干什么

③规定格式、需要严格要求的放在prompt最后

④使用中英混合-有些句子大模型对英文理解较好

⑤使用符号，如分点阐述使用-或·，以及<>       

example：

-The task scenario is: I will provide you with the <theme> and <content> that I want to learn. You need to stand from the teacher's perspective to help me learn knowledge well, and according to the <content description>, divide the <content> into five consecutive lesson and return them to me
-我提供的theme为：LightGBM
-我提供的<content>为：参数优化
-我提供的<content description>为：掌握如何调整LightGBM的参数以优化模型性能



## 四、备注

1. button渐变背景色

```
background-image: linear-gradient(87deg,#8748e0,#7870e3,#5e91e5,#21b0e7);
```

2. svg图标路径

```
<svg xmlns="http://www.w3.org/2000/svg" class ="svg2"height="1em" viewBox="0 0 576 512">
                          <style> .svg2{fill:#b197fc;height: 40px;width: 40px;}</style>
                          <path d="M386.539 111.485l15.096 248.955-10.979-.275c-36.232-.824-71.64 8.783-102.657 27.997-31.016-19.214-66.424-27.997-102.657-27.997-45.564 0-82.07 10.705-123.516 27.723L93.117 129.6c28.546-11.803 61.484-18.115 92.226-18.115 41.173 0 73.836 13.175 102.657 42.544 27.723-28.271 59.013-41.721 98.539-42.544zM569.07 448c-25.526 0-47.485-5.215-70.542-15.645-34.31-15.645-69.993-24.978-107.871-24.978-38.977 0-74.934 12.901-102.657 40.623-27.723-27.723-63.68-40.623-102.657-40.623-37.878 0-73.561 9.333-107.871 24.978C55.239 442.236 32.731 448 8.303 448H6.93L49.475 98.859C88.726 76.626 136.486 64 181.775 64 218.83 64 256.984 71.685 288 93.095 319.016 71.685 357.17 64 394.225 64c45.289 0 93.049 12.626 132.3 34.859L569.07 448zm-43.368-44.741l-34.036-280.246c-30.742-13.999-67.248-21.41-101.009-21.41-38.428 0-74.385 12.077-102.657 38.702-28.272-26.625-64.228-38.702-102.657-38.702-33.761 0-70.267 7.411-101.009 21.41L50.298 403.259c47.211-19.487 82.894-33.486 135.045-33.486 37.604 0 70.817 9.606 102.657 29.644 31.84-20.038 65.052-29.644 102.657-29.644 52.151 0 87.834 13.999 135.045 33.486z"/>
 </svg>
```

3. css样式：

```
.carddiy{
    height: 230px;
    width: 60%;
    margin-top: 3%;
    background-color: #fff;
    border: 0.3px solid #ccc;
    border-radius: 10px;
    box-shadow: 0 0.35em 0 #ccc;
    display: flex;
    flex-direction: column;
}
.top{
    border-radius: 8px 8px 0px 0px;
    height: 50px;
    border-bottom: 1px solid #ccc;
    background-color: rgb(24,49,83);
    display: flex;
    justify-content: center;
    align-items: center;
}

.bottom{
    text-align: left;
    padding-left: 10px;
    margin: 0;
    margin-top: 3%;
}

.botm_title{
    font-size: 24px;
    margin: 0;
}
.botm_ph{
    font-size: 15px;
    text-indent: 2em;
    margin-top: 14px;
}

.carddiy:hover {
    box-shadow: 0 0.25em 0 rgb(177, 151, 252);
    border-color: rgb(177,151,252); 
    border-width: 2.3px;
  }
```

4. 设置文心一言的相关参数：

    erniebot.api_type = 'aistudio'
    erniebot.access_token = "2a14e181576d07e3874b914c630c0668410e39a9"
    model = 'ernie-bot'
    
    # 将文本放在单个消息对象中，用空格分隔不同的文本段落
    message_content = 
    messages = [
        {
            'role': 'user',
            'top_p': '0.001',
            'content': message_content
        }
    ]
    # 调用文心一言回答问题
    response = erniebot.ChatCompletion.create(
        model=model,
        messages=messages,
    )
    # 获取文心一言的回答
    answer = response.result

5. prompt：

```
"The task scenario is: I need you to refine the knowledge points I provide into four small modules to help me learn. " \
                    "The best way to refine is to follow a good learning path, and you need to stand from the perspective of a teacher to help me learn the knowledge well. " \
                    f"-对每个模块进行介绍，让读者能够直观的知道该模块的学习内容 我提供的知识点为：{question} " \
                    "-示例json文件如下，参考它的格式：[{\"模块主题\": \"\", \"本模块内容简介\": \"\"},] " \
                    "- Strictly follow the format I provided " \
                    "- 每个模块的介绍在30个中文汉字左右。 " \
                    "- The output is just pure JSON format, with no other descriptions."
```



