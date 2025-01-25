from apps.cron.cron import get_ticker_price_data

class Command(BaseCommand):
    help = 'Get ticker price data'

    def handle(self, *args, **options):
        get_ticker_price_data()