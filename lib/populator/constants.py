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

import os
import configparser

from populator.errors import MongoPopulatorOptionsError
from populator.utils.text import to_text

BOOL_TRUE = frozenset(['true', 't', 'y', '1', 'yes', 'on'])


def make_boolean(value):
    ret = value
    if not isinstance(value, bool):
        if value is None:
            ret = False
        else:
            ret = (str(value).lower() in BOOL_TRUE)

    return ret


def shell_expand(path, expand_relative_paths=False):
    """
    This is needed, since os.path.expanduser doesn't work
    :param path:
    :param expand_relative_paths:
    :return:
    """
    if path:
        path = os.path.expanduser(os.path.expandvars(path))
        if expand_relative_paths and not path.startswith('/'):
            # paths are always 'relative' to the config?
            if 'CONFIG_FILE' in globals():
                CFGDIR = os.path.dirname(CONFIG_FILE)
                path = os.path.join(CFGDIR, path)
            path = os.path.abspath(path)

    return path


def _get_config(p, section, key, env_var, default):
    """ helper function for get_config """
    value = default

    if p is not None:
        try:
            value = p.get(section, key, raw=True)
        except:
            pass

    if env_var is not None:
        env_value = os.environ.get(env_var, None)
        if env_value is not None:
            value = env_value

    return to_text(value, errors='surrogate_or_strict', nonstring='passthru')


def get_config(p, section, key, env_var, default, value_type=None, expand_relative_paths=False):
    """ todo """
    value = _get_config(p, section, key, env_var, default)

    if value_type == 'boolean':
        value = make_boolean(value)
    elif value:
        if value_type == 'integer':
            value = int(value)

        elif value_type == 'float':
            value = float(value)

        elif value_type == 'list':
            if isinstance(value, str):
                value = [x.strip() for x in value.split(',')]

        elif value_type == 'none':
            if value == "None":
                value = None

        elif value_type == 'path':
            value = shell_expand(value, expand_relative_paths=expand_relative_paths)

        elif value_type == 'tmppath':
            pass

    return to_text(value, errors='surrogate_or_strict', nonstring='passthru')


def load_config_file():
    """
    Loads configuration file from ENV, cwd, HOME or /etc/mongo-populator.
    The first found (in that order) is the first returned
    :return:
    """
    p = configparser.ConfigParser()

    path1 = os.getenv('MONGO_POPULATOR_CONFIG', None)
    if path1 is not None:
        path1 = os.path.expanduser(path1)
        if os.path.isdir(path1):
            path1 += '/mongo-populator.cfg'

    try:
        path2 = os.getcwd() + '/mongo-populator.cfg'
    except OSError:
        path2 = None

    path3 = os.path.expanduser('~/.mongo-populator.cfg')
    path4 = '/etc/mongo-populator/mongo-populator.cfg'

    for path in [path1, path2, path3, path4]:
        if path is not None and os.path.exists(path):
            try:
                p.read(path)
            except configparser.Error as e:
                raise MongoPopulatorOptionsError(f"Error reading config file: \n{e}")
            return p, path

    return None, ''

parser, CONFIG_FILE = load_config_file()
