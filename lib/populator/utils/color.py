# coding=utf-8

# (c) 2017, Pedro Rodrigues <csixteen@gmail.com>
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

# https://github.com/ansible/ansible/blob/devel/lib/ansible/utils/color.py

import sys

from populator import constants as C


MONGO_POPULATOR_COLOR = True
if C.MONGO_POPULATOR_NOCOLOR:
    MONGO_POPULATOR_COLOR = False
elif not hasattr(sys.stdout, 'isatty') or not sys.stdout.isatty():
    MONGO_POPULATOR_COLOR = False
else:
    try:
        import curses
        curses.setupterm()
        if curses.tigetnum('colors') < 0:
            MONGO_POPULATOR_COLOR = False
    except curses.error:
        MONGO_POPULATOR_COLOR = False
        
if C.MONGO_POPULATOR_FORCE_COLOR:
    MONGO_POPULATOR_COLOR = True

# --- begin "pretty"
#
# pretty - A miniature library that provides a Python print and stdout
# wrapper that makes colored terminal text easier to use (e.g. without
# having to mess around with ANSI escape sequences). This code is public
# domain - there is no license except that you must leave this header.
#
# Copyright (C) 2008 Brian Nez <thedude at bri1 dot com>
#
# http://nezzen.net/2008/06/23/colored-text-in-python-using-ansi-escape-sequences/

codeCodes = {
    'black':     '0;30', 'bright gray':    '0;37',
    'blue':      '0;34', 'white':          '1;37',
    'green':     '0;32', 'bright blue':    '1;34',
    'cyan':      '0;36', 'bright green':   '1;32',
    'red':       '0;31', 'bright cyan':    '1;36',
    'purple':    '0;35', 'bright red':     '1;31',
    'yellow':    '0;33', 'bright purple':  '1;35',
    'dark gray': '1;30', 'bright yellow':  '1;33',
    'magenta':   '0;35', 'bright magenta': '1;35',
    'normal':    '0',
}


def stringc(text, color):
    """String in color."""
    if MONGO_POPULATOR_COLOR:
        return '\n'.join(['\033[%sm%s\033[0m' % (codeCodes[color], t) for t in text.split('\n')])
    else:
        return text
