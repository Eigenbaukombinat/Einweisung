from django.contrib import admin
from .models import Area, Member, Einweisable, Einweisung, Multieinweisung
from admin_searchable_dropdown.filters import AutocompleteFilterFactory, AutocompleteFilter
from .views import MembersearchView
from django.urls import path
from django.shortcuts import reverse
from django.db.utils import IntegrityError
from django.contrib import messages


class MemberFilter(AutocompleteFilter):
    title = 'Member'
    field_name = 'member'

    def get_autocomplete_url(self, request, model_admin):
        return reverse('admin:member_search')


class EinweisungAdmin(admin.ModelAdmin):
    list_display = ('member', 'level',  'einweisable', 'instructor', 
                    'issue_date')

    autocomplete_fields = ['member', 'instructor', 'einweisable']
    list_filter = ['level',
        MemberFilter,
        AutocompleteFilterFactory('Einweisable', 'einweisable')]
    search_fields = ['member__name', 'einweisable__name']
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('member_search/', self.admin_site.admin_view(MembersearchView.as_view(model_admin=self)),
                 name='member_search'),
        ]
        return custom_urls + urls




@admin.action(description='Generate Einweisungen')
def create_einweisungen(modeladmin, request, queryset):
    for multieinweisung in queryset.all():
        error = False
        for mem in multieinweisung.members.all():
            e = Einweisung()
            e.member = mem
            e.einweisable = multieinweisung.einweisable
            e.level = multieinweisung.level
            e.issue_date = multieinweisung.issue_date
            e.instructor = multieinweisung.instructor
            try:
                e.save()
            except IntegrityError:
                messages.error(request, f"Einweisung {mem.name} für {multieinweisung.einweisable} existiert schon.")
                error = True
                break
        if not error:
            multieinweisung.delete()

class MultieinweisungAdmin(admin.ModelAdmin):
    list_display = ('einweisable', 'instructor', 'issue_date')

    autocomplete_fields = ["members", "instructor", "einweisable"]
    actions = [create_einweisungen]

class MemberAdmin(admin.ModelAdmin):
    list_display = ('member_id', 'name', 'is_active')
    list_filter = ['is_active']
    ordering = ('member_id',)
    search_fields = ['name']

    def get_queryset(self, req):
        #check url here, only do for autocomplete, as
        #this is called for list view also
        qs = super().get_queryset(req)
        if 'autocomplete' in req.get_full_path():
            qs = qs.filter(is_active=True)
        return qs

class EinweisableAdmin(admin.ModelAdmin):
    list_display = ('name', 'area', 'etype')
    list_filter = ('area',)
    ordering = ('area', 'etype', 'name')
    search_fields = ['name']


admin.site.register(Member, MemberAdmin)
admin.site.register(Einweisable, EinweisableAdmin)
admin.site.register(Area)
admin.site.register(Einweisung, EinweisungAdmin)
admin.site.register(Multieinweisung, MultieinweisungAdmin)


