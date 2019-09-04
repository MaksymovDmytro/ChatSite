from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from .views import ThreadView, ThreadsView


app_name = 'chat_app'
redirect_url = '/accounts/login'

urlpatterns = [
    path('', login_required(ThreadsView.as_view()), name='list_threads'),
    re_path(r'^(?P<username>[\w.@+-]+)/$', login_required(ThreadView.as_view()), name='chat_thread'),
]
