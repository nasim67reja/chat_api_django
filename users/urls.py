from django.urls import path
from .api_views import SignupView, SigninView, UserDetailView,CustomTokenRefreshView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('signin/', SigninView.as_view(), name='signin'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('refresh_token', CustomTokenRefreshView.as_view(), name='token_refresh'),  # Refresh token endpoint
]
