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
from populator.destination import MongoDestination
from populator.utils.common import info


class AmazonS3Destination(MongoDestination, AmazonS3Populator):
    def __init__(self, s3_bucket, s3_prefix=None, s3_access_key_id=None, s3_secret_access_key=None,
                 s3_region_name=None, source=None, db_name=None, db_user=None, db_password=None, drop_db=True):
        MongoDestination.__init__(
            self,
            source=source,
            db_name=db_name,
            db_user=db_user,
            db_password=db_password,
            drop_db=drop_db
        )
        AmazonS3Populator.__init__(
            self,
            bucket=s3_bucket,
            prefix=s3_prefix,
            aws_access_key_id=s3_access_key_id,
            aws_secret_access_key=s3_secret_access_key,
            region_name=s3_region_name
        )
    
    def _populate(self):
        self.prefix = os.path.join(
            self.prefix, datetime.now().strftime('%Y%m%d-%H%M%S'), self.source.db_name
        )
        
        info('Copying files to Amazon S3 ({}): {}'.format(self.bucket, self.prefix), color='purple')
        for file in os.listdir(self.dump_dir):
            orig_file = os.path.join(self.dump_dir, file)
            dest_file = os.path.join(self.prefix, file)
            
            info('-> {}'.format(dest_file), color='white')
            info('-> {}'.format(orig_file), color='dark gray')
            self.bucket.upload_file(
                os.path.join(self.dump_dir, file),
                os.path.join(self.prefix, file)
            )
