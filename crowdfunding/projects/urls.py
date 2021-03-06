from django.urls  import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('projects/', views.ProjectList.as_view()),
    path('projects/<int:pk>', views.ProjectDetail.as_view()),
    path('projects/<int:pk>/comment/', views.CommentList.as_view()),
    path('pledges/', views.PledgesList.as_view()),
    path('pledges/<int:pk>', views.PledgesDetail.as_view()),
    path('categories/', views.CategoryList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)