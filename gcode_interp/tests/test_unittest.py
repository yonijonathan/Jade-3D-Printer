import pytest
from gcode_interp.lib.gcode_interpreter import GcodeExpression
import serial
import codecs


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


def test_ser_communication():
    gcode_line = 'G16 X3.00 Y14.00'
    gcode_obj = GcodeExpression()
    gcode_obj.open_port_and_send_data(b'1')


def test_checksum():
    a = GcodeExpression()
    msg = '101010101010'
    assert (a.checksum(msg, 3) == 'A0')


def test_open_port_and_send_data():
    """
    initiate communication
    """
    port = serial.Serial()

    port.port = 'COM3'
    port.baudrate = 9600
    port.open()
    port.timeout = 2
    a = 'abcde'
    b = bytes(a, encoding='utf-8')
    port.write(b)
    x = port.readline()
    port.close()
    assert x == b'abcd'


def test_format():
    gcode_line = 'G1 X3.00 Y14.00'
    gcode_obj = GcodeExpression()
    gcode_obj.parse(gcode_line)
    print(gcode_obj.format_message())
