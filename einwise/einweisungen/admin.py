from django.contrib import admin
from .models import Area, Member, Einweisable, Einweisung
from admin_searchable_dropdown.filters import AutocompleteFilterFactory, AutocompleteFilter
from .views import MembersearchView
from django.urls import path
from django.shortcuts import reverse


class MemberFilter(AutocompleteFilter):
    title = 'Member'
    field_name = 'member'

    def get_autocomplete_url(self, request, model_admin):
        return reverse('admin:member_search')


class EinweisungAdmin(admin.ModelAdmin):
    list_display = ('member', 'level',  'einweisable', 'instructor', 
                    'issue_date')

    autocomplete_fields = ['member', 'einweisable']
    list_filter = ['level',
        MemberFilter,
        AutocompleteFilterFactory('Einweisable', 'einweisable')]
    search_fields = ['member__name', 'einweisable__name']

    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('custom_search/', self.admin_site.admin_view(MembersearchView.as_view(model_admin=self)),
                 name='member_search'),
        ]
        return custom_urls + urls


class MemberAdmin(admin.ModelAdmin):
    list_display = ('member_id', 'name', 'is_active')
    list_filter = ['is_active']
    ordering = ('member_id',)
    search_fields = ['name']


class EinweisableAdmin(admin.ModelAdmin):
    list_display = ('name', 'area', 'etype')
    list_filter = ('area',)
    ordering = ('area', 'etype', 'name')
    search_fields = ['name']


admin.site.register(Member, MemberAdmin)
admin.site.register(Einweisable, EinweisableAdmin)
admin.site.register(Area)
admin.site.register(Einweisung, EinweisungAdmin)
