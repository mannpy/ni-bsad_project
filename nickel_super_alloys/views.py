from django.shortcuts import render
from django.views.generic import ListView, DetailView
from pure_pagination.mixins import PaginationMixin
from .models import Alloy, AlloyingElement

ORDER_VAR = 'o'
SEARCH_VAR = 'q'
ORDER_VARS = {'1': 'name', '2': 'type_of_alloy', '3': 'type_of_structure'}


class IndexList(PaginationMixin, ListView):
    model = Alloy
    context_object_name = 'alloys'
    paginate_by = 50
    template_name = "nickel_super_alloys/index.html"

    def get_queryset(self):
        params = dict(self.request.GET.items())
        queryset = Alloy.objects.all()
        self.query = self.request.GET.get(SEARCH_VAR, '')
        if self.query:
            queryset = queryset.filter(name__icontains=params[SEARCH_VAR])
        self.ordering_links = {str(k): ["?o=%s" % k] for k in range(1,4)}
        if ORDER_VAR in params:
            # составляю список для сортировки
            ordering = []
            # список из параметров сортировки
            order_params = params[ORDER_VAR].split('.')
            # делаю меняющиеся ссылки
            ordering_links = {str(k): ["", "", ""] for k in range(1,4)}
            for p in order_params:
                try:
                    none, pfx, idx = p.rpartition('-')
                    for key in ordering_links:
                        not_first_1 = "." if ordering_links[key][0] else "?o="
                        not_first_2 = "." if ordering_links[key][1] else "?o="
                        if idx == key:
                            if pfx:
                                ordering_links[key][0] += (not_first_1 + idx)
                                ordering_links[key][2] = 'desc'
                            else:
                                ordering_links[key][0] += (not_first_1 + "-" + idx)
                                ordering_links[key][2] = 'asc'
                        else:
                            ordering_links[key][0] += (not_first_1 + pfx + idx)
                            ordering_links[key][1] += (not_first_2 + pfx + idx)
                        if key not in params[ORDER_VAR]:
                            ordering_links[key][0] = "?o=%s.%s" % (params[ORDER_VAR], key)
                            ordering_links[key][1] = ""


                    ordering.append(pfx + ORDER_VARS[idx])
                except (IndexError, ValueError):
                    continue
            self.ordering_links = ordering_links
            queryset = queryset.order_by(*ordering)
        self.count = queryset.count()
        return queryset


    def get_context_data(self, **kwargs):
        context = super(IndexList, self).get_context_data(**kwargs)
        context['alloys_count'] = self.count
        elements = []
        for el in AlloyingElement.objects.all():
            if el.element not in elements:
                elements.append(el.element)
        context['elements'] = elements
        context['query'] = self.query
        if self.query:
            context['query_link'] = "&q=" + self.query
        if self.ordering_links:
            context['links'] = sorted(self.ordering_links.items())
        return context

class AlloyDetail(DetailView):
    model = Alloy
    context_object_name = 'alloy'
    template_name = "nickel_super_alloys/alloy-detail.html"
