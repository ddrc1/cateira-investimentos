from django.db.models import QuerySet
from django.db.utils import IntegrityError
from django.db import transaction

from typing import Optional
from yfinance import Ticker
import pandas as pd
from datetime import timedelta, datetime
from concurrent.futures import ThreadPoolExecutor
from decouple import config
from pymongo import MongoClient

from ..assets.models import Asset, Dividend, AssetPrice
from ..operations.models import Custody, CustodySnapshot

def datalake_connection():
    client = MongoClient(f"mongodb://{config('DATALAKE_USER')}:{config('DATALAKE_PASSWORD')}@{config('DATALAKE_HOST')}/")
    db = client[config('DATALAKE_DB')]
    collection = db[config('DATALAKE_COLLECTION')]
    return collection

def get_tick(asset: Asset) -> Optional[Ticker]:
    tick = None
    if asset.asset_type.name == "Cryptocurrency":
        tick = Ticker(asset.code + "-USD")
    else:
        tick = Ticker(asset.code)
        if tick.history().empty:
            tick = Ticker(asset.code + ".SA")
            if tick.history().empty:
                return None
    return tick

def add_dividends_to_users_custody(new_dividend: Dividend):
    custodies: QuerySet[Custody] = Custody.objects.filter(asset=new_dividend.asset, volume__gt=0, active=True)
    for custody in custodies:
        custody.earned_dividends.create(dividend=new_dividend, volume=custody.volume)

@transaction.atomic
def create_custodies_snaphots():
    custodies: QuerySet[Custody] = Custody.objects.filter(active=True, volume__gt=0)
    for custody in custodies:
        CustodySnapshot.objects.create(asset=custody.asset, volume=custody.volume, total_cost=custody.total_cost,
                                       last_price=custody.last_price, mean_price=custody.mean_price, user=custody.user,
                                       dividend_amount_received=custody.dividend_amount_received, total_value=custody.total_value)

@transaction.atomic
def get_ticker_price_data():
    assets: QuerySet[Asset] = Asset.objects.filter(active=True)
    connection = datalake_connection()

    @transaction.atomic
    def process(asset: Asset):
        while True:
            try:
                tick = get_tick(asset)
                break
            except ConnectionError as e:
                print(e)
            except Exception as e:
                print(e)
                break

        if not tick:
            return

        if asset.prices.exists():
            hist = tick.history(period="1d", start=asset.prices.last().date + timedelta(days=1), end=datetime.today().date() - timedelta(days=1), interval='1d')
        else:
            hist: pd.DataFrame = tick.history(period='max', end=datetime.today().date() - timedelta(days=1), interval='1d')
            hist.dropna(inplace=True)

        if hist.empty:
            return

        if len(tick.info.keys()) > 1:
            connection.insert_one({"data": tick.info, "asset": asset.code, "date": datetime.now()})

        hist.index = hist.index.tz_convert("UTC")

        try:
            price_objects = []
            for row in hist.itertuples():
                price_objects.append(AssetPrice(open_price=row.Open, high_price=row.High, low_price=row.Low, close_price=row.Close, 
                                                date=row.Index.date(), volume=row.Volume, asset=asset))
                if row.Dividends:
                    dividend: Dividend = asset.dividends.create(value=row.Dividends, date=row.Index.date())
                    add_dividends_to_users_custody(dividend)

            AssetPrice.objects.bulk_create(price_objects)
        except IntegrityError:
            #TODO log error
            return
        
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.map(process, assets)