from django.conf.urls import url
from django.urls import path, include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers

from books import views


schema_view = get_schema_view(
   openapi.Info(
      title="Work At Olist API",
      default_version='v1',
   ),
   public=True
)

router = routers.DefaultRouter()
router.register(r'authors', views.AuthorViewSet, basename='authors')
router.register(r'books', views.BookViewSet, basename='books')

urlpatterns = [
    path('', include(router.urls)),
    url('docs/', schema_view.with_ui('swagger'))
]
