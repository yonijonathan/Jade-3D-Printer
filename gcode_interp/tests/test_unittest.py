import pytest
from lib.gcode_interpreter import GcodeExpression


def test_determine_new_location():
    gcode_line = 'G16 X3.00 Y14.00'
    gcode_obj = GcodeExpression().parse(gcode_line)
    msg = gcode_obj.encode_message()
    print(msg)
    '''
    new_loc = gcode_obj.determine_new_location()
    new_line = 'G1 X9.00 Y12.00'
    new_gcode = GcodeExpression()
    new_gcode.prev_x = new_loc[1]
    new_gcode.prev_y = new_loc[2]
    new_gcode.parse(new_line)
    print(new_gcode.determine_new_location())'''
