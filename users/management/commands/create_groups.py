from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Creates the moderator group'

    def handle(self, *args, **options):
        moderators_group, created = Group.objects.get_or_create(name='moderators')
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created moderator group'))
        else:
            self.stdout.write(self.style.SUCCESS('Moderator group already exists'))