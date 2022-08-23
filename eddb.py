import db


@db.db.atomic()
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
        system['position'] = f"POINT({system.pop('x')} {system.pop('y')} {system.pop('z')})"
        system['states'] = ', '.join(state['name'] for state in system['states'])
        db.System.create(**system)
