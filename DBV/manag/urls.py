from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'dashboard'

urlpatterns = [
    # path('home', views.index, name="index"),
    path('dashboard', views.dashboard, name='dashboard'),
    path('data/', views.dashboard_data, name='data'),
    path('products/', views.product_list_data, name='products') #for search listing
]
# Static media files configuration for development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)