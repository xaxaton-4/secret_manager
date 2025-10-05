import datetime
import random

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from tickets.models import Ticket
from openbao.client import get_client


class Command(BaseCommand):
    help = 'Создаются тестовые пользователи: admin@mail.ru 12345 и user@mail.ru 12345, тикеты до 100 шт в бд'

    def handle(self, *args, **kwargs):
        admin, admin_created = self.create_user('admin@mail.ru', '12345')
        user, user_created = self.create_user('user@mail.ru', '12345')
        if not admin_created:
            self.stdout.write(self.style.WARNING('Admin with this email already exists'))
        else:
            admin.is_superuser = True
            admin.is_staff = True
            admin.save(update_fields=['is_superuser', 'is_staff'])
        if not user_created:
            self.stdout.write(self.style.WARNING('User with this email already exists'))

        tickets_created = self.create_some_tickets(user)
        self.stdout.write(self.style.SUCCESS(f'{tickets_created} tickets was created'))

        self.create_secrets()
        self.stdout.write('Private secrets created successully.')
        self.stdout.write(self.style.SUCCESS('Finish setup_test_data command'))

    def create_user(self, email: str, password: str):
        created = True
        try:
            user = User.objects.get(email=email)
            created = False
        except User.DoesNotExist:
            user = User.objects.create(email=email, username=email)
            user.set_password(password)
            user.save(update_fields=['password'])
        return user, created

    def create_some_tickets(self, user):
        need_count = 100 - Ticket.objects.filter(user=user).count()
        if need_count > 0:
            for i in range(need_count):
                random_days = random.randint(1, 30)
                random_resource = random.randint(1, 3)
                period = datetime.datetime.now() + datetime.timedelta(days=random_days)
                Ticket.objects.create(resource=f'test_resource{random_resource}', reason=f'reason-{i}', user=user, period=period)
        return need_count

    def create_secrets(self):
        openbao = get_client()
        openbao.write_secret('private/test_resource1', data={'v': 'test-secret-value'})
        openbao.write_secret('private/test_resource2', data={'v': 'realsecret'})
        openbao.write_secret('private/test_resource3', data={'v': 'secret-value'})
