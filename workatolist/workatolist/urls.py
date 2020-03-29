from django.conf.urls import url
from django.urls import path, include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
   openapi.Info(
      title="Work At Olist API",
      default_version='v1',
   ),
   public=True
)

urlpatterns = [
    path('', include('books.urls')),
    url('docs/', schema_view.with_ui('swagger'))
]
