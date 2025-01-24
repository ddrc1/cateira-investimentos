from apps.cron.cron import create_custodies_snaphots

class Command(BaseCommand):
    help = 'Create custodies snapshots'

    def handle(self, *args, **options):
        create_custodies_snaphots()