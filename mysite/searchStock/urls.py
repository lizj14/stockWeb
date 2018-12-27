from django.conf.urls import url
from searchStock import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^predict',views.predict),
    

]