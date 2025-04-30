from django.urls import path, re_path
from . import views
from django.conf import settings
from django.views.static import serve

app_name = 'cryptoriseapp'
urlpatterns = [
   path('', views.home, name='home page'),
   path('about/', views.about, name='about page'),
   path('faq/', views.faq, name='faq page'),
   path('login/', views.userlogin, name='login page'),
   path('register/', views.useregister, name='register page'),
   path('dashboard/', views.dashboard, name='dashboard page'),
   path('deposite/', views.deposite, name='deposiet page'),
   path('asset/withdraw', views.withdraw, name='withdraw asset'),
   path('history/transactions', views.history, name='transaction history'),
   path('referral/', views.referral, name='referral page'),
   path('account/settings', views.setting, name='user account setting'),
   path('plan/selection/<plantype>=<price>', views.planpay, name=' plan payment'),
   path('place/withdrawal', views.place_with, name='place withdrawal'),
   
   # ajax controls
   
   path('place_invest/', views.sub_plan, name='new investment'),
   path('update_img/', views.add_img, name='image update action'),
   path('update_profile/', views.update_pro, name='update profile'),
   path('update_pass/', views.update_pass, name='udate password'),
   path('new_user/', views.user_register, name='new user registration'),
   path('log_user/', views.login_user, name='user lofin'),
   path('delete_account/', views.deleteuser, name='delete user account'),
   path('logout/', views.userlogout, name='user logout'),
   path('conf_deposite/', views.comfirm_d, name='confirm deposite'),
   path('place_with/', views.place_wit, name='place withdrawal'),
   
]

urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]