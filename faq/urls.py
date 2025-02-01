from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_faq, name='create_faq'), 
    path('<int:id>/update/', views.update_faq, name='update_faq'),  
    path('', views.get_all_faqs, name='get_all_faqs'), 
    path('<int:id>/delete/', views.delete_faq, name='delete_faq'),
    path('language/<str:lang>/', views.get_faqs_by_language, name='get_faqs_by_language'), 
    path('<int:id>/language/<str:lang>/', views.get_faq_by_language, name='get_faq_by_language'),
]
