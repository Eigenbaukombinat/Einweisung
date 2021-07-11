#coding:utf8
from django.core.management.base import BaseCommand, CommandError
from einweisungen.models import Member, Einweisung


DEFAULT_INI = """[default]
foo = 1
"""


class Command(BaseCommand):
    help = 'Migrate Einweisungen from one member to another.'

    def add_arguments(self, parser):
        parser.add_argument('old_mem_id', type=int)
        parser.add_argument('new_mem_id', type=int)

    def handle(self, *args, **options):
        old_mem = Member.objects.get(member_id=options.get('old_mem_id'))
        new_mem = Member.objects.get(member_id=options.get('new_mem_id'))
        einw = Einweisung.objects.filter(member=old_mem)
        num = len(einw)
        for ein in einw:
            ein.member = new_mem
            ein.save()
        self.stdout.write(self.style.SUCCESS(f'Migrated {num} Einweisungen from {old_mem.member_id} to {new_mem.member_id}'))

