import csv
import logging

import playhouse.apsw_ext as pw
import requests
from discord.ext import tasks

import models

EDDB_FACTIONS_URL = 'https://eddb.io/archive/v6/factions.csv'
EDDB_SYSTEMS_URL = 'https://eddb.io/archive/v6/systems_populated.json'
EDDB_STATIONS_URL = 'https://eddb.io/archive/v6/stations.json'
EDDB_COMMODITIES_URL = 'https://eddb.io/archive/v6/commodities.json'
EDDB_LISTINGS_URL = 'https://eddb.io/archive/v6/listings.csv'
LIVE_LISTINGS_URL = 'https://elite.tromador.com/files/listings-live.csv'

logger = logging.getLogger(__name__)


def fetch_update(path, process_fn):
    headers = {'Accept-Encoding': 'gzip, deflate, sdch'}
    last_update = None
    try:
        last_update = models.DatabaseUpdate.get(models.DatabaseUpdate.path == path)
        headers['If-Modified-Since'] = last_update.updated_at
    except pw.DoesNotExist:
        logger.warning('DatabaseUpdate entry for %s not found; first time download', path)
    logger.info('Downloading %s...', path)
    response = requests.get(path, headers=headers)

    logger.info('Request complete for %s', path)
    response.raise_for_status()
    if response.status_code == 200:
        last_modified = response.headers['Last-Modified']
        logger.info('Last modification for %s on %s; updating database', path, last_modified)
        if last_update:
            last_update.updated_at = last_modified
            last_update.save()
        else:
            models.DatabaseUpdate.create(path=path, updated_at=last_modified)
        process_fn(response)
        logger.info('Finished loading %s', path)
    else:
        logger.debug('No modification found for %s', path)


@tasks.loop(minutes=15)
async def sync_database():
    fetch_update(EDDB_FACTIONS_URL, process_factions)
    fetch_update(EDDB_SYSTEMS_URL, process_systems)
    fetch_update(EDDB_STATIONS_URL, process_stations)
    fetch_update(EDDB_COMMODITIES_URL, process_commodities)
    fetch_update(EDDB_LISTINGS_URL, process_listings)
    fetch_update(LIVE_LISTINGS_URL, process_listings)


@models.db.atomic()
def process_factions(response):
    for row in csv.DictReader(response):
        del row['government_id']
        del row['allegiance_id']
        models.MinorFaction.create(**row)


@models.db.atomic()
def process_systems(response):
    for row in response.json():
        del row['government_id']
        del row['allegiance_id']
        del row['security_id']
        del row['primary_economy_id']
        del row['power_state_id']
        del row['reserve_type_id']
        del row['controlling_minor_faction']
        del row['minor_faction_presences']
        del row['minor_factions_updated_at']
        row['position'] = pw.fn.MakePointZ(row.pop('x'), row.pop('y'), row.pop('z'))
        row['states'] = ', '.join(state['name'] for state in row['states'])
        models.System.create(**row)


@models.db.atomic()
def process_stations(response):
    for row in response.json():
        del row['government_id']
        del row['allegiance_id']
        del row['type_id']
        del row['settlement_size_id']
        del row['settlement_security_id']
        del row['selling_ships']
        del row['selling_modules']
        row['states'] = ', '.join(state['name'] for state in row['states'])
        row['economies'] = ', '.join(row['economies'])
        models.Station.create(**row)


@models.db.atomic()
def process_commodities(response):
    for row in response.json():
        del row['category_id']
        row['category'] = row['category']['name']
        models.Commodity.create(**row)


@models.db.atomic()
def process_listings(response):
    for row in csv.DictReader(response):
        models.Listing.create(**row)
