from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from . import views
from .views import AnimalView, AnimalGetView

# app_name will help us do a reverse look-up later
app_name = 'animals'


urlpatterns = [ 

    path('', views.homeView, name='home'),
    path('all/', views.viewAll, name='terms'),
    path('all/', views.viewAll, name='all'),
    path('all/<str:pk>/', views.viewDetail, name='detail'),
    path('accounts/login/', views.loginUser, name="login"),
    path('accounts/changepw/', views.changePW, name="changepw"),
    path('logout/', views.logoutUser, name="logout"),    

    path('api/animals/all', AnimalView.as_view(), name='add'),
    path('api/animals/all/<int:pk>', AnimalView.as_view()),
    path('api/animals/all/<str:name>', AnimalGetView.as_view()),

    
    # path('api/animals/add/', views.addAnimal, name="add"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
