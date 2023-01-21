from django.contrib import admin
from .models import Area, Member, Einweisable, Einweisung
from admin_searchable_dropdown.filters import AutocompleteFilterFactory


class EinweisungAdmin(admin.ModelAdmin):
    list_display = ('member', 'level',  'einweisable', 'instructor', 
                    'issue_date')

    autocomplete_fields = ['member', 'einweisable']
    list_filter = ['level',
        AutocompleteFilterFactory('Mitglied', 'member'),
        AutocompleteFilterFactory('Einweisable', 'einweisable')]
    search_fields = ['member__name', 'einweisable__name']

    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ("member", "instructor"):
            kwargs["queryset"] = Member.objects.filter(is_active=True).order_by("name")
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


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
