#coding:utf8
from django.core.management.base import BaseCommand, CommandError
from einweisungen.models import Member
from gocept.collmex.collmex import Collmex
import configparser
import datetime
import io


DEFAULT_INI = """[default]
foo = 1
"""


class Command(BaseCommand):
    help = 'Sync members from collmex.'

    def handle(self, *args, **options):
        api = Collmex()
        members = api.get_members(include_inactive=True)
        checked = 0

        for mem in members:
            checked += 1
            collmex_id = mem.get('Mitgliedsnummer')
            try:
                db_mem = Member.objects.get(member_id=collmex_id)
            except Member.DoesNotExist:
                db_mem = Member(
                    member_id=collmex_id,
                    name=f"{mem.get('Vorname')} {mem.get('Name')}")

            if not is_active(mem):
                db_mem.is_active = False
                db_mem.name = 'ausgetreten'
            else:
                db_mem.is_active = True
                db_mem.name = f"{mem.get('Vorname')} {mem.get('Name')}" 
            #fetch rfid from collmex "bemerkungen" field"""
            mconfig = configparser.ConfigParser()
            try:
                mconfig.readfp(io.StringIO(mem.get('Bemerkung')))
            except configparser.Error as exc:
                self.stdout.write(self.style.ERROR(
                   u'Member <{} {}> has invalid data in Bemerkung field.'
                   u'\n{}'.format(
                       mem.get('Vorname'),
                       mem.get('Name'), str(exc)
                   )
                ))
                mconfig.readfp(io.StringIO(DEFAULT_INI))         
            if (mconfig.has_section('rfid') 
                    and 'ausweis' in [k for k,v in  mconfig.items('rfid')]):
                rfid = mconfig['rfid'].get('ausweis', '')
                db_mem.rfid = rfid

            db_mem.save()

            self.stdout.write(self.style.SUCCESS('Imported member "%s"' % collmex_id))





def is_active(mem):
    austritt = mem.get('Austrittsdatum')
    if not austritt:
        return True
    if int(datetime.date.today().strftime('%Y%m%d')) > int(austritt):
        return False
    return True

