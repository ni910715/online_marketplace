# online_marketplace
跟著Youtube頻道[freeCodeCamp.org](https://www.youtube.com/watch?v=ZxMB6Njs3ck&list=PLEfmhkMT7yZiVXuExfXWd5pYWutdasC5r&index=1&t=931s)實做練習

### Forms流程

---

##### 創建forms.py

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

##### 新增到views

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

##### 新增HTML模板

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

### URL設定

---

##### 在新創見的app中加入urls.py

```python
from django.urls import path
from . import views

app_name = 'item'

urlpatterns = [
    path('<int:pk>/', views.detail, name='detail'),
]
```

`<int:pk>/`int表示數字pk為item中的id

##### 在主app中的urls.py註冊這個app的url

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

