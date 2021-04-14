import time
import tempfile
import os
import traceback
import logging
from datetime import datetime
from distantrs import Invocation

class results_listener:

    def __init__(self, attr):
        self.ROBOT_LISTENER_API_VERSION = 3
        self._x_start_time = {}
        self._x_logs = {}
        attr_split = attr.split("--")
        self.remote = Invocation(invocation_id=attr_split[0], auth_token=attr_split[1])


    def decorate(self, text):
        if not text:
            return ''
        indent_level = 6
        box_length = 1

        box_upper_corner = u'\u2554'.encode()
        box_horizontal_element = u'\u2550'
        box_vertical_element = u'\u2551'.encode()
        box_lower_corner = u'\u255a'.encode()

        initial_spacing = (" " * indent_level).encode()
        line_prefix = u"\n".encode() + initial_spacing + box_vertical_element + u" ".encode()
        horizontal_line = (box_horizontal_element * box_length).encode()

        return (initial_spacing + box_upper_corner + horizontal_line \
            + line_prefix \
            + line_prefix.join([x.encode() for x in text.split("\n")]) \
            + u"\n".encode() + initial_spacing + box_lower_corner + horizontal_line).decode()


    def start_test(self, data, result):
        self.remote.announce_target(data.longname.replace(" ", "_"))
        msg = "[{1}] +++++ Starting test '{0}'".format(data.longname, str(datetime.now().time()))
        self._x_start_time[data.longname] = time.time()
        self._x_logs[data.longname] = msg


    def end_test(self, data, result):
        status = ""
        if result.passed:
            status = 'OK'
        else:
            if 'skipped' in result.tags:
                status = 'skipped'
            elif 'non_critical' in result.tags:
                status = 'failed (non critical)'
            else:
                status = 'failed'

        duration = time.time() - self._x_start_time[data.longname]
        del self._x_start_time[data.longname]

        msg = "[{3}] +++++ Finished test '{0}' in {1:.2f} seconds with status {2}".format(data.longname, duration, status, str(datetime.now().time()))
        self._x_logs[data.longname] += f"\n{msg}"

        emu_state = f"output/tests/snapshots/{data.longname.replace(' ', '_')}.fail.save"
        tmp = tempfile.NamedTemporaryFile()
        with open(tmp.name, 'wb') as f:
            f.write((self._x_logs[data.longname] + '\n' + self.decorate(result.message)).encode('utf-8')) 

        if os.path.isfile(emu_state):
            self.remote.send_file(os.path.basename(emu_state), emu_state)

        rs_target = data.longname.replace(" ", "_")

        self.remote.add_log_to_target(rs_target, tmp.name)
        self.remote.finalize_target(rs_target, result.passed)
