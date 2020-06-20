from django.core.management.base import BaseCommand, CommandError
from einweisungen.models import Member, Einweisable, Einweisung
import datetime
import csv
from pprint import pprint

einweisables = {}


class Command(BaseCommand):
    help = 'Import csv data.'

    def handle(self, *args, **options):
        with open('bestandsdaten.csv') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                if row[0] == 'Mitglieds- nummer':
                    for machine_index in range(3, len(row)):
                        if row[machine_index] != '':
                            einweisables[machine_index] = (row[machine_index], [])
                    break
            for row in reader:
                if len(row[0]) == 5:
                    if row[0] == '10001':
                        continue
                    try:
                        int(row[0])
                    except:
                        continue
                    for einweisungen_index in range(3, len(row)):
                        if row[einweisungen_index] != '':
                            einweisables[einweisungen_index][1].append((row[0], row[einweisungen_index]))
        pprint(einweisables)
        instructor = Member(member_id='99999', name='unbekannt')
        instructor.save()
        for machine, ews in einweisables.values():
            ews_ob = Einweisable(name=machine)
            ews_ob.save()
            for memid, level in ews:    
                mem = Member.objects.get(member_id=memid)
                ew_ob = Einweisung(
                            einweisable=ews_ob,
                            issue_date=datetime.date.today(),
                            member=mem,
                            instructor=instructor,
                            level=level)
                ew_ob.save()