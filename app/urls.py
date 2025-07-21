from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm,MyPasswordResetForm,MySetPasswordForm
urlpatterns = [
# Home Panel URL
    path('', views.ProductView.as_view(), name='home'),

# Product View URL
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
# Cart URL
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
# Plus and Minus Remove Cart URL
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='removecart'),
    path('removecart/', views.remove_cart, name='removecart'),
# buy now URL
    path('buy/', views.buy_now, name='buy-now'),
# Profile URL
    path('profile/', views.ProfileView.as_view(), name='profile'),
# Address URL
    path('address/', views.address, name='address'),
# Order URL
    path('orders/', views.orders, name='orders'),
# Mobile URL
    path('mobile/', views.mobile, name='mobile'),
# Mobile URL with slug
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
# Laptop URL
    path('laptop/', views.laptop, name='laptop'),
# Laptop URL with slug
    path('laptop/<slug:data>', views.laptop, name='laptopdata'),
# Top Wear URL
    path('top/', views.top, name='top'),
# Top Wear URL with slug
    path('top/<slug:data>', views.top, name='topdata'),
# Bottom Wear URL
    path('bottom/', views.bottom, name='bottom'),
# Bottom Wear URL with slug
    path('bottom/<slug:data>', views.bottom, name='bottomdata'),
# Checkout URL
    path('checkout/', views.checkout, name='checkout'),
# Payment URL
    path('paymentdone/', views.payment_done, name='paymentdone'),
# Authentication URLs
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm), name='login'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/Done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordChange.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('passwordchangedone/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# path('', views.home),
 # path('login/', views.login, name='login'),
# path('registration/', views.customerregistration, name='customerregistration'),
# path('profile/', views.profile, name='profile')
 # path('changepassword/', views.change_password, name='changepassword'),
