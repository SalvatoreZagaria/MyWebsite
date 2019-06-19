from django.urls import path
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('downloadCV', views.download, name='download_cv'),
    #path('contact', views.send_email, name='send_email')
]
