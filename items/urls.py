from django.urls import path
from . import views
app_name = 'items'

urlpatterns = [
    path('new/',views.newItem,name='newItem'),
    path('',views.items,name='items'),
    path('edit/<int:pk>',views.edit,name='edit'),
    path('delete/<int:pk>',views.delete,name='delete'),
    path('<int:pk>/',views.detail_view,name='detail')
]