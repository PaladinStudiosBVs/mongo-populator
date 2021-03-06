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


import codecs

try:
    codecs.lookup_error('surrogateescape')
    HAS_SURROGATEESCAPE = True
except LookupError:
    HAS_SURROGATEESCAPE = False


def to_text(obj, encoding='utf-8', errors=None, nonstring='simplerepr'):
    if isinstance(obj, str):
        return obj

    if errors in (None, 'surrogate_or_replace'):
        if HAS_SURROGATEESCAPE:
            errors = 'surrogateescape'
        else:
            errors = 'replace'
    elif errors == 'surrogate_or_strict':
        if HAS_SURROGATEESCAPE:
            errors = 'surrogateescape'
        else:
            errors = 'strict'

    if isinstance(obj, bytes):
        return obj.decode(encoding, errors)

    # Note: We do these last even though we have to call to_text again on the
    # value because we're optimizing the common case
    if nonstring == 'simplerepr':
        try:
            value = str(obj)
        except UnicodeError:
            try:
                value = repr(obj)
            except UnicodeError:
                # Giving up
                return ''
    elif nonstring == 'passthru':
        return obj
    elif nonstring == 'empty':
        return ''
    elif nonstring == 'strict':
        raise TypeError('obj must be a string type')
    else:
        raise TypeError('Invalid value {} for to_text\'s nonstring parameter'.format(nonstring))

    return to_text(value, encoding, errors)
