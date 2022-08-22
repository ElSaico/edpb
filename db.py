import enum

import peewee as pw
from playhouse.apsw_ext import APSWDatabase

db = APSWDatabase('db.sqlite3')
db.load_extension('mod_spatialite')


class MinorFaction(pw.Model):
    name = pw.CharField()
    updated_at = pw.DateTimeField()
    government = pw.CharField(index=True)
    allegiance = pw.CharField(index=True)
    home_system = pw.DeferredForeignKey('System', backref='home_factions')
    is_player_faction = pw.BooleanField()

    class Meta:
        database = db


class System(pw.Model):
    edsm_id = pw.IntegerField()
    name = pw.CharField()
    #position (TODO set up spatialite)
    population = pw.IntegerField()
    is_populated = pw.BooleanField()
    government = pw.CharField(index=True)
    allegiance = pw.CharField(index=True)
    states = pw.CharField()
    security = pw.CharField(index=True)
    primary_economy = pw.CharField(index=True)
    power = pw.CharField(index=True)
    power_state = pw.CharField(index=True)
    needs_permit = pw.BooleanField()
    updated_at = pw.DateTimeField()
    minor_factions_updated_at = pw.DateTimeField()
    simbad_ref = pw.CharField()
    controlling_minor_faction = pw.ForeignKeyField(MinorFaction, backref='controlling_systems')
    reserve_type = pw.CharField(index=True)
    ed_system_address = pw.IntegerField()

    class Meta:
        database = db


class Station(pw.Model):
    name = pw.CharField()
    system = pw.ForeignKeyField(System, backref='stations')
    controlling_minor_faction = pw.ForeignKeyField(MinorFaction, backref='controlling_stations')
    updated_at = pw.DateTimeField()
    shipyard_updated_at = pw.DateTimeField()
    outfitting_updated_at = pw.DateTimeField()
    market_updated_at = pw.DateTimeField()
    max_landing_pad_size = pw.CharField(index=True)
    distance_to_star = pw.IntegerField()
    government = pw.CharField(index=True)
    allegiance = pw.CharField(index=True)
    states = pw.CharField()
    type = pw.CharField(index=True)
    has_blackmarket = pw.BooleanField()
    has_market = pw.BooleanField()
    has_refuel = pw.BooleanField()
    has_repair = pw.BooleanField()
    has_rearm = pw.BooleanField()
    has_outfitting = pw.BooleanField()
    has_shipyard = pw.BooleanField()
    has_docking = pw.BooleanField()
    has_commodities = pw.BooleanField()
    has_material_trader = pw.BooleanField()
    has_technology_broker = pw.BooleanField()
    has_carrier_vendor = pw.BooleanField()
    has_carrier_administration = pw.BooleanField()
    has_interstellar_factors = pw.BooleanField()
    has_universal_cartographics = pw.BooleanField()
    is_planetary = pw.BooleanField()
    economies = pw.CharField()
    settlement_size = pw.CharField(index=True)
    settlement_security = pw.CharField(index=True)
    body_id = pw.IntegerField()
    ed_market_id = pw.IntegerField()

    class Meta:
        database = db


class CommodityBracket(enum.IntEnum):
    TEMPORARY = -1  # empty on eddb, -1 on eddblink servers; the latter is most sensible
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3

    @classmethod
    def choices(cls):
        return [(name, member.value) for name, member in cls.__members__.items()]


class Commodity(pw.Model):
    ed_id = pw.IntegerField()
    name = pw.CharField()
    category = pw.CharField(index=True)
    is_rare = pw.BooleanField()
    is_non_marketable = pw.BooleanField()
    average_price = pw.IntegerField()
    max_buy_price = pw.IntegerField()
    max_sell_price = pw.IntegerField()
    min_buy_price = pw.IntegerField()
    min_sell_price = pw.IntegerField()
    buy_price_lower_average = pw.IntegerField()
    sell_price_upper_average = pw.IntegerField()

    class Meta:
        database = db


class Listing(pw.Model):
    station = pw.ForeignKeyField(Station, backref='listings')
    commodity = pw.ForeignKeyField(Commodity, backref='listings')
    buy_price = pw.IntegerField()
    supply = pw.IntegerField()
    supply_bracket = pw.SmallIntegerField(choices=CommodityBracket.choices())
    sell_price = pw.IntegerField()
    demand = pw.IntegerField()
    demand_bracket = pw.SmallIntegerField(choices=CommodityBracket.choices())
    collected_at = pw.DateTimeField()

    class Meta:
        database = db
