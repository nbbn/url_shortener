from django.core.management.base import BaseCommand
import requests
from django.utils.dateparse import parse_datetime
from django.contrib.auth.hashers import make_password

from django.contrib import auth
import pytz


class Command(BaseCommand):
    help = 'Add fake users from randomuser.me'

    def add_arguments(self, parser):
        parser.add_argument('number_of_users', type=int)

    def handle(self, number_of_users, **options):
        try:
            r = requests.get(
                'https://randomuser.me/api/'
                '?inc=login,name,email,registered&noinfo&password=special,32&results={}'.format(number_of_users),
                timeout=10)
        except requests.RequestException:
            raise SystemExit('no internet access or other issue with connection.')
        if r.status_code != 200:
            raise SystemExit('randomuser.me issue, please check it.')
        for i in r.json()['results']:
            try:
                username = i['login']['username']
                first_name = i['name']['first']
                last_name = i['name']['last']
                email = i['email']
                password = i['login']['password']
                date_joined = pytz.utc.localize(parse_datetime(i['registered']))
            except KeyError:
                self.stdout.write(self.style.ERROR('Wrong schema, skipping!'))
                continue
            user = auth.get_user_model()(username=username,
                                         first_name=first_name,
                                         last_name=last_name,
                                         email=email,
                                         password=make_password(password),
                                         date_joined=date_joined)
            user.save()
        self.stdout.write(self.style.SUCCESS('Users added :)'))
