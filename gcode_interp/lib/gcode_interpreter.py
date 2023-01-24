import re
from datetime import datetime
from dataclasses import dataclass
from utils import util
from utils.exceptions import GcodeParseError, GcodeValidationError, GcodeInterpretationError

FILE_PATH = "/Book_Display_6h42m_0.2mm_205C_PLA_ENDER3.gcode"


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
            case _:  # is neither gcode nor mcode (is a comment or \n, most likely. should not happen)
                raise GcodeInterpretationError("ERROR: No G or M code found")

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
        return bytes_message


if __name__ == "__main__":

    start = datetime.now()

    with open(FILE_PATH) as f:
        data = f.readlines()

    if not f.closed:
        f.close()

    for index, gcode_line in enumerate(data):
        if gcode_line.startswith(";") or gcode_line == '\n':
            continue
        gcode_obj = GcodeExpression().parse(gcode_line)
        gcode_obj.interpret_gcode()
        gcode_obj.print(index)

    print('computation time = ' + str(datetime.now() - start) + 's')
