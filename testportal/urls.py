from django.contrib import admin
from django.urls import path, include

from users.views import SignUpView

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', auth_views.LoginView.as_view(
        redirect_authenticated_user=True,
        template_name='auth/login.html'
    )
         ),
    path('admin/', admin.site.urls),
    path('register/', SignUpView.as_view(), name="register"),
    path('login/', auth_views.LoginView.as_view(
        redirect_authenticated_user=True,
        template_name='auth/login.html'
    ),
         name='login'
         ),
    path('users/', include("users.urls")),
    path('tests/', include("tests.urls")),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='login'
    ),
         name='logout'
         ),
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='auth/change-password.html',
            success_url='/'
        ),
        name='change-password'
    ),

    # Forget Password
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='auth/password-reset/password_reset.html',
             subject_template_name='auth/password-reset/password_reset_subject.txt',
             email_template_name='auth/password-reset/password_reset_email.html',
             # success_url='/login/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='auth/password-reset/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='auth/password-reset/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='auth/password-reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path('oauth/', include('social_django.urls', namespace='social')),

]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)