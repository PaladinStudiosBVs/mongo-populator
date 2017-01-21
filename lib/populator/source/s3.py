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

from datetime import datetime
import os

from populator import AmazonS3Populator
from populator.source import MongoSource


class AmazonS3Source(MongoSource, AmazonS3Populator):
    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None, tmp_dir=None):
        MongoSource.__init__(self, tmp_dir)
        AmazonS3Populator.__init__(self, aws_access_key_id, aws_secret_access_key)
    
    def get_dump_dir(self):
        # We create the local dump dir
        i = datetime.now().strftime('%Y%m%d-%H%M%S')
        tmpdir = os.path.join(self.tmp_dir, i)
        os.makedirs(tmpdir)
        
        # Now we iterate over all
        for obj in self.bucket.objects.filter(Prefix=''):
            if not obj.key.endswith('/'):
                self.bucket.download_file(
                    obj.key, obj.key.split('/')[-1]
                )
