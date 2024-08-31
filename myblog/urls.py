from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [

path('',Homeview.as_view(),name='home'),
path('category_posts/<int:pk>/',Postview.as_view(),name="category_posts"),
path('create_post',PostCreateview.as_view(),name='create_post'),
path('post_detail/<int:pk>/',PostDetailview.as_view(),name='post_detail'),
path('update_post/<int:pk>/',PostEditview.as_view(),name='update_post'),
path('delete_post/<int:pk>/',Deletepostview.as_view(),name='delete_post'),
path('show_comment/<int:pk>/',Commentview.as_view(),name='show_comment'),
path('comment_like/<int:pk>/',commentlikeview.as_view(),name='comment_like'),
path('edit_comment/<int:pk>/',Editcommentview.as_view(),name='edit_comment'),
path('delete_comment/<int:pk>/',Deletecommentview.as_view(),name='delete_comment'),
path('reply_comment/<int:pk>/',ReplyCommentView.as_view(),name='reply_comment'),
path('post_like/<int:pk>/',Postlikeview.as_view(),name='post_like'),
path('login/',Myloginview.as_view(),name='login'),
path('register/',MyuserSingnupview.as_view(),name='register'),
path('all_profiles/',ProfileAllview.as_view(),name='all_profiles'),
path('user_profile/<int:pk>/',ShowProfileView.as_view(),name="user_profile"),
path('edit_profile/<int:pk>/',EditProfileView.as_view(),name="edit_profile"),
path('update_email/<int:pk>/',UpdateEmailView.as_view(),name='update_email'),
path('user_logout/',Mylogoutview.as_view(),name="user_logout"),
path('follow_user/<int:pk>/',UserFollowview.as_view(),name='follow_user'),
path('list_followers/',Myfollowerview.as_view(),name='list_followers'),
path('list_follows/',Myfollowview.as_view(),name='list_follows'),
path('change_password/',CustompasswordchangeView.as_view(),name='change_password'),
path('add_category/',AddCategoryView.as_view(),name='add_category'),

path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
path('forbidden_access',forbidden_access.as_view(),name='forbidden_access'),
path('about_us',Aboutview.as_view(),name='about_us'),
path('privacy/',Privacyview.as_view(),name='privacy'),
path('terms/',Termsview.as_view(),name='terms'),
path('contact/',ContactMessageView.as_view(),name='contact'),
path('show_messages/',ShowmessageView.as_view(),name='show_messages'),

path('account_activation/<uidb64>/<token>', views.account_activation, name='account_activation'),

 
]