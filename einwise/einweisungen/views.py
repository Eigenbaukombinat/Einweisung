from django.http import HttpResponse
from einweisungen.models import Einweisung, Member, Area, Einweisable
from django.template import loader
import datetime
from django.contrib.auth.decorators import permission_required

from admin_searchable_dropdown.views import AutocompleteJsonView


class MembersearchView(AutocompleteJsonView):
    model_admin = None
    def get_queryset(self):
        """
           your custom logic goes here.
        """
        queryset = Member.objects.filter(is_active=True).order_by('name')
        return queryset


class NonEinweisung(object):
    issue_date = ''

@permission_required('einweisungen.view_all')
def index(request):
    rfid = request.GET.get('rfid')
    memid = request.GET.get('memid')
    error = False
    mem = None
    if rfid or memid:
        try:
            if rfid:
                mems = Member.objects.filter(rfid=rfid)
            elif memid:
                mems = Member.objects.filter(member_id=memid)
            if len(mems) != 1:
                error = 'More than 1 member found.'
            else:
                mem = mems[0]
        except Member.DoesNotExist:
            error = 'Member not found.'


    if mem:
        einweisungen = Einweisung.objects.filter(member=mem)
        member = mem
    else:
        einweisungen = []
        member = None

    areas = {}
    if member is not None:
        einweisungen_by_einweisable_id = dict([(e.einweisable.id, e) for e in einweisungen])

        all_areas = Area.objects.all()
        for area in all_areas:
            areas[area.name] = []
            for ews in Einweisable.objects.filter(area=area):
                einweisung = einweisungen_by_einweisable_id.get(ews.id)
                if einweisung is None:
                    einweisung = NonEinweisung()
                areas[area.name].append((ews, einweisung))

    left = {}
    right= {}
    for a_key, a_val in areas.items():
        if a_key in 'HandarbeitHolz':
            left[a_key] = a_val
        else:
            right[a_key] = a_val



    template = loader.get_template('einweisungen/index.html')
    context = {
        'areas': [('left', left.items()), ('right', right.items())],
        'member': member,
        'error': error,
        'today': datetime.date.today(),
    }
    return HttpResponse(template.render(context, request))

