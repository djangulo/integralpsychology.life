"""
Generates a secret key and appends it to the project's
secrets.py
"""
import re
from random import SystemRandom
from os import listdir
from os.path import join as pjoin
from sys import exit as sysexit
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

class Command(BaseCommand):
    help = "Generates a secret key and writes/appends it to the "\
           "designated secrets file."
    def add_arguments(self, parser):
        parser.add_argument('-o',
                            '--output-file',
                            nargs='?',
                            default='secrets.py',
                            const='secrets.py',
                            type=str,
                            help=_('name of the output file; default '\
                                   '"secrets.py"'))
        parser.add_argument('-n',
                            '--keyvar-name',
                            nargs='?',
                            default='SECRET_KEY',
                            const='SECRET_KEY',
                            type=str,
                            help=_('name of the secret key variable; '\
                                   'default SECRET_KEY'))

    def handle(self, *args, **options):
        output = options['output_file']
        varname = options['keyvar_name']
        if output not in listdir(settings.PROJECT_DIR):
            with open(pjoin(settings.PROJECT_DIR, output), 'w') as fh:
                chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
                key = ''.join(SystemRandom().sample(chars, k=50))
                fh.write("%(var)s = '%(key)s'\n" % {
                    'var': varname,
                    'key': key,
                })
                self.stdout.write("\n %(var)s written into '%(out)s'"\
                                  " %(ok)s" % {
                    'var': varname,
                    'out': output,
                    'ok': self.style.SUCCESS(' OK')
                })
                self.stdout.flush()
                fh.close()
        else:
            with open(pjoin(settings.PROJECT_DIR, output), 'r') as fh:
                linebools = [bool(re.match(r'^' + varname + r'[\s=]?', line)) for line in fh.readlines()]
                if any(linebools):
                    self.stdout.write(
                        self.style.WARNING(' %(var)s exists in'\
                                           ' %(out)s, exitting' % {
                                               'var': varname,
                                               'out': output,
                                           }))
                    fh.close()
                    sysexit()
            with open(pjoin(settings.PROJECT_DIR, output), 'a') as fh:
                chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
                key = ''.join(SystemRandom().sample(chars, k=50))
                fh.write("%(var)s = '%(key)s'\n" % {
                    'var': varname,
                    'key': key,
                })
                self.stdout.write("\n %(var)s appended to '%(out)s'"\
                                  " %(ok)s" % {
                    'var': varname,
                    'out': output,
                    'ok': self.style.SUCCESS(' OK')
                })
                fh.close()
                sysexit()
