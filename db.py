import enum

import peewee as pw

db = pw.SqliteDatabase('trade.db')


class ChoiceMixin:
    @classmethod
    def choices(cls):
        return [(name, member.value) for name, member in cls.__members__.items()]


class MinorFaction(pw.Model):
    class Meta:
        database = db


class System(pw.Model):
    class Meta:
        database = db


class LandingPadSize(ChoiceMixin, enum.Enum):
    pass


class Government(ChoiceMixin, enum.IntEnum):
    pass


class Allegiance(ChoiceMixin, enum.IntEnum):
    pass


class StationType(ChoiceMixin, enum.IntEnum):
    pass


class Station(pw.Model):
    name = pw.CharField()
    system = pw.ForeignKeyField(System, backref='stations')
    controlling_minor_faction = pw.ForeignKeyField(MinorFaction, backref='controlling_stations')
    updated_at = pw.DateTimeField()
    shipyard_updated_at = pw.DateTimeField()
    outfitting_updated_at = pw.DateTimeField()
    market_updated_at = pw.DateTimeField()
    max_landing_pad_size = pw.CharField(choices=LandingPadSize.choices())
    distance_to_star = pw.IntegerField()
    government = pw.SmallIntegerField(choices=Government.choices())
    allegiance = pw.SmallIntegerField(choices=Allegiance.choices())
    #states
    type = pw.SmallIntegerField(choices=StationType.choices())
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
    #economies
    #settlement_size
    #settlement_security
    body_id = pw.IntegerField()
    ed_market_id = pw.IntegerField()

    class Meta:
        database = db


class CommodityCategory(ChoiceMixin, enum.IntEnum):
    ...  # TODO map categories


class CommodityBracket(ChoiceMixin, enum.IntEnum):
    TEMPORARY = -1  # empty on eddb, -1 on eddblink servers; the latter is most sensible
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Commodity(pw.Model):
    ed_id = pw.IntegerField()
    name = pw.CharField()
    category = pw.SmallIntegerField(choices=CommodityCategory.choices())
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

