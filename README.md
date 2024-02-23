# online_marketplace

跟著Youtube頻道[freeCodeCamp.org](https://www.youtube.com/watch?v=ZxMB6Njs3ck&list=PLEfmhkMT7yZiVXuExfXWd5pYWutdasC5r&index=1&t=931s)實做練習

### 疑問

- 為何LoginForm不需要在views.py中宣告？

# 學習筆記

### Forms流程

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
def signup(response):
    if response.method == 'POST':
        form = SignupForm(response.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()
    
    return render(response, 'core/signup.html', {'form':form})
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



### 設定Login Logout url

在主app中開啟settings.py並加入以下

```python
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL='/'
LOGOUT_REDIRECT_URL='/'
```

`LOGIN_URL`為登入頁面的網址，`LOGIN_REDIRECT_URL`為登入後的重新導向網址，`LOGOUT_REDIRECT_URL='/'`為都出後所重新導向的網址

### URL設定

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

**html中操作網址用法**

```html
<a href="{% url 'core:contact' %}" class="text-teal-500 hover:text-teal-700">Contact</a>
```

`{% url 'core:contact' %}`中core為該url所屬的app_name,contact為path中所取的別名,點擊Contact後就會跳轉到該url

