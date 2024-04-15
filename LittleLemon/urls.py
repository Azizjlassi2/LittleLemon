
from django.contrib import admin
from django.urls import path ,include
from rest_framework_simplejwt.views import TokenRefreshView ,TokenObtainPairView, TokenBlacklistView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/",include("LittleLemonApi.urls")),
    path("auth/",include('djoser.urls')),
    path("auth/",include('djoser.urls.authtoken')),
    path("api/token/",TokenObtainPairView.as_view(),name="token_obtain_view"),
    path("api/token/refresh/",TokenRefreshView.as_view(),name="token_refresh"),
    path("api/token/blacklist/",TokenBlacklistView.as_view(),name="token_blacklist"),

]
