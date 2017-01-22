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

from populator import AmazonS3Populator
from populator.destination import MongoDestination


class AmazonS3Destination(MongoDestination, AmazonS3Populator):
    def __init__(self, s3_bucket, s3_prefix=None, s3_access_key_id=None, s3_secret_access_key=None,
                 s3_region_name=None, source=None):
        MongoDestination.__init__(self, source)
        AmazonS3Populator.__init__(
            self,
            bucket=s3_bucket,
            prefix=s3_prefix,
            aws_access_key_id=s3_access_key_id,
            aws_secret_access_key=s3_secret_access_key,
            region_name=s3_region_name
        )
    
    def _populate(self):
        pass
