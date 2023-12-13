from django.urls import path, include
from .views import *

urlpatterns = [
    path('api/', include('vendor_app.api.urls'))
    
    
    
]
