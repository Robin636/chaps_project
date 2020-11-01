from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views


urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(), name='logout', kwargs={'next_page': '/'}),
    path('', include('chaps.urls')),
]
