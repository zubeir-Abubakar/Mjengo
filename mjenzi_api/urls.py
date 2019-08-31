from django.urls import path
from .views import ProjectList, ProjectDetail, MaterialList, UserCreate, ReportList, RequestList, LoginView, home

urlpatterns = [
    path("projects/", ProjectList.as_view(), name="projects_list"),
    path("projects/<int:pk>/", ProjectDetail.as_view(), name="projects_detail"),
    path("projects/<int:pk>/reports/", ReportList.as_view(), name="reports_list"),
    path("projects/<int:pk>/materials/", MaterialList.as_view(), name="materials_list"),
    path("projects/<int:pk>/requests/", RequestList.as_view(), name="create_request"),
    path("sign-up/", UserCreate.as_view(), name="user_create"),
    path("login/", LoginView.as_view(), name="login"),
]
