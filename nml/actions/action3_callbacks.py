__license__ = """
NML is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

NML is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with NML; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA."""

from nml import expression, nmlop

callbacks = 0x12 * [{}]

# Possible values for 'purchase':
# 0 (or not set): not called from purchase list
# 1: called normally and from purchase list
# 2: only called from purchase list
# 'cbname': as 1) but if 'cbname' is set also, then 'cbname' overrides this
# in the purchase list. 'cbname' should have a value of 2 for 'purchase'


# Callbacks common to all vehicle types
general_vehicle_cbs = {
    'default' : {'type': 'cargo', 'num': None},
    'purchase' : {'type': 'cargo', 'num': 0xFF},
    'random_trigger' : {'type': 'cb', 'num': 0x01}, # Almost undocumented, but really neccesary!
    'loading_speed' : {'type': 'cb', 'num': 0x36, 'var10': 0x07},
    'cargo_subtype_text' : {'type': 'cb', 'num': 0x19, 'flag_bit': 5},
    'additional_text' : {'type': 'cb', 'num': 0x23, 'purchase': 2},
    'colour_mapping' : {'type': 'cb', 'num': 0x2D, 'flag_bit':6, 'purchase': 'purchase_colour_mapping'},
    'purchase_colour_mapping' : {'type': 'cb', 'num': 0x2D, 'flag_bit':6, 'purchase': 2},
    'start_stop' : {'type': 'cb', 'num': 0x31},
    'every_32_days' : {'type': 'cb', 'num': 0x32},
    'sound_effect' : {'type': 'cb', 'num': 0x33, 'flag_bit': 7},
    'refit_cost' : {'type': 'cb', 'num': 0x15E},
}

# Function to convert vehicle length to the actual property value, which is (8 - length)
def vehicle_length(value):
    return expression.BinOp(nmlop.SUB, expression.ConstantNumeric(8, value.pos), value, value.pos)

# Trains
callbacks[0x00] = {
    'visual_effect_and_powered' : {'type': 'cb', 'num': 0x10, 'flag_bit': 0},
    'shorten_vehicle' : {'type': 'cb', 'num': 0x36, 'var10': 0x21, 'deprecate_message': "Callback 'shorten_vehicle' is deprecated, use 'length' instead. Use a return value between 1 (very short) and 8 (default length, equal to constant VEHICLE_LENGTH) for this callback."},
    'length' : {'type': 'cb', 'num': 0x36, 'var10': 0x21, 'value_function': vehicle_length},
    'cargo_capacity' : [{'type': 'cb', 'num': 0x15, 'flag_bit': 3}, {'type': 'cb', 'num': 0x36, 'var10': 0x14, 'purchase': 'purchase_cargo_capacity'}],
    'purchase_cargo_capacity' : {'type': 'cb', 'num': 0x36, 'var10': 0x14, 'purchase': 2},
    'articulated_part' : {'type': 'cb', 'num': 0x16, 'flag_bit': 4, 'purchase': 1}, # Don't add separate purchase CB here
    'can_attach_wagon' : {'type': 'cb', 'num': 0x1D},
    'speed' : {'type': 'cb', 'num': 0x36, 'var10': 0x09, 'purchase': 'purchase_speed'},
    'purchase_speed' : {'type': 'cb', 'num': 0x36, 'var10': 0x09, 'purchase': 2},
    'power' : {'type': 'cb', 'num': 0x36, 'var10': 0x0B, 'purchase': 'purchase_power'},
    'purchase_power' : {'type': 'cb', 'num': 0x36, 'var10': 0x0B, 'purchase': 2},
    'running_cost_factor' : {'type': 'cb', 'num': 0x36, 'var10': 0x0D, 'purchase': 'purchase_running_cost_factor'},
    'purchase_running_cost_factor' : {'type': 'cb', 'num': 0x36, 'var10': 0x0D, 'purchase': 2},
    'weight' : {'type': 'cb', 'num': 0x36, 'var10': 0x16, 'purchase': 'purchase_weight'},
    'purchase_weight' : {'type': 'cb', 'num': 0x36, 'var10': 0x16, 'purchase': 2},
    'cost_factor' : {'type': 'cb', 'num': 0x36, 'var10': 0x17, 'purchase': 2},
    'tractive_effort_coefficient' : {'type': 'cb', 'num': 0x36, 'var10': 0x1F, 'purchase': 'purchase_tractive_effort_coefficient'},
    'purchase_tractive_effort_coefficient' : {'type': 'cb', 'num': 0x36, 'var10': 0x1F, 'purchase': 2},
    'bitmask_vehicle_info' : {'type': 'cb', 'num': 0x36, 'var10': 0x25},
    'cargo_age_period' : {'type': 'cb', 'num': 0x36, 'var10': 0x28},
}
callbacks[0x00].update(general_vehicle_cbs)

# Road vehicles
callbacks[0x01] = {
    'visual_effect' : {'type': 'cb', 'num': 0x10, 'flag_bit': 0},
    'shorten_vehicle' : {'type': 'cb', 'num': 0x36, 'var10': 0x23, 'deprecate_message': "Callback 'shorten_vehicle' is deprecated, use 'length' instead. Use a return value between 1 (very short) and 8 (default length, equal to constant VEHICLE_LENGTH) for this callback."},
    'length' : {'type': 'cb', 'num': 0x36, 'var10': 0x23, 'value_function': vehicle_length},
    'cargo_capacity' : [{'type': 'cb', 'num': 0x15, 'flag_bit': 3}, {'type': 'cb', 'num': 0x36, 'var10': 0x0F, 'purchase': 'purchase_cargo_capacity'}],
    'purchase_cargo_capacity' : {'type': 'cb', 'num': 0x36, 'var10': 0x0F, 'purchase': 2},
    'articulated_part' : {'type': 'cb', 'num': 0x16, 'flag_bit': 4,  'purchase': 1}, # Don't add separate purchase CB here
    'running_cost_factor' : {'type': 'cb', 'num': 0x36, 'var10': 0x09, 'purchase': 'purchase_running_cost_factor'},
    'purchase_running_cost_factor' : {'type': 'cb', 'num': 0x36, 'var10': 0x09, 'purchase': 2},
    'cost_factor' : {'type': 'cb', 'num': 0x36, 'var10': 0x11, 'purchase': 2},
    'power' : {'type': 'cb', 'num': 0x36, 'var10': 0x13, 'purchase': 'purchase_power'},
    'purchase_power' : {'type': 'cb', 'num': 0x36, 'var10': 0x13, 'purchase': 2},
    'weight' : {'type': 'cb', 'num': 0x36, 'var10': 0x14, 'purchase': 'purchase_weight'},
    'purchase_weight' : {'type': 'cb', 'num': 0x36, 'var10': 0x14, 'purchase': 2},
    'speed' : {'type': 'cb', 'num': 0x36, 'var10': 0x15, 'purchase': 'purchase_speed'},
    'purchase_speed' : {'type': 'cb', 'num': 0x36, 'var10': 0x15, 'purchase': 2},
    'tractive_effort_coefficient' : {'type': 'cb', 'num': 0x36, 'var10': 0x18, 'purchase': 'purchase_tractive_effort_coefficient'},
    'purchase_tractive_effort_coefficient' : {'type': 'cb', 'num': 0x36, 'var10': 0x18, 'purchase': 2},
    'cargo_age_period' : {'type': 'cb', 'num': 0x36, 'var10': 0x22},
}
callbacks[0x01].update(general_vehicle_cbs)

# Ships
callbacks[0x02] = {
    'visual_effect' : {'type': 'cb', 'num': 0x10, 'flag_bit': 0},
    'cargo_capacity' : [{'type': 'cb', 'num': 0x15, 'flag_bit': 3}, {'type': 'cb', 'num': 0x36, 'var10': 0x0D, 'purchase': 'purchase_cargo_capacity'}],
    'purchase_cargo_capacity' : {'type': 'cb', 'num': 0x36, 'var10': 0x0D, 'purchase': 2},
    'cost_factor' : {'type': 'cb', 'num': 0x36, 'var10': 0x0A, 'purchase': 2},
    'speed' : {'type': 'cb', 'num': 0x36, 'var10': 0x0B, 'purchase': 'purchase_speed'},
    'purchase_speed' : {'type': 'cb', 'num': 0x36, 'var10': 0x0B, 'purchase': 2},
    'running_cost_factor' : {'type': 'cb', 'num': 0x36, 'var10': 0x0F, 'purchase': 'purchase_running_cost_factor'},
    'purchase_running_cost_factor' : {'type': 'cb', 'num': 0x36, 'var10': 0x0F, 'purchase': 2},
    'cargo_age_period' : {'type': 'cb', 'num': 0x36, 'var10': 0x1D},
}
callbacks[0x02].update(general_vehicle_cbs)

# Aircraft
callbacks[0x03] = {
    'passenger_capacity' : [{'type': 'cb', 'num': 0x15, 'flag_bit': 3}, {'type': 'cb', 'num': 0x36, 'var10': 0x0F, 'purchase': 'purchase_passenger_capacity'}],
    'purchase_passenger_capacity' : {'type': 'cb', 'num': 0x36, 'var10': 0x0F, 'purchase': 2},
    'cost_factor' : {'type': 'cb', 'num': 0x36, 'var10': 0x0B, 'purchase': 2},
    'speed' : {'type': 'cb', 'num': 0x36, 'var10': 0x0C, 'purchase': 'purchase_speed'},
    'purchase_speed' : {'type': 'cb', 'num': 0x36, 'var10': 0x0C, 'purchase': 2},
    'running_cost_factor' : {'type': 'cb', 'num': 0x36, 'var10': 0x0E, 'purchase': 'purchase_running_cost_factor'},
    'purchase_running_cost_factor' : {'type': 'cb', 'num': 0x36, 'var10': 0x0E, 'purchase': 2},
    'mail_capacity' : {'type': 'cb', 'num': 0x36, 'var10': 0x11, 'purchase': 'purchase_mail_capacity'},
    'purchase_mail_capacity' : {'type': 'cb', 'num': 0x36, 'var10': 0x11, 'purchase': 2},
    'cargo_age_period' : {'type': 'cb', 'num': 0x36, 'var10': 0x1C},
    'range' : {'type': 'cb', 'num': 0x36, 'var10': 0x1F, 'purchase': 'purchase_range'},
    'rotor' : {'type': 'override'},
}
callbacks[0x03].update(general_vehicle_cbs)

# Stations (0x04) are not yet implemented

# Canals
callbacks[0x05] = {
    'sprite_offset' : {'type': 'cb', 'num': 0x147, 'flag_bit': 0},
    'default' : {'type': 'cargo', 'num': None},
}

# Bridges (0x06) have no action3

# Houses
callbacks[0x07] = {
    'random_trigger'         : {'type': 'cb', 'num': 0x01},
    'construction_check'     : {'type': 'cb', 'num':  0x17, 'flag_bit':  0},
    'anim_next_frame'        : {'type': 'cb', 'num':  0x1A, 'flag_bit':  1},
    'anim_control'           : {'type': 'cb', 'num':  0x1B, 'flag_bit':  2},
    'construction_anim'      : {'type': 'cb', 'num':  0x1C, 'flag_bit':  3},
    'colour'                 : {'type': 'cb', 'num':  0x1E, 'flag_bit':  4},
    'cargo_amount_accept'    : {'type': 'cb', 'num':  0x1F, 'flag_bit':  5},
    'anim_speed'             : {'type': 'cb', 'num':  0x20, 'flag_bit':  6},
    'destruction'            : {'type': 'cb', 'num':  0x21, 'flag_bit':  7},
    'cargo_type_accept'      : {'type': 'cb', 'num':  0x2A, 'flag_bit':  8},
    'cargo_production'       : {'type': 'cb', 'num':  0x2E, 'flag_bit':  9},
    'protection'             : {'type': 'cb', 'num': 0x143, 'flag_bit': 10},
    'watched_cargo_accepted' : {'type': 'cb', 'num': 0x148},
    'name'                   : {'type': 'cb', 'num': 0x14D},
    'foundations'            : {'type': 'cb', 'num': 0x14E, 'flag_bit': 11},
    'autoslope'              : {'type': 'cb', 'num': 0x14F, 'flag_bit': 12},
    'default'                : {'type': 'cargo', 'num': None},
}

# General variables (0x08) have no action3

# Industry tiles
callbacks[0x09] = {
    'random_trigger'      : {'type': 'cb', 'num': 0x01},
    'anim_control'        : {'type': 'cb', 'num': 0x25},
    'anim_next_frame'     : {'type': 'cb', 'num': 0x26, 'flag_bit': 0},
    'anim_speed'          : {'type': 'cb', 'num': 0x27, 'flag_bit': 1},
    'cargo_amount_accept' : {'type': 'cb', 'num': 0x2B, 'flag_bit': 2}, # Should work like the industry CB, i.e. call multiple times
    'cargo_type_accept'   : {'type': 'cb', 'num': 0x2C, 'flag_bit': 3}, # Should work like the industry CB, i.e. call multiple times
    'tile_check'          : {'type': 'cb', 'num': 0x2F, 'flag_bit': 4},
    'foundations'         : {'type': 'cb', 'num': 0x30, 'flag_bit': 5},
    'autoslope'           : {'type': 'cb', 'num': 0x3C, 'flag_bit': 6},
    'default'             : {'type': 'cargo', 'num': None},
}

# Industries
callbacks[0x0A] = {
    'construction_probability' : {'type': 'cb', 'num': 0x22,  'flag_bit': 0},
    'produce_cargo_arrival' : {'type': 'cb', 'num': 0x00,  'flag_bit': 1, 'var18': 0},
    'produce_256_ticks'     : {'type': 'cb', 'num': 0x00,  'flag_bit': 2, 'var18': 1},
    'location_check'        : {'type': 'cb', 'num': 0x28,  'flag_bit': 3}, # We need a way to access all those special variables
    'random_prod_change'    : {'type': 'cb', 'num': 0x29,  'flag_bit': 4},
    'monthly_prod_change'   : {'type': 'cb', 'num': 0x35,  'flag_bit': 5},
    'cargo_subtype_display' : {'type': 'cb', 'num': 0x37,  'flag_bit': 6},
    'extra_text_fund'       : {'type': 'cb', 'num': 0x38,  'flag_bit': 7},
    'extra_text_industry'   : {'type': 'cb', 'num': 0x3A,  'flag_bit': 8},
    'control_special'       : {'type': 'cb', 'num': 0x3B,  'flag_bit': 9},
    'stop_accept_cargo'     : {'type': 'cb', 'num': 0x3D,  'flag_bit': 10},
    'colour'                : {'type': 'cb', 'num': 0x14A, 'flag_bit': 11},
    'cargo_input'           : {'type': 'cb', 'num': 0x14B, 'flag_bit': 12},
    'cargo_output'          : {'type': 'cb', 'num': 0x14C, 'flag_bit': 13},
    'default'               : {'type': 'cargo', 'num': None},
}

# Cargos
def cargo_profit_value(value):
    # In NFO, calculation is (amount * price_factor * cb_result) / 8192
    # Units of the NML price factor differ by about 41.12, i.e. 1 NML unit = 41 NFO units
    # That'd make the formula (amount * price_factor * cb_result) / (8192 / 41)
    # This is almost (error 0.01%) equivalent to the following, which is what this calculation does
    # (amount * price_factor * (cb_result * 329 / 256)) / 256
    # This allows us to report a factor of 256 in the documentation, which makes a lot more sense than 199.804...
    # Not doing the division here would improve accuracy, but limits the range of the return value too much
    value = expression.BinOp(nmlop.MUL, value, expression.ConstantNumeric(329), value.pos)
    return expression.BinOp(nmlop.DIV, value, expression.ConstantNumeric(256), value.pos)

callbacks[0x0B] = {
    'profit'         : {'type': 'cb', 'num':  0x39, 'flag_bit': 0, 'value_function': cargo_profit_value},
    'station_rating' : {'type': 'cb', 'num': 0x145, 'flag_bit': 1},
    'default'        : {'type': 'cargo', 'num': None},
}

# Sound effects (0x0C) have no item-specific action3

# Airports
callbacks[0x0D] = {
    'additional_text' : {'type': 'cb', 'num': 0x155},
    'layout_name'     : {'type': 'cb', 'num': 0x156},
    'default'         : {'type': 'cargo', 'num': None},
}

# New signals (0x0E) have no item-specific action3

# Objects
callbacks[0x0F] = {
    'tile_check'      : {'type': 'cb', 'num': 0x157, 'flag_bit': 0, 'purchase': 2},
    'anim_next_frame' : {'type': 'cb', 'num': 0x158, 'flag_bit': 1},
    'anim_control'    : {'type': 'cb', 'num': 0x159},
    'anim_speed'      : {'type': 'cb', 'num': 0x15A, 'flag_bit': 2},
    'colour'          : {'type': 'cb', 'num': 0x15B, 'flag_bit': 3},
    'additional_text' : {'type': 'cb', 'num': 0x15C, 'flag_bit': 4, 'purchase': 2},
    'autoslope'       : {'type': 'cb', 'num': 0x15D, 'flag_bit': 5},
    'default'         : {'type': 'cargo', 'num': None},
    'purchase'        : {'type': 'cargo', 'num': 0xFF},
}

# Railtypes
callbacks[0x10] = {
    # No default here, it makes no sense
    'gui'             : {'type': 'cargo', 'num': 0x00},
    'track_overlay'   : {'type': 'cargo', 'num': 0x01},
    'underlay'        : {'type': 'cargo', 'num': 0x02},
    'tunnels'         : {'type': 'cargo', 'num': 0x03},
    'catenary_wire'   : {'type': 'cargo', 'num': 0x04},
    'catenary_pylons' : {'type': 'cargo', 'num': 0x05},
    'bridge_surfaces' : {'type': 'cargo', 'num': 0x06},
    'level_crossings' : {'type': 'cargo', 'num': 0x07},
    'depots'          : {'type': 'cargo', 'num': 0x08},
    'fences'          : {'type': 'cargo', 'num': 0x09},
    'tunnel_overlay'  : {'type': 'cargo', 'num': 0x0A},
}

# Airport tiles
callbacks[0x11] = {
    'foundations'     : {'type': 'cb', 'num': 0x150, 'flag_bit': 5},
    'anim_control'    : {'type': 'cb', 'num': 0x152},
    'anim_next_frame' : {'type': 'cb', 'num': 0x153, 'flag_bit': 0},
    'anim_speed'      : {'type': 'cb', 'num': 0x154, 'flag_bit': 1},
    'default'         : {'type': 'cargo', 'num': None},
}
