from django.shortcuts import render
from django.views.generic import ListView, DetailView
from pure_pagination.mixins import PaginationMixin
from .models import Alloy, AlloyingElement

ORDER_VAR = 'o'
SEARCH_VAR = 'q'
ORDER_VARS = {'1': 'name', '2': 'type_of_alloy', '3': 'type_of_structure'}

# функция для перевода диапазана фильтра из строкового формата в вещественный
def float_num(s, lte=False):
    try:
        s = float(s)
    except ValueError:
        if lte:
            return 100
        return 0
    return s


class IndexList(PaginationMixin, ListView):
    model = Alloy
    context_object_name = 'alloys'
    paginate_by = 50
    template_name = "nickel_super_alloys/index.html"

    def get_queryset(self):
        # параметры запроса Get
        params = dict(self.request.GET.items())
        # запрос - все сплавы
        queryset = Alloy.objects.all()
        self.query = params.get(SEARCH_VAR, '')
        # марка сплава
        if self.query:
            queryset = queryset.filter(name__icontains=self.query)
        self.toa = params.get('ta', '')
        # тип сплава
        if self.toa:
            queryset = queryset.filter(type_of_alloy__startswith=self.toa)
        self.ordering_links = {str(k): ["?o=%s" % k] for k in range(1,4)}
        # Фильтры
        # первый фильтр
        f1 = {'ltf1': float_num(params.get('ltf1', ''), lte=True),
            'f1': params.get('f1', ''), 'gtf1': float_num(params.get('gtf1', ''))}
        # второй фильтр
        f2 = {'ltf2': float_num(params.get('ltf2', ''), lte=True),
            'f2': params.get('f2', ''), 'gtf2': float_num(params.get('gtf2', ''))}
        # третий фильтр
        f3 = {'ltf3': float_num(params.get('ltf3', ''), lte=True),
            'f3': params.get('f3', ''), 'gtf3': float_num(params.get('gtf3', ''))}
        if f1['f1']:
            queryset = queryset.filter(alloyingelement__element__exact=f1['f1'],
                alloyingelement__value__gt=f1['gtf1'], alloyingelement__value__lte=f1['ltf1'])
        if f2['f2']:
            queryset = queryset.filter(alloyingelement__element__exact=f2['f2'],
                alloyingelement__value__gt=f2['gtf2'], alloyingelement__value__lte=f2['ltf2'])
        if f3['f3']:
            queryset = queryset.filter(alloyingelement__element__exact=f3['f3'],
                alloyingelement__value__gt=f3['gtf3'], alloyingelement__value__lte=f3['ltf3'])
        # формируем ссылку url для фильтров
        self.filter_link = ""
        for filt in (f1, f2, f3):
            for key, value in filt.items():
                if value and value not in (0, 100):
                    self.filter_link += "&%s=%s" % (key, value)
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
        type_of_alloys = []
        for alloy in Alloy.objects.all():
            if alloy.type_of_alloy not in type_of_alloys:
                type_of_alloys.append(alloy.type_of_alloy)
        context['type_of_alloys'] = type_of_alloys
        context['elements'] = elements
        context['query_link'] = ""
        if self.query:
            context['query_link'] = "&q=" + self.query
        if self.toa:
            context['query_link'] += "&ta=" + self.toa
        if self.filter_link:
            context['query_link'] += self.filter_link
        if self.ordering_links:
            context['links'] = sorted(self.ordering_links.items())
        return context

class AlloyDetail(DetailView):
    model = Alloy
    context_object_name = 'alloy'
    template_name = "nickel_super_alloys/alloy-detail.html"
