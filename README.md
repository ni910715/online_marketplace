# online_marketplace

跟著Youtube頻道[freeCodeCamp.org](https://www.youtube.com/watch?v=ZxMB6Njs3ck&list=PLEfmhkMT7yZiVXuExfXWd5pYWutdasC5r&index=1&t=931s)實做練習

## 疑問

- 為何LoginForm不需要在views.py中宣告？

# 學習筆記

## Forms流程

**創建forms.py (SignupForm)**

```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    username = forms.CharField(widget=forms.TextInput(attrs={
		...
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        ...
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        ...
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        ...
    }))
```

**新增到views**

``` python
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()
    
    return render(request, 'core/signup.html', {'form':form})
```

**新增HTML模板**

```html
{% extends 'core/base.html' %}

{% block title %}Sign Up{% endblock %}

{% block content %}
<div class="w-1/2 my-6 mx-auto p-6 bg-gray-100 rounded-xl">
<h1 class="mb-6 text-3xl">Sign up</h1>

    <form method="post" action=".">
        {% csrf_token %}
        
        <div class="mb-3">
            <label class="inline-block mb-3">Username</label><br>
            {{ form.username }}
        </div>

        <div class="mb-3">
            <label class="inline-block mb-3">Email</label><br>
            {{ form.email }}
        </div>

        <div class="mb-3">
            <label class="inline-block mb-3">Password</label><br>
            {{ form.password1 }}
        </div>

        <div class="mb-3">
            <label class="inline-block mb-3">Repeat password</label><br>
            {{ form.password2 }}
        </div>

        {% if form.errors or form.non_field_errors %}
            <div class="mb-3 p-6 bg-red-100 rounded-xl">
                {% for field in form %}
                    {{ form.errors }}
                {% endfor %}
                {{ form.non_field_errors }}
            </div>
        {% endif %}

        <button class="py-4 px-8 text-lg bg-teal-500 hover:bg-teal-700 rounded-xl text-white">Submit</button>
    </form>
</div>
{% endblock%}
```

**在forms.py 新增LoginForm**

導入Django的AuthenticationForm

```python
from django.contrib.auth.forms import AuthenticationForm
```

新增LoginForm並繼承AuthenticationForm

```python
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        ... ＃樣式
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        ... ＃樣式
    }))
```

**到urls.py新增path**

由於將直接使用django所提供的表單所以跳過在views進行設定，並且導入

```python
from django.contrib.auth import views as auth_views
from .forms import LoginForm
```

**加入login的url**

```python
path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
```

因為沒有在views中定義使用的html所以在這裡需要設定`template_name=' '`

**新增login.html**

```python
{% extends 'core/base.html' %}

{% block title %}Log in{% endblock %}

{% block content %}
<div class="w-1/2 my-6 mx-auto p-6 bg-gray-100 rounded-xl">
<h1 class="mb-6 text-3xl">Log in</h1>

    <form method="post" action=".">
        {% csrf_token %}
        
        <div class="mb-3">
            <label class="inline-block mb-3">Username</label><br>
            {{ form.username }}
        </div>

        <div class="mb-3">
            <label class="inline-block mb-3">Password</label><br>
            {{ form.password }}
        </div>

        {% if form.errors or form.non_field_errors %}
            <div class="mb-3 p-6 bg-red-100 rounded-xl">
                {% for field in form %}
                    {{ form.errors }}
                {% endfor %}
                {{ form.non_field_errors }}
            </div>
        {% endif %}

        <button class="py-4 px-8 text-lg bg-teal-500 hover:bg-teal-700 rounded-xl text-white">Submit</button>
    </form>
</div>
{% endblock%}
```

雖然沒有在views中定義操作表單所使用的變數，但django預設為form

**當登入成功後改變base.html的按鈕**

表示為當入狀態

```python
{% if request.user.is_authenticated %}
                    <a href="#" class="px-6 py-3 text-lg font-semiblod bg-teal-500 text-white rounded-xl hover:bg-teal-700">Inbox</a>
                    <a href="#" class="px-6 py-3 text-lg font-semiblod bg-gray-500 text-white rounded-xl hover:bg-gray-700">Dashboard</a>
                {% else %}
                    <a href="{% url 'core:signup' %}" class="px-6 py-3 text-lg font-semiblod bg-teal-500 text-white rounded-xl hover:bg-teal-700">Sign up</a>
                    <a href="{% url 'core:login' %}" class="px-6 py-3 text-lg font-semiblod bg-gray-500 text-white rounded-xl hover:bg-gray-700">Log in</a>
                {% endif%}
```
### HTML form參數
`enctype="multipart/form-data"`代表可以上傳圖片
### Forms styling的方式
```python
class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Your username',
        'class':'w-full py-4 px-6 rounded-xl'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder':'Your email address',
        'class':'w-full py-4 px-6 rounded-xl'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Your password',
        'class':'w-full py-4 px-6 rounded-xl'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Repeat password',
        'class':'w-full py-4 px-6 rounded-xl'
    }))
```
```python
INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'
class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('category', 'name', 'description', 'price', 'image',)
        widgets = {
            'category':forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'name':forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description':forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'price':forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image':forms.FileInput(attrs={
                'class': INPUT_CLASSES
            })
        }
```
### 表單初始化
```python
@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, create_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)
        print(form)
        
        if form.is_valid():
            form.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)
    return render(request, 'item/form.html', {'form':form, 'title':'Edit Item'})
```
`instance=item`告訴表單以該item內容為初始化
### Search
**browse**
```html
<div class="col-span-1">
    <form method="get" action="{% url 'item:browse' %}">
        <input name="query" class="w-full py-4 px-6 border rounded-xl" type="text" value="{{query}}" placeholder="Find a bike, a chair or a car...">

        <button class="mt-2 py-2 px-8 text-lg bg-teal-500 text-white rounded-xl">Search</button>
    </form>

    <hr class="my-6">
    <p class="font-semiblod">Categories</p>
    <ul>
        {% for category in categories %}
        <li class="py-2 px-2 rounded-xl {% if category.id == category_id %}bg-gray-200{% endif %}">
            <a href="{% url 'item:browse' %}?query={{query}}&category={{category.id}}">{{category.name}}</a>
        </li>
        {% endfor %}
    </ul>

    <hr class="my-6">
    <p class="font-semiblod">Clear filters</p>

    <ul>
        <li>
            <a href="{% url 'item:browse' %}" class="mt-2 py-4 px-8 inline-block bg-yellow-500 text-lg rounded-xl text-white">Clear</a>
        </li>
    </ul>

</div>
```
`value=" "`為input元素的初始值  
`?query={{query}}&category={{category.id}}`可以在網址中插入額外的搜尋網址  
**views**
```python
def browse(request):
    query = request.GET.get('query', '')
    category_id =request.GET.get('category', 0)
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'item/browse.html', {'items':items, 'query':query, 'categories':categories, 'category_id':int(category_id)})
```
```python
from django.db.models import Q
```
`Q`模組提供複雜查詢方法，可同時查詢符合多個條件的項目  
`name__icontains=query`將模型Item中的name與query參數做不區分大小寫的**模糊過濾**
## Method
```python
if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        print(form)
        
        if form.is_valid():
            item = form.save(commit=False)
            item.create_by = request.user
            item.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()
```
`request.POST`收取文字  
`request.FILES`因為有在form中使用圖檔
## 設定Login Logout url

在主app中開啟settings.py並加入以下

```python
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL='/'
LOGOUT_REDIRECT_URL='/'
```

`LOGIN_URL`為登入頁面的網址  
`LOGIN_REDIRECT_URL`為登入後的重新導向網址 `LOGOUT_REDIRECT_URL='/'`為都出後所重新導向的網址  

## URL設定

**在新創見的app中加入urls.py**

```python
from django.urls import path
from . import views

app_name = 'item'

urlpatterns = [
    path('<int:pk>/', views.detail, name='detail'),
]
```

`<int:pk>/`int表示數字pk為item中的id

**在主app中的urls.py註冊這個app的url**

需要從django.urls導入include

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('core.urls')),
    path('item/', include('item.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

`path('item/', include('item.urls')),`所有由item所產生的url都會在`item/`之後

### Html中操作網址用法

```html
<a href="{% url 'core:contact' %}" class="text-teal-500 hover:text-teal-700">Contact</a>
```

`{% url 'core:contact' %}`中core為該url所屬的app_name,contact為path中所取的別名,點擊Contact後就會跳轉到該url

## Decorators
導入
```python
from django.contrib.auth.decorators import login_required
```
**login_required**:只有在登入過後才能進入，否則重新導向login page  
Example:
```python
@login_required
def new(request):
    form = NewItemForm()
    return render(request, 'item/form.html', {'form':form, 'title':'New Item'})
```
## Models
### Create
```python
class Conversation(models.Model):
    item = models.ForeignKey(Item, related_name='conversations', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class  Meta:
        ordering = ('-modified_at',)
```
`DateTimeField`紀錄日期+時間，另有`DateField`和`TimeField`  
`auto_now_add`用於記錄創建當下得時間戳記  
`auto_now`用於記錄並更新每次儲存時的時間戳記  
`ordering`排序方式
### 在view中操作資料庫
```python
items = Item.objects.filter(create_by=request.user)
```
查找所有使用者所建立的物件   