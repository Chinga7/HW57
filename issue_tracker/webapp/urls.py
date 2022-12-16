from django.urls import path
from webapp.views import ProjectView, CreateProjectView, ProjectDetailView, UpdateProjectView, DeleteProjectView, \
    IssueListView, IssueView, CreateIssueView, UpdateIssueView, DeleteIssueView \

app_name = 'webapp'

urlpatterns = [
    # Project urls
    path('', ProjectView.as_view(), name='project_list'),
    path('project/create/', CreateProjectView.as_view(), name='create_project'),
    path('project/detail/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('project/update/<int:pk>/', UpdateProjectView.as_view(), name='update_project'),
    path('project/delete/<int:pk>/', DeleteProjectView.as_view(), name='delete_project'),

    # Issue urls
    path('issue/list/', IssueListView.as_view(), name='issue_list'),
    path('issue/detail/<int:pk>/', IssueView.as_view(), name='issue_detail'),
    path('issue/create/<int:pk>', CreateIssueView.as_view(), name='create_issue'),
    path('issue/update/<int:pk>/', UpdateIssueView.as_view(), name='update_issue'),
    path('issue/delete/<int:pk>/', DeleteIssueView.as_view(), name='delete_issue'),
]