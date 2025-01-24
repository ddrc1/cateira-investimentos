from .cron import create_custodies_snaphots, get_ticker_price_data

from celery import shared_task

@shared_task
def create_custodies_snaphots():
    create_custodies_snaphots()

@shared_task
def get_ticker_price_data():
    get_ticker_price_data()