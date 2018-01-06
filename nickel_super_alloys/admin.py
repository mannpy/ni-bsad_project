from django.contrib import admin
from .models import Alloy, AlloyingElement, LongTimeStressRupture, OtherProperties



class AlloyingElementInline(admin.TabularInline):
    model = AlloyingElement
    extra = 0

class LongTimeStressRuptureInline(admin.TabularInline):
    model = LongTimeStressRupture
    extra = 0

class OtherPropertiesInline(admin.TabularInline):
    model = OtherProperties
    extra = 0

class AlloyAdmin(admin.ModelAdmin):
    search_fields = ['name']
    fields = ['name', 'balance', 'type_of_alloy', 'type_of_structure', 'work_temp']
    list_filter = ['created_date']
    list_display = ('name', 'type_of_alloy', 'type_of_structure', 'work_temp')
    inlines = [AlloyingElementInline, LongTimeStressRuptureInline, OtherPropertiesInline]

class AlloyingElementAdmin(admin.ModelAdmin):
    list_display = ('alloy', 'element', 'value')

class LongTimeStressRuptureAdmin(admin.ModelAdmin):
    list_display = ('alloy', 'temperature', 'life', 'stress')

admin.site.register(Alloy, AlloyAdmin)
#admin.site.register(AlloyingElement, AlloyingElementAdmin)
#admin.site.register(LongTimeStressRupture, LongTimeStressRuptureAdmin)
