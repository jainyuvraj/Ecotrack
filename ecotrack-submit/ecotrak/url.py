from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index, name='index'),
    path('report',views.report_form,name='report'),
    path('login',views.user_login,name='login'),
    path('sign_up',views.sign_up,name='sign_up'),
    path('logout',views.user_logout,name='logout'),
    path('user_dashboard',views.user_dashboard,name='user_dashboard'),
    path('staff_dashboard',views.staff_dashboard,name='staff_dashboard'),
    path('feedback',views.feedback,name='feedback'),
    path('logindex',views.logindex,name='logindex'),
    path('verify_otp/<int:user_id>/', views.verify_otp, name='verify_otp'),
    path('submit-report/', views.submit_report, name='submit_report'),
    path('chatbot',views.chatbot,name='chatbot'),
    path('submit/', views.submit_feedback, name='submit_feedback'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)