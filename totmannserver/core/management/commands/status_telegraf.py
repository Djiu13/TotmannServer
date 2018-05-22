from django.core.management.base import BaseCommand, CommandError
from core import models
import re

class Command(BaseCommand):
    help = "Dump state of checks for some user in influx line format."

    def add_arguments(self, parser):
        parser.add_argument('user', nargs=1, type=str)

    @staticmethod
    def escape_tag(txt):
        txt = re.sub("""[^a-zA-Z0-9_ -]""", '', txt)
        return txt.replace(" ", r"\ ")

    def escape_value(txt):
        return '"' + txt.replace('"', r'\"') + '"' 

    def handle(self, *args, **kwargs):
        checks = models.Check.objects.filter(owner__username=kwargs['user'][0], enabled=True).all()
        tags = ''
        for c in checks:
            service = self.escape_tag(c.name)
            state = 0 if not c.is_late() else 1
            print ('totmann_check,service=%s%s is_late=%d' % (service, tags, state))
