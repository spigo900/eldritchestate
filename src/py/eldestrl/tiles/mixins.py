def door(tiledefs):
    tiledefs = tiledefs.copy()
    tiledef = tiledefs[0]
    if '_open' in tiledef['type']:
        new_type = tiledef.copy()
        new_type['type'] += '_closed'
        new_type['char'] = '+'
        new_type['blocks'] = True
        new_type['blocks_sight'] = True
        open_type = new_type
        closed_type = tiledef
    else:
        new_type = tiledef.copy()
        new_type['type'] += '_open'
        new_type['char'] = '/'
        new_type['blocks'] = False
        new_type['blocks_sight'] = False
        open_type = tiledef
        closed_type = new_type
    open_type.setdefault('behaviors', {})['close'] = \
        ('!change_tile_type', closed_type['type'])
    closed_type.setdefault('behaviors', {})['open'] = \
        ('!change_tile_type', open_type['type'])
    tiledefs.append(new_type)
    return tiledefs
