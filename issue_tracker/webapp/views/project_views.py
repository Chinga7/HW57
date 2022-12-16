from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic.list import MultipleObjectMixin
from django.utils.http import urlencode
from webapp.models import Project
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from webapp.forms import ProjectForm, SearchForm


class ProjectView(ListView):
    template_name = 'projects/list.html'
    model = Project
    context_object_name = 'projects'
    paginate_by = 3
    paginate_orphans = 1

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            queryset = queryset.filter(Q(title__icontains=self.search_value) | Q(description__icontains=self.search_value))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
            context['search'] = self.search_value
        return context


class ProjectDetailView(DetailView, MultipleObjectMixin):
    template_name = 'projects/detail.html'
    model = Project
    paginate_by = 3
    # context_object_name = 'issues'

    def get_context_data(self, **kwargs):
        project = self.object
        issues = project.issues.filter(is_deleted=False).order_by('-created_at')
        context = super(ProjectDetailView, self).get_context_data(object_list=issues, **kwargs)
        return context


class CreateProjectView(LoginRequiredMixin, CreateView):
    template_name = "projects/create.html"
    model = Project
    form_class = ProjectForm


class UpdateProjectView(LoginRequiredMixin, UpdateView):
    template_name = 'projects/update.html'
    form_class = ProjectForm
    model = Project
    context_object_name = 'project'


class DeleteProjectView(LoginRequiredMixin, DeleteView):
    template_name = 'projects/delete.html'
    model = Project
    context_object_name = 'project'
    success_url = reverse_lazy('project_list')