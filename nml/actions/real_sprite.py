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

from nml import generic, expression
from nml.actions import base_action
from nml.ast import assignment
import os
try:
    from PIL import Image
except ImportError:
    import Image

palmap_d2w = [
          0, 215, 216, 136,  88, 106,  32,  33, #   0..7
         40, 245,  10,  11,  12,  13,  14,  15, #   8..15
         16,  17,  18,  19,  20,  21,  22,  23, #  16..23
         24,  25,  26,  27,  28,  29,  30,  31, #  24..31
         53,  54,  34,  35,  36,  37,  38,  39, #  32..39
        178,  41,  42,  43,  44,  45,  46,  47, #  40..47
         48,  49,  50,  51,  52,  53,  54,  55, #  48..55
         56,  57,  58,  59,  60,  61,  62,  63, #  56..63
         64,  65,  66,  67,  68,  69,  70,  71, #  64..71
         72,  73,  74,  75,  76,  77,  78,  79, #  72..79
         80,  81,  82,  83,  84,  85,  86,  87, #  80..87
         96,  89,  90,  91,  92,  93,  94,  95, #  88..95
         96,  97,  98,  99, 100, 101, 102, 103, #  96..103
        104, 105,  53, 107, 108, 109, 110, 111, # 104..111
        112, 113, 114, 115, 116, 117, 118, 119, # 112..119
        120, 121, 122, 123, 124, 125, 126, 127, # 120..127
        128, 129, 130, 131, 132, 133, 134, 135, # 128..135
        170, 137, 138, 139, 140, 141, 142, 143, # 136..143
        144, 145, 146, 147, 148, 149, 150, 151, # 144..151
        152, 153, 154, 155, 156, 157, 158, 159, # 152..159
        160, 161, 162, 163, 164, 165, 166, 167, # 160..167
        168, 169, 170, 171, 172, 173, 174, 175, # 168..175
        176, 177, 178, 179, 180, 181, 182, 183, # 176..183
        184, 185, 186, 187, 188, 189, 190, 191, # 184..191
        192, 193, 194, 195, 196, 197, 198, 199, # 192..199
        200, 201, 202, 203, 204, 205, 206, 207, # 200..207
        208, 209, 210, 211, 212, 213, 214, 215, # 208..215
        216, 217, 246, 247, 248, 249, 250, 251, # 216..223
        252, 253, 254, 227, 228, 229, 230, 231, # 224..231
        232, 233, 234, 235, 236, 237, 238, 239, # 232..239
        240, 241, 242, 243, 244, 217, 218, 219, # 240..247
        220, 221, 222, 223, 224, 225, 226, 255, # 248..255
]

palmap_w2d = [
          0,   1,   2,   3,   4,   5,   6,   7, #   0..7
          8,   9,  10,  11,  12,  13,  14,  15, #   8..15
         16,  17,  18,  19,  20,  21,  22,  23, #  16..23
         24,  25,  26,  27,  28,  29,  30,  31, #  24..31
          6,   7,  34,  35,  36,  37,  38,  39, #  32..39
          8,  41,  42,  43,  44,  45,  46,  47, #  40..47
         48,  49,  50,  51,  52,  53,  54,  55, #  48..55
         56,  57,  58,  59,  60,  61,  62,  63, #  56..63
         64,  65,  66,  67,  68,  69,  70,  71, #  64..71
         72,  73,  74,  75,  76,  77,  78,  79, #  72..79
         80,  81,  82,  83,  84,  85,  86,  87, #  80..87
          4,  89,  90,  91,  92,  93,  94,  95, #  88..95
         96,  97,  98,  99, 100, 101, 102, 103, #  96..103
        104, 105,   5, 107, 108, 109, 110, 111, # 104..111
        112, 113, 114, 115, 116, 117, 118, 119, # 112..119
        120, 121, 122, 123, 124, 125, 126, 127, # 120..127
        128, 129, 130, 131, 132, 133, 134, 135, # 128..135
          3, 137, 138, 139, 140, 141, 142, 143, # 136..143
        144, 145, 146, 147, 148, 149, 150, 151, # 144..151
        152, 153, 154, 155, 156, 157, 158, 159, # 152..159
        160, 161, 162, 163, 164, 165, 166, 167, # 160..167
        168, 169, 170, 171, 172, 173, 174, 175, # 168..175
        176, 177, 178, 179, 180, 181, 182, 183, # 176..183
        184, 185, 186, 187, 188, 189, 190, 191, # 184..191
        192, 193, 194, 195, 196, 197, 198, 199, # 192..199
        200, 201, 202, 203, 204, 205, 206, 207, # 200..207
        208, 209, 210, 211, 212, 213, 214,   1, # 208..215
          2, 245, 246, 247, 248, 249, 250, 251, # 216..223
        252, 253, 254, 229, 230, 231, 227, 228, # 224..231
        232, 233, 234, 235, 236, 237, 238, 239, # 232..239
        240, 241, 242, 243, 244,   9, 218, 219, # 240..247
        220, 221, 222, 223, 224, 225, 226, 255, # 248..255
]

translate_w2d = ''.join(map(chr, palmap_w2d))
translate_d2w = ''.join(map(chr, palmap_d2w))

def convert_palette(pal):
    ret = 256 * [0]
    for idx, colour in enumerate(pal):
        if 0xD7 <= idx <= 0xE2:
            if idx != colour:
                raise generic.ScriptError("Indices 0xD7..0xE2 are not allowed in recolour sprites when the output is in the WIN palette")
            continue
        ret[palmap_d2w[idx]] = palmap_d2w[colour]
    return ret

class RealSprite(object):
    def __init__(self, param_list = None, label = None):
        self.param_list = param_list
        self.label = label
        self.is_empty = False
        self.xpos = None
        self.ypos = None
        self.xsize = None
        self.ysize = None

    def debug_print(self, indentation):
        print indentation*' ' + 'Real sprite, parameters:'
        for param in self.param_list:
            param.debug_print(indentation + 2)

    def get_labels(self):
        labels = {}
        if self.label is not None:
            labels[self.label.value] = 0
        return labels, 1

    def expand(self, default_file, default_mask_file, id_dict):
        return [parse_real_sprite(self, default_file, default_mask_file, id_dict)]

    def check_sprite_size(self):
        generic.check_range(self.xpos.value,  0, 0x7fffFFFF,   "Real sprite paramater 'xpos'", self.xpos.pos)
        generic.check_range(self.ypos.value,  0, 0x7fffFFFF,   "Real sprite paramater 'ypos'", self.ypos.pos)
        generic.check_range(self.xsize.value, 1, 0xFFFF,       "Real sprite paramater 'xsize'", self.xsize.pos)
        generic.check_range(self.ysize.value, 1, 0xFFFF,       "Real sprite paramater 'ysize'", self.ysize.pos)

    def validate_size(self):
        """
        Check if xpos/ypos/xsize/ysize are already set and if not, set them
        to 0,0,image_width,image_height.
        """
        if self.xpos is None:
            im = Image.open(generic.find_file(self.file.value))
            self.xpos = expression.ConstantNumeric(0)
            self.ypos = expression.ConstantNumeric(0)
            self.xsize = expression.ConstantNumeric(im.size[0])
            self.ysize = expression.ConstantNumeric(im.size[1])
            self.check_sprite_size()
        if self.mask_pos is None:
            self.mask_pos = (self.xpos, self.ypos)

    def __str__(self):
        ret = ""
        if self.label is not None:
            ret += str(self.label) + ": "
        ret += "["
        ret += ", ".join([str(param) for param in self.param_list])
        ret += "]"
        return ret

class SpriteAction(base_action.BaseAction):
    def __init__(self):
        self.sprite_num = None
        self.last = False

    def prepare_output(self, sprite_num):
        if self.sprite_num is not None and self.sprite_num.value != sprite_num:
            raise generic.ScriptError("Sprite number %d given in base_graphics-block, but it doesn't match output sprite number %d" % (self.sprite_num.value, sprite_num))

class RealSpriteAction(SpriteAction):
    def __init__(self):
        SpriteAction.__init__(self)
        self.sprite_list = []

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)

    def write(self, file):
        if len(self.sprite_list) == 0 or self.sprite_list[0].is_empty:
            file.print_empty_realsprite()
        else:
            file.print_sprite([s for s in self.sprite_list if not s.is_empty])
        if self.last: file.newline()

class RecolourSprite(object):
    def __init__(self, mapping, label = None):
        self.mapping = mapping
        self.label = label

    def debug_print(self, indentation):
        print indentation*' ' + 'Recolour sprite, mapping:'
        for assignment in self.mapping:
            print (indentation + 2)*' ' + '%s: %s;' % (str(assignment.name), str(assignment.value))

    def get_labels(self):
        labels = {}
        if self.label is not None:
            labels[self.label.value] = 0
        return labels, 1

    def expand(self, default_file, default_mask_file, id_dict):
        # create new struct, needed for template expansion
        new_mapping = []
        for old_assignment in self.mapping:
            from_min_value = old_assignment.name.min.reduce_constant([id_dict])
            from_max_value = from_min_value if old_assignment.name.max is None else old_assignment.name.max.reduce_constant([id_dict])
            to_min_value = old_assignment.value.min.reduce_constant([id_dict])
            to_max_value = None if old_assignment.value.max is None else old_assignment.value.max.reduce_constant([id_dict])
            new_mapping.append(assignment.Assignment(assignment.Range(from_min_value, from_max_value), assignment.Range(to_min_value, to_max_value), old_assignment.pos))
        return [RecolourSprite(new_mapping)]

    def __str__(self):
        ret = "" if self.label is None else str(self.label) + ": "
        ret += "recolour_sprite {\n"
        for assignment in self.mapping:
            ret += '%s: %s;' % (str(assignment.name), str(assignment.value))
        ret += "}"
        return ret

class RecolourSpriteAction(SpriteAction):
    def __init__(self, sprite):
        SpriteAction.__init__(self)
        self.sprite = sprite
        self.output_table = []

    def prepare_output(self, sprite_num):
        SpriteAction.prepare_output(self, sprite_num)
        colour_mapping = {}
        for assignment in self.sprite.mapping:
            if assignment.value.max is not None and assignment.name.max.value - assignment.name.min.value != assignment.value.max.value - assignment.value.min.value:
                raise generic.ScriptError("From and to ranges in a recolour block need to have the same size", assignment.pos)
            for i in range(assignment.name.max.value - assignment.name.min.value + 1):
                idx = assignment.name.min.value + i
                val = assignment.value.min.value
                if assignment.value.max is not None:
                    val += i
                colour_mapping[idx] = val
        for i in range(256):
            if i in colour_mapping:
                colour = colour_mapping[i]
            else:
                colour = i
            self.output_table.append(colour)

    def write(self, file):
        file.start_sprite(257)
        file.print_bytex(0)
        if file.palette not in ("DOS", "WIN"):
            raise generic.ScriptError("Recolour sprites are only supported when writing to the DOS or WIN palette. If you don't have any real sprites use the commandline option -p to set a palette.")
        colour_table = self.output_table if file.palette == "DOS" else convert_palette(self.output_table)
        for idx, colour in enumerate(colour_table):
            if idx % 16 == 0:
                file.newline()
            file.print_bytex(colour)
        if self.last: file.newline()
        file.end_sprite()

class TemplateUsage(object):
    def __init__(self, name, param_list, label, pos):
        self.name = name
        self.param_list = param_list
        self.label = label
        self.pos = pos

    def debug_print(self, indentation):
        print indentation*' ' + 'Template used:', self.name.value
        print (indentation+2)*' ' + 'Parameters:'
        for param in self.param_list:
            param.debug_print(indentation + 4)

    def get_labels(self):
        # Load labels from the template definition
        if self.name.value not in sprite_template_map:
            raise generic.ScriptError("Encountered unknown template identifier: " + self.name.value, self.name.pos)
        labels, offset = sprite_template_map[self.name.value].get_labels()
        # Add (possibly) label applied to ourselves
        if self.label is not None:
            if self.label.value in labels:
                raise generic.ScriptError("Duplicate label encountered; '%s' already exists." % self.label.value, self.pos)
            labels[self.label.value] = 0
        return labels, offset

    def expand(self, default_file, default_mask_file, parameters):
        if self.name.value not in sprite_template_map:
            raise generic.ScriptError("Encountered unknown template identifier: " + self.name.value, self.name.pos)
        template = sprite_template_map[self.name.value]
        if len(self.param_list) != len(template.param_list):
            raise generic.ScriptError("Incorrect number of template arguments. Expected " + str(len(template.param_list)) + ", got " + str(len(self.param_list)), self.pos)
        param_dict = {}
        for i, param in enumerate(self.param_list):
            param = param.reduce([real_sprite_compression_flags, parameters])
            if not isinstance(param, (expression.ConstantNumeric, expression.StringLiteral)):
                raise generic.ScriptError("Template parameters should be compile-time constants", param.pos)
            param_dict[template.param_list[i].value] = param.value

        return parse_sprite_list(template.sprite_list, default_file, default_mask_file, param_dict)

    def __str__(self):
        return "%s(%s)" % (str(self.name), ", ".join([str(param) for param in self.param_list]))

real_sprite_compression_flags = {
    'CROP'         : 0x00,
    'NOCROP'       : 0x40,
}


def parse_real_sprite(sprite, default_file, default_mask_file, id_dict):
    # check the number of parameters
    num_param = len(sprite.param_list)
    if num_param == 0:
        sprite.is_empty = True
        return sprite
    elif not (2 <= num_param <= 9):
        raise generic.ScriptError("Invalid number of arguments for real sprite. Expected 2..9.", sprite.param_list[0].pos)

    # create new sprite struct, needed for template expansion
    new_sprite = RealSprite()

    param_offset = 0

    if num_param >= 6:
        # xpos, ypos, xsize and ysize are all optional. If not specified they'll default
        # to 0, 0, image_width, image_height
        new_sprite.xpos  = sprite.param_list[0].reduce_constant([id_dict])
        new_sprite.ypos  = sprite.param_list[1].reduce_constant([id_dict])
        new_sprite.xsize = sprite.param_list[2].reduce_constant([id_dict])
        new_sprite.ysize = sprite.param_list[3].reduce_constant([id_dict])
        new_sprite.check_sprite_size()
        param_offset += 4

    new_sprite.xrel  = sprite.param_list[param_offset].reduce_constant([id_dict])
    new_sprite.yrel  = sprite.param_list[param_offset + 1].reduce_constant([id_dict])
    generic.check_range(new_sprite.xrel.value, -0x8000, 0x7fff,  "Real sprite paramater %d 'xrel'" % (param_offset + 1), new_sprite.xrel.pos)
    generic.check_range(new_sprite.yrel.value, -0x8000, 0x7fff,  "Real sprite paramater %d 'yrel'" % (param_offset + 2), new_sprite.yrel.pos)
    param_offset += 2

    # Next may follow any combination of (compression, filename, mask), but always in that order
    new_sprite.compression = expression.ConstantNumeric(0)
    if num_param > param_offset:
        try:
            new_sprite.compression = sprite.param_list[param_offset].reduce_constant([real_sprite_compression_flags, id_dict])
            param_offset += 1
            if (new_sprite.compression.value & ~0x40) != 0:
                raise generic.ScriptError("Real sprite compression is invalid; can only have the NOCROP bit (0x40) set, encountered " + str(new_sprite.compression.value), new_sprite.compression.pos)
        except generic.ConstError:
            pass

    new_sprite.file = default_file
    if num_param > param_offset and not isinstance(sprite.param_list[param_offset], expression.Array):
        new_sprite.file = sprite.param_list[param_offset].reduce([id_dict])
        param_offset += 1
        if not isinstance(new_sprite.file, expression.StringLiteral):
            raise generic.ScriptError("Real sprite parameter %d 'file' should be a string literal" % (param_offset + 1), new_sprite.file.pos)

    if new_sprite.file is None:
        raise generic.ScriptError("No image file specified for real sprite", sprite.param_list[0].pos)

    new_sprite.mask_file = default_mask_file
    new_sprite.mask_pos = None
    if num_param > param_offset:
        mask = sprite.param_list[param_offset]
        param_offset += 1
        # Mask may be either string (file only) or array (empty => no mask, 1 value => file only, 2 => offsets only, 3 => file + offsets)
        if isinstance(mask, expression.Array):
            if not (0 <= len(mask.values) <= 3):
                raise generic.ScriptError("Real sprite mask should be an array with 0 to 3 values, encountered %d" % len(mask.values), mask.pos)
            if len(mask.values) == 0:
                # disable any default mask
                new_sprite.mask_file = None
            else:
                if len(mask.values) & 1:
                    new_sprite.mask_file = mask.values[0].reduce([id_dict])
                    if not isinstance(new_sprite.mask_file, expression.StringLiteral):
                        raise generic.ScriptError("Real sprite parameter 'mask_file' should be a string literal", new_sprite.file.pos)
                if len(mask.values) & 2:
                    new_sprite.mask_pos = tuple(mask.values[i].reduce_constant([id_dict]) for i in range(-2, 0))
                    # Check that there is also a mask specified, else the offsets make no sense
                    if new_sprite.mask_file is None:
                        raise generic.ScriptError("Mask offsets are specified, but there is no mask file set.", new_sprite.mask_pos[0].pos)
        else:
            new_sprite.mask_file = mask.reduce([id_dict])
            if not isinstance(new_sprite.mask_file, expression.StringLiteral):
                raise generic.ScriptError("Real sprite parameter %d 'mask' should be an array or string literal" % (param_offset + 1), new_sprite.file.pos)

    if num_param > param_offset:
        raise generic.ScriptError("Real sprite has too many parameters, the last %d parameter(s) cannot be parsed." % (num_param - param_offset), sprite.param_list[param_offset].pos)

    return new_sprite

sprite_template_map = {}

def parse_sprite_list(sprite_list, default_file, default_mask_file, parameters = {}):
    real_sprite_list = []
    for sprite in sprite_list:
        real_sprite_list.extend(sprite.expand(default_file, default_mask_file, parameters))
    return real_sprite_list

def parse_sprite_data(sprite_container):
    """
    @param sprite_container: AST node that contains the sprite data
    @type sprite_container: L{SpriteContainer}

    @return: List of real sprite actions
    @rtype: C{list} of L{BaseAction}
    """
    all_sprite_data = sprite_container.get_all_sprite_data()
    action_list = []
    first = True

    for sprite_data in all_sprite_data:
        sprite_list, default_file, default_mask_file, zoom_level, bit_depth = sprite_data
        new_sprite_list = parse_sprite_list(sprite_list, default_file, default_mask_file)
        if not first and len(new_sprite_list) != len(action_list):
            raise generic.ScriptError("Expected %d alternative sprites for %s '%s', got %d." % \
                    (len(action_list), sprite_container.block_type, sprite_container.block_name.value, len(new_sprite_list)), sprite_container.pos)

        for i, sprite in enumerate(new_sprite_list):
            sprite.zoom_level = zoom_level
            sprite.bit_depth = bit_depth
            if bit_depth == 8 and isinstance(sprite, RealSprite) and (not sprite.is_empty) and sprite.mask_file is not None:
                raise generic.ScriptError("Mask file may only be specified for 32bpp sprites.", sprite.mask_file.pos)
            if first:
                if isinstance(sprite, RealSprite):
                    action_list.append(RealSpriteAction())
                else:
                    assert isinstance(sprite, RecolourSprite)
                    action_list.append(RecolourSpriteAction(sprite))
            else:
                # Not the first sprite, so an alternative sprite
                if isinstance(sprite, RecolourSprite) or isinstance(action_list[i], RecolourSpriteAction):
                    raise generic.ScriptError("Alternative sprites may only be provided for and contain real sprites, not recolour sprites.", sprite_container.pos)
                if action_list[i].sprite_list[0].is_empty and not sprite.is_empty:
                    # if the first sprite is empty, all others are ignored
                    generic.print_warning("Alternative sprites for an empty real sprite are ignored.", sprite_container.pos)
            if isinstance(sprite, RealSprite): action_list[i].add_sprite(sprite)
        first = False

    if len(action_list) != 0: action_list[-1].last = True
    return action_list

