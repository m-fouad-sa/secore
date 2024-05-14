from django.urls import path

from .views import *

urlpatterns = [
    path("projects/", ProjectList.as_view()),
    path("projects/<str:id>/", ProjectDetail.as_view()),
    path("status/", StatusList.as_view()),
    path("status/<str:id>/", StatusDetail.as_view()),
    path("sector/", SectorList.as_view()),
    path("sector/<str:id>/", SectorDetail.as_view()),
    path("attachment/", AttachmentList.as_view()),
    path("attachment/<str:id>/", AttachmentDetail.as_view()),
    path("client/", ClientList.as_view()),
    path("client/<str:id>/", ClientDetail.as_view()),
]
