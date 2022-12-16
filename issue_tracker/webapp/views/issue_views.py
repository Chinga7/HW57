from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.http import urlencode
from webapp.models import Issue, Project
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from webapp.forms import IssueForm, SearchForm
from webapp.views.base_views import CustomSearchView


class IssueListView(ListView):
    template_name = 'issues/list.html'
    model = Issue
    context_object_name = 'issues'
    ordering = ('-created_at')
    paginate_by = 3
    paginate_orphans = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_deleted=False)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = SearchForm
        return context


class SearchView(CustomSearchView):

    template_name = 'issues/list.html'
    model = Issue
    search_form = SearchForm
    context_object_name = 'issues'
    ordering = ('-created_at')
    paginate_by = 3
    paginate_orphans = 2

    def get_queryset(self):
        if self.search_value:
            queryset = super().get_queryset()
            queryset = queryset.filter(Q(summary__icontains=self.search_value) | Q(description__icontains=self.search_value))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
            context['search'] = self.search_value
        return context


class IssueView(DetailView):
    template_name = 'issues/detail.html'
    model = Issue


class CreateIssueView(LoginRequiredMixin, CreateView):
    template_name = "issues/create.html"
    model = Issue
    form_class = IssueForm

    def form_valid(self, form):
        project = (get_object_or_404(Project, pk=self.kwargs.get('pk')))
        issue = form.save(commit=False)
        issue.project = project
        issue.save()
        return redirect('project_detail', pk=project.pk)


class UpdateIssueView(LoginRequiredMixin, UpdateView):
    template_name = 'issues/update.html'
    form_class = IssueForm
    model = Issue
    context_object_name = 'issue'


class DeleteIssueView(LoginRequiredMixin, DeleteView):
    template_name = 'issues/delete.html'
    model = Issue
    context_object_name = 'issue'
    success_url = reverse_lazy('project_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.is_deleted = True
        self.object.save()
        return HttpResponseRedirect(success_url)