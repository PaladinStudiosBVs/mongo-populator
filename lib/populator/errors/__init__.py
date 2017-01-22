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

from populator.utils.text import to_text


class MongoPopulatorError(Exception):
    def __init__(self, message='', obj=None, show_content=True):
        self._obj = obj
        self._show_content = show_content
        self.message = '%s' % to_text(message)

    def __str__(self):
        return self.message
    
    def __repr__(self):
        return self.message


class MongoPopulatorOptionsError(MongoPopulatorError):
    """ Bad or incomplete options passed """
    pass


class MongoPopulatorNoSourceError(MongoPopulatorError):
    """ No source dump, s3 bucket or database specified """
    pass


class MongoPopulatorNoDestinationError(MongoPopulatorError):
    """ No destination directory, s3 bucket or database specified"""
    pass


class MongoPopulatorNoS3BucketError(MongoPopulatorError):
    """
    When you want to use Amazon S3 as source or destination and don't
    specify a bucket
    """
    pass
