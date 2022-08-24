import playhouse.apsw_ext as pw

import models

# if eddb has new dumps, update (locking commands in the meantime) https://eddb.io/api


def sync_factions():
    ...


def sync_systems():
    ...


def sync_stations():
    ...


def sync_commodities():
    ...


def sync_listings():
    # get live prices from Tromador's eddblink server http://elite.tromador.com/files/listings-live.csv
    ...


@models.db.atomic()
def insert_systems(systems):
    for system in systems:
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
