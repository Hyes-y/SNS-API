from django.urls import path, include

urlpatterns = [
    path('account/', include('apps.account.urls')),
    path('posts/', include('apps.post.urls')),
]