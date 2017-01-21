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
    :param path:
    :param expand_relative_paths:
    :return:
    """
    if path:
        path = os.path.expanduser(os.path.expandvars(path))
        if expand_relative_paths and not path.startswith('/'):
            # paths are always 'relative' to the config?
            if 'CONFIG_FILE' in globals():
                config_dir = os.path.dirname(CONFIG_FILE)
                path = os.path.join(config_dir, path)
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
    parser = configparser.ConfigParser()

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
                parser.read(path)
            except configparser.Error as e:
                raise MongoPopulatorOptionsError(f"Error reading config file: \n{e}")
            return parser, path

    return None, ''

p, CONFIG_FILE = load_config_file()

# The defaults section in the configuration file
DEFAULTS = 'defaults'

SOURCE_DB_NAME = get_config(p, DEFAULTS, 'source_db_name', 'MONGO_POPULATOR_SOURCE_DB_NAME', None)
SOURCE_DB_USER = get_config(p, DEFAULTS, 'source_db_user', 'MONGO_POPULATOR_SOURCE_DB_USER', None)
SOURCE_DB_PASSWORD = get_config(p, DEFAULTS, 'source_db_password', 'MONGO_POPULATOR_SOURCE_DB_PASSWORD', None)

SOURCE_USE_LOCAL_DB = get_config(p, DEFAULTS, 'source_use_local_db', 'MONGO_POPULATOR_SOURCE_USE_LOCAL_DB', False, value_type='boolean')
SOURCE_USE_LOCAL_DUMP = get_config(p, DEFAULTS, 'source_use_local_dump', 'MONGO_POPULATOR_SOURCE_USE_LOCAL_DUMP', False, value_type='boolean')
SOURCE_DUMP_DIR = get_config(p, DEFAULTS, 'source_dump_dir', 'MONGO_POPULATOR_SOURCE_DUMP_DIR', '~/.mongo-populator/dump/', value_type='path')
SOURCE_TMP_DIR = get_config(p, DEFAULTS, 'source_tmp_dir', 'MONGO_POPULATOR_SOURCE_TMP_DIR', '~/.mongo-populator/tmp/', value_type='path')

SOURCE_USE_SSH = get_config(p, DEFAULTS, 'source_use_ssh', 'MONGO_POPULATOR_SOURCE_USE_SSH', False, value_type='boolean')
SOURCE_SSH_HOST = get_config(p, DEFAULTS, 'source_ssh_host', 'MONGO_POPULATOR_SOURCE_SSH_HOST', '127.0.0.1')
SOURCE_SSH_USER = get_config(p, DEFAULTS, 'source_ssh_user', 'MONGO_POPULATOR_SOURCE_SSH_USER', None)
SOURCE_SSH_PASSWORD = get_config(p, DEFAULTS, 'source_ssh_password', 'MONGO_POPULATOR_SOURCE_SSH_PASSWORD', None)
SOURCE_SSH_KEY_FILE = get_config(p, DEFAULTS, 'source_ssh_key_file', 'MONGO_POPULATOR_SOURCE_SSH_KEY_FILE', None)

SOURCE_IS_DOCKERIZED = get_config(p, DEFAULTS, 'source_is_dockerized', 'MONGO_POPULATOR_SOURCE_IS_DOCKERIZED', False, value_type='boolean')

SOURCE_USE_S3 = get_config(p, DEFAULTS, 'source_use_s3', 'MONGO_POPULATOR_SOURCE_USE_S3', False, value_type='boolean')

DESTINATION_DB_NAME = get_config(p, DEFAULTS, 'destination_db_name', 'MONGO_POPULATOR_DESTINATION_DB_NAME', None)
DESTINATION_DB_USER = get_config(p, DEFAULTS, 'destination_db_user', 'MONGO_POPULATOR_DESTINATION_DB_USER', None)
DESTINATION_DB_PASSWORD = get_config(p, DEFAULTS, 'destination_db_password', 'MONGO_POPULATOR_DESTINATION_DB_PASSWORD', None)
DESTINATION_DROP_DB = get_config(p, DEFAULTS, 'destination_drop_db', 'MONGO_POPULATOR_DESTINATION_DROP_DB', False, value_type='boolean')

DESTINATION_USE_LOCAL_DB = get_config(p, DEFAULTS, 'destination_use_local_db', 'MONGO_POPULATOR_DESTINATION_USE_LOCAL_DB', False, value_type='boolean')

DESTINATION_USE_SSH = get_config(p, DEFAULTS, 'destination_use_ssh', 'MONGO_POPULATOR_DESTINATION_USE_SSH', False, value_type='boolean')
DESTINATION_SSH_HOST = get_config(p, DEFAULTS, 'destination_ssh_host', 'MONGO_POPULATOR_DESTINATION_SSH_HOST', '127.0.0.1')
DESTINATION_SSH_USER = get_config(p, DEFAULTS, 'destination_ssh_user', 'MONGO_POPULATOR_DESTINATION_SSH_USER', None)
DESTINATION_SSH_PASSWORD = get_config(p, DEFAULTS, 'destination_ssh_password', 'MONGO_POPULATOR_DESTINATION_SSH_PASSWORD', None)
DESTINATION_SSH_KEY_FILE = get_config(p, DEFAULTS, 'destination_ssh_key_file', 'MONGO_POPULATOR_DESTINATION_SSH_KEY_FILE', None)

# Display
MONGO_POPULATOR_FORCE_COLOR = get_config(p, DEFAULTS, 'force_color', 'MONGO_POPULATOR_FORCE_COLOR', None, value_type='boolean')
MONGO_POPULATOR_NOCOLOR = get_config(p, DEFAULTS, 'nocolor', 'MONGO_POPULATOR_NOCOLOR', None, value_type='boolean')

# Colors
COLOR_HIGHLIGHT = get_config(p, 'colors', 'highlight', 'MONGO_POPULATOR_COLOR_HIGHLIGHT', 'white')
COLOR_VERBOSE = get_config(p, 'colors', 'verbose', 'MONGO_POPULATOR_COLOR_VERBOSE', 'blue')
COLOR_WARN = get_config(p, 'colors', 'warn', 'MONGO_POPULATOR_COLOR_WARN', 'bright purple')
COLOR_ERROR = get_config(p, 'colors', 'error', 'MONGO_POPULATOR_COLOR_ERROR', 'red')
COLOR_DEBUG = get_config(p, 'colors', 'debug', 'MONGO_POPULATOR_COLOR_DEBUG', 'dark gray')
COLOR_DEPRECATE = get_config(p, 'colors', 'deprecate', 'MONGO_POPULATOR_COLOR_DEPRECATE', 'purple')
COLOR_SKIP = get_config(p, 'colors', 'skip', 'MONGO_POPULATOR_COLOR_SKIP', 'cyan')
COLOR_UNREACHABLE = get_config(p, 'colors', 'unreachable', 'MONGO_POPULATOR_COLOR_UNREACHABLE', 'bright red')
COLOR_OK = get_config(p, 'colors', 'ok', 'MONGO_POPULATOR_COLOR_OK', 'green')
COLOR_CHANGED = get_config(p, 'colors', 'changed', 'MONGO_POPULATOR_COLOR_CHANGED', 'yellow')
COLOR_DIFF_ADD = get_config(p, 'colors', 'diff_add', 'MONGO_POPULATOR_COLOR_DIFF_ADD', 'green')
COLOR_DIFF_REMOVE = get_config(p, 'colors', 'diff_remove', 'MONGO_POPULATOR_COLOR_DIFF_REMOVE', 'red')
COLOR_DIFF_LINES = get_config(p, 'colors', 'diff_lines', 'MONGO_POPULATOR_COLOR_DIFF_LINES', 'cyan')
