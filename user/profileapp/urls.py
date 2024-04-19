from django.urls import path, re_path
from .views import RegisterView, LoginView, UserView, LogoutView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="Detailed documentation of API endpoints",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('profile', UserView.as_view()),
    path ('logout', LogoutView.as_view()),

 # URLs for the Swagger documentation
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

