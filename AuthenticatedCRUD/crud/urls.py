from django.urls import path
from . import views


app_name = 'crud'

urlpatterns = [
    path('', views.index, name='index' ),
    path('create/', views.create, name='create' ),
    path('add_client/', views.add_client, name='add_client' ),
    path('delete/<id>/', views.delete, name='delete' ),
    path('edit/<id>/', views.edit, name='edit' ),
    path('update/<id>/', views.update, name='update' ),
    path('gallery/', views.gallery, name='gallery'),

    path('signup/',views.signup,name='signup'),
    path('login_user/',views.login_user,name='login_user'),
    path('logout_user/',views.logout_user,name='logout_user'),
    path('search/', views.search, name='search'),

    #account register confirmations
    # path('activate/<str:uid>/<str:token>', views.activate, name='activate'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),




]
