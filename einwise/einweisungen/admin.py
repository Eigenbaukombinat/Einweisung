from django.contrib import admin
from .models import Area, Member, Einweisable, Einweisung


class EinweisungAdmin(admin.ModelAdmin):
    list_display = ('member', 'level',  'einweisable', 'instructor', 
                    'issue_date')
    list_filter = ['level', 'member', 'einweisable']
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ("member", "instructor"):
            kwargs["queryset"] = Member.objects.filter(is_active=True).order_by("name")
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class MemberAdmin(admin.ModelAdmin):
    list_display = ('member_id', 'name', 'is_active')
    list_filter = ['is_active']
    ordering = ('member_id',)


class EinweisableAdmin(admin.ModelAdmin):
    list_display = ('name', 'area', 'etype')
    list_filter = ('area',)
    ordering = ('area', 'etype', 'name')


admin.site.register(Member, MemberAdmin)
admin.site.register(Einweisable, EinweisableAdmin)
admin.site.register(Area)
admin.site.register(Einweisung, EinweisungAdmin)
