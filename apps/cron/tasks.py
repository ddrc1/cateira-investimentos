from apps.cron.cron import create_custodies_snaphots, get_ticker_price_data

from celery import shared_task

@shared_task
def create_custodies_snaphots_task():
    create_custodies_snaphots()

@shared_task
def get_ticker_price_data_task():
    get_ticker_price_data()