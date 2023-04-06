import re
from datetime import datetime
from dataclasses import dataclass
import hashlib
import serial

from gcode_interp.utils import util
from gcode_interp.utils.exceptions import GcodeParseError, GcodeValidationError, GcodeInterpretationError

FILE_PATH = "C:\\Users\\andre\PycharmProjects\\Jade-3D-Printer\\gcode_interp\\lib\\" \
            "Book_Display_6h42m_0.2mm_205C_PLA_ENDER3.gcode"

STEPS_PER_MM = 10
Z_STEPS_PER_MM = 5


@dataclass
class GcodeExpression:
    """
    class that parses each line in gcode file into its components, interprets each line, and has some utility methods.
    """
    GorM: str = ""
    code: int = 0
    x: float = 0
    y: float = 0
    z: float = 0
    e: float = 0
    f: float = 0
    s: float = 0

    CURR_LOCATION_X = 0.0
    CURR_LOCATION_Y = 0.0
    CURR_LOCATION_Z = 0.0

    # compile each of the regexes
    compiled_g_regex = re.compile(pattern='G\\d{1,3}')
    compiled_m_regex = re.compile(pattern='M\\d{1,3}')
    compiled_x_regex = re.compile(pattern='X(\\d+\\.\\d+)')
    compiled_y_regex = re.compile(pattern='Y(\\d+\\.\\d+)')
    compiled_z_regex = re.compile(pattern='Z(\\d+\\.\\d+)')
    compiled_e_regex = re.compile(pattern='E-{0,1}(\\d*\\.\\d+)')
    compiled_f_regex = re.compile(pattern='F(\\d+\\.\\d+)')
    compiled_s_regex = re.compile(pattern='S(\\d+\\.\\d+)')

    @classmethod
    def interpret_gcode(cls):
        code = cls.GorM + str(cls.code)
        if code not in util.gcode_dict and code not in util.mcode_dict:
            raise GcodeInterpretationError("ERROR: code %r not in dictionary" % code)
        match code:
            case 'G1':
                """ 
                linear motion, most common gcode
                need to extract x, y, z coordinates; extrusion rate
                """
                gcode = cls.GorM + str(cls.code)
            case 'M':  # is a mcode
                mcode = cls.GorM + str(cls.code)

    @classmethod
    def parse(cls, line_to_parse):
        # search each line to see if it contains any of the regexes
        searched_g_regex = re.search(cls.compiled_g_regex, line_to_parse)
        searched_m_regex = re.search(cls.compiled_m_regex, line_to_parse)
        searched_x_regex = re.search(cls.compiled_x_regex, line_to_parse)
        searched_y_regex = re.search(cls.compiled_y_regex, line_to_parse)
        searched_z_regex = re.search(cls.compiled_z_regex, line_to_parse)
        searched_e_regex = re.search(cls.compiled_e_regex, line_to_parse)
        searched_f_regex = re.search(cls.compiled_f_regex, line_to_parse)
        searched_s_regex = re.search(cls.compiled_s_regex, line_to_parse)
        gcode_exp = GcodeExpression
        # add the components to the dataclass
        if searched_g_regex is not None:
            gcode_exp.GorM = 'G'
            gcode_exp.code = line_to_parse[searched_g_regex.start() + 1:searched_g_regex.end()]
        elif searched_m_regex is not None:
            gcode_exp.GorM = 'M'
            gcode_exp.code = line_to_parse[searched_m_regex.start() + 1:searched_m_regex.end()]
        if searched_x_regex is not None:
            gcode_exp.x = float(line_to_parse[searched_x_regex.start() + 1:searched_x_regex.end()])
        if searched_y_regex is not None:
            gcode_exp.y = float(line_to_parse[searched_y_regex.start() + 1:searched_y_regex.end()])
        if searched_z_regex is not None:
            gcode_exp.z = float(line_to_parse[searched_z_regex.start() + 1:searched_z_regex.end()])
        if searched_e_regex is not None:
            gcode_exp.e = float(line_to_parse[searched_e_regex.start() + 1:searched_e_regex.end()])
        if searched_f_regex is not None:
            gcode_exp.f = float(line_to_parse[searched_f_regex.start() + 1:searched_f_regex.end()])
        if searched_s_regex is not None:
            gcode_exp.s = float(line_to_parse[searched_s_regex.start() + 1:searched_s_regex.end()])
        return gcode_exp

    @classmethod
    def validate_gcode(cls):
        curr_code = cls.GorM + str(cls.code)
        if curr_code not in util.gcode_dict and curr_code not in util.mcode_dict:
            raise GcodeValidationError

    @classmethod
    def print(cls, i):
        print(str(i) + '\t' + cls.GorM + str(cls.code))

    @classmethod
    def encode_message(cls):
        bytes_message = ''
        if cls.GorM == 'M':
            bytes_message = '{0}0'.format(bytes_message)
        else:
            bytes_message = '{0}1'.format(bytes_message)
        hex_code = hex(int(cls.code)).replace('0x', '')
        while len(hex_code) < 3:
            hex_code = '0{0}'.format(hex_code)
        bytes_message = "{0}{1}".format(bytes_message, hex_code)
        if cls.x == 0:
            bytes_message = '{0}0'.format(bytes_message)
        else:
            bytes_message = '{0}1'.format(bytes_message)
            split_x = str(cls.x).split('.')
            for i in range(len(split_x)):
                split_x[i] = hex(int(split_x[i])).replace("0x", "")

            front_count = len(split_x[0])
            back_count = len(split_x[1])
            bytes_message = "{0}{1}{2}{3}{4}".format(bytes_message, str(front_count), str(back_count), split_x[0],
                                                     split_x[1])
        if cls.y == 0:
            bytes_message = '{0}0'.format(bytes_message)
        else:
            bytes_message = '{0}1'.format(bytes_message)
            split_y = str(cls.y).split('.')
            for i in range(len(split_y)):
                split_y[i] = hex(int(split_y[i])).replace("0x", "")

            front_count = len(split_y[0])
            back_count = len(split_y[1])
            bytes_message = "{0}{1}{2}{3}{4}".format(bytes_message, str(front_count), str(back_count), split_y[0],
                                                     split_y[1])
        if cls.z == 0:
            bytes_message = '{0}0'.format(bytes_message)
        else:
            bytes_message = '{0}1'.format(bytes_message)
            split_z = str(cls.z).split('.')
            for i in range(len(split_z)):
                split_z[i] = hex(int(split_z[i])).replace("0x", "")

            front_count = len(split_z[0])
            back_count = len(split_z[1])
            bytes_message = "{0}{1}{2}{3}{4}".format(bytes_message, str(front_count), str(back_count), split_z[0],
                                                     split_z[1])
        if cls.e == 0:
            bytes_message = "{0}0".format(bytes_message)
        else:
            bytes_message = "{0}1".format(bytes_message)
            if cls.e < 0:
                bytes_message = "{0}1".format(bytes_message)
            else:
                bytes_message = "{0}0".format(bytes_message)
            split_e = str(cls.e).split(".")
            for i in range(len(split_e)):
                split_e[i] = hex(int(split_e[i])).replace("0x", "")
            front_count = len(split_e[0])
            back_count = len(split_e[1])
            bytes_message = "{0}{1}{2}{3}{4}".format(bytes_message, str(front_count), str(back_count), split_e[0],
                                                     split_e[1])
        if cls.f == 0:
            bytes_message = "{0}0".format(bytes_message)
        else:
            bytes_message = "{0}1".format(bytes_message)
            hex_rate = hex(int(cls.f))
            length = len(hex_rate)
            bytes_message = "{0}{1}{2}".format(bytes_message, length, hex_rate)

        if cls.s == 0:
            bytes_message = "{0}0".format(bytes_message)
        else:
            bytes_message = "{0}1".format(bytes_message)
            hex_temp = hex(int(cls.s))
            length = len(hex_temp)
            bytes_message = "{0}{1}{2}".format(bytes_message, length, hex_temp)
        return bytes(bytes_message)

    @classmethod
    def format_message(cls):
        """
        message format:
        nibbles of data
        first: 1 for G, 0 for M
        next 3: code num, padded with leading 0s if necessary
        each section should have a separator (*) between them
        next: parameters (0 = A, 1 = B, 2 = Z, 3 = E, 4 = F, 5 = S)
        individual parameters are followed by the number of steps required for the stepper motors when applicable
        A and B motors work together for XY motion
        next is a terminator
        checksum sent separately (before terminator added)
        e.g. G1 X70.6645 Y80.321 E.001243
        1001 0(followed by num steps) 1(followed by num steps) 3(followed by num steps)
        e.g. M140 S60
        1140 560
        """
        message = ''
        separator = '*'
        terminator = '#'
        step_inputs = cls.determine_num_steps()
        if cls.GorM == 'G':
            message = '{0}1'.format(message)
        else:
            message = '{0}0'.format(message)
        code = cls.code
        while len(code) < 3:
            code = '0{0}'.format(str(code))
        message = '{0}{1}{2}'.format(message, code, separator)
        if step_inputs[0] != 0:
            message = '{0}0{1}{2}{3}'.format(message, separator, step_inputs[0], separator)
        if step_inputs[1] != 0:
            message = '{0}1{1}{2}{3}'.format(message, separator, step_inputs[1], separator)
        if step_inputs[2] != 0:
            message = '{0}2{1}{2}{3}'.format(message, separator, step_inputs[2], separator)
        if cls.s != 0:
            message = '{0}5{1}{2}{3}'.format(message, separator, cls.s, separator)
        csum = cls.checksum(message)
        while len(message) < 55:
            message = '{0}0'.format(message)
        message = '{0}{1}'.format(message, terminator)
        return bytes(message, 'utf-8'), csum

    @classmethod
    def checksum(cls, msg):
        """calculate the MD5 checksum for the message"""
        return hashlib.md5(msg.encode("utf-8")).hexdigest()

    @classmethod
    def close_serial_port(cls, com_port):
        """
        close the serial port when finished with transmission
        """
        com_port.close()

    @classmethod
    def open_port_and_send_data(cls, bytes_msg):
        """
        initiate communication
        """
        port = serial.Serial()
        port.baudrate = 9600
        port.port = 'COM3'
        port.timeout = 2
        port.open()

        #  port.write(bytes_msg)
        port.write(bytes_msg)
        response = port.readline().decode('utf-8')
        #  port.write(checksum)
        #  checksum_response = port.readline().decode('utf-8')
        port.close()
        '''if checksum_response != 0:
            raise Exception'''
        return response

    @classmethod
    def update_curr_loc(cls, x, y, z):
        cls.CURR_LOCATION_X = x
        cls.CURR_LOCATION_Y = y
        cls.CURR_LOCATION_Z = z

    @classmethod
    def determine_num_steps(cls):
        """returns number of steps for xy motors, in """
        if not cls.GorM == 'G' or not cls.code == '1':
            t = (0.0, 0.0, 0.0)
            return t
        '''compute the next location using CURR_LOCATION and STEPS_PER_MM'''
        # num steps will be dA and dB
        # dA = dX + dY
        # dB = dX - dY

        # use cls.x and cls.y since we are using absolute coordinates
        next_x = cls.x
        next_y = cls.y
        next_z = cls.z

        if next_x == 0.0 and next_y == 0.0:
            motor_a_steps = 0.0
            motor_b_steps = 0.0

        else:
            dx = next_x - cls.CURR_LOCATION_X
            dy = next_y - cls.CURR_LOCATION_Y

            da = abs(dx + dy)
            db = abs(dx - dy)

            motor_a_steps = da * STEPS_PER_MM
            motor_b_steps = db * STEPS_PER_MM

        if next_z != 0.0:
            dz = next_z - cls.CURR_LOCATION_Z
            z_motor_steps = dz * Z_STEPS_PER_MM  # for both z motors

        else:
            z_motor_steps = 0.0
        '''
        if cls.e == prev_e or cls.e == 0.0:
            # no change in e means no flow
            e_motor_steps = 0.0

        else:
            # E (volume of filament to be extruded) is calculated as follows
            # E = (4 * h * SF * dn * l)/(pi * df^2)
            # h = layer height, SF = flow modifier (1), dn = nozzle diameter, l = length of line, df = filament diameter
            ''''''
        '''
        cls.update_curr_loc(next_x, next_y, next_z)

        t = (motor_a_steps, motor_b_steps, z_motor_steps)
        return t


if __name__ == "__main__":

    with open(FILE_PATH) as f:
        data = f.readlines()

    if not f.closed:
        f.close()

    for index, gcode_line in enumerate(data):
        if gcode_line.startswith(";") or gcode_line == '\n':
            continue
        gcode_obj = GcodeExpression().parse(gcode_line)
        gcode_obj.interpret_gcode()
        to_send = gcode_obj.format_message()
        recd = gcode_obj.open_port_and_send_data(to_send[0])
        print(recd)
