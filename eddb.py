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

    logger.info('Download complete for %s', path)
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
    else:
        logger.debug('No modification found for %s', path)


@tasks.loop(minutes=15)
async def sync_database():
    fetch_update(EDDB_FACTIONS_URL, process_factions)
    fetch_update(EDDB_SYSTEMS_URL, process_systems)
    fetch_update(EDDB_STATIONS_URL, process_stations)
    fetch_update(EDDB_COMMODITIES_URL, process_commodities)
    fetch_update(EDDB_LISTINGS_URL, process_listings_eddb)


@models.db.atomic()
def process_factions(response):
    ...


@models.db.atomic()
def process_systems(response):
    for system in response.json():
        del system['government_id']
        del system['allegiance_id']
        del system['security_id']
        del system['primary_economy_id']
        del system['power_state_id']
        del system['reserve_type_id']
        del system['controlling_minor_faction']
        del system['minor_faction_presences']
        del system['minor_factions_updated_at']
        system['position'] = pw.fn.MakePointZ(system.pop('x'), system.pop('y'), system.pop('z'))
        system['states'] = ', '.join(state['name'] for state in system['states'])
        models.System.create(**system)


@models.db.atomic()
def process_stations(response):
    ...


@models.db.atomic()
def process_commodities(response):
    ...


def process_listings_eddb(response):
    if response.status_code == 304:
        fetch_update(LIVE_LISTINGS_URL, process_listings)
    process_listings(response)


@models.db.atomic()
def process_listings(response):
    ...
