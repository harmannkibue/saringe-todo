from django.conf.urls import url
from .views import ListCreateUsers, ChangePassword, ForgotPasssword,\
    ResetPasswordView, RequestCodeApiView, UserRetrieveUpdateDestroy,\
    RetrieveUpdateUserProfile, \
    UserUpdateProfilePicture, VerifyAccountView

urlpatterns = [
    url(r'^register/$', ListCreateUsers.as_view(), name="list_register_user"),
    url(r'^change-password/$', ChangePassword.as_view(), name="change_password"),
    url(r'^forgot-password/$', ForgotPasssword.as_view(), name="forgot_password"),
    url(r'^reset-password/$', ResetPasswordView.as_view(), name="reset_password"),
    url(r'^request-code/$', RequestCodeApiView.as_view(), name="request_code"),
    url(r'^profile/$', RetrieveUpdateUserProfile.as_view(), name="user_profile"),
    url(r'^profile-photo/$', UserUpdateProfilePicture.as_view(), name="profile_photo"),
    url(r'^(?P<id>[0-9]+)/?$', UserRetrieveUpdateDestroy.as_view(), name="user_retrieve_update_destroy"),
    url(r'^verify-account/', VerifyAccountView.as_view(), name="verify-account"),
]
