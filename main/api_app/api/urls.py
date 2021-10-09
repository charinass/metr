from django.urls import path
from api_app.api.views import commit, export


urlpatterns = [
    path('commit/', commit),
    path('commit', commit, name='commit'),
    path('export', export, name='export'),
]