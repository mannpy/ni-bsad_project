from django.shortcuts import render
from django.views.generic import ListView, DetailView
from pure_pagination.mixins import PaginationMixin
from .models import Alloy

class IndexList(PaginationMixin, ListView):
    model = Alloy
    context_object_name = 'alloys'
    paginate_by = 50
    template_name = "nickel_super_alloys/index.html"

class AlloyDetail(DetailView):
    model = Alloy
    context_object_name = 'alloy'
    template_name = "nickel_super_alloys/alloy-detail.html"
