# coding=utf-8

# (c) 2017, Pedro Rodrigues <pedro@paladinstudios.com>
#
# This file is part of Mongo Populator
#
# Mongo Populator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mongo Populator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mongo Populator.  If not, see <http://www.gnu.org/licenses/>.

########################################################

import sys
import errno

from populator import constants as C
from populator.utils.text import to_text
from populator.utils.color import stringc

logger = None


def die(msg):
    print(f"[ERROR] {msg}")
    sys.exit(1)


def info(msg, color=None, stderr=False, screen_only=False, log_only=False):
    """
    https://github.com/ansible/ansible/blob/devel/lib/ansible/utils/display.py
    :param msg:
    :param color:
    :param stderr:
    :param screen_only:
    :param log_only:
    :return:
    """
    nocolor = msg
    if color:
        msg = stringc(msg, color)
        
    if not log_only:
        if not msg.endswith('\n'):
            msg2 = msg + '\n'
        else:
            msg2 = msg

        msg2 = to_text(msg2)
        if not stderr:
            fileobj = sys.stdout
        else:
            fileobj = sys.stderr

        fileobj.write(msg2)
        
        try:
            fileobj.flush()
        except IOError as e:
            # Ignore EPIPE in case fileobj has been prematurely closed, eg.
            # when piping to "head -n1"
            if e.errno != errno.EPIPE:
                raise
            
    if logger and not screen_only:
        msg2 = nocolor.lstrip('\n')
        msg2 = to_text(msg2)

        if color == C.COLOR_ERROR:
            logger.error(msg2)
        else:
            logger.info(msg2)
    
    print(f"[INFO] {msg}")
