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

from populator import AmazonS3Populator
from populator.source import MongoSource
from populator.utils.common import info


class AmazonS3Source(MongoSource, AmazonS3Populator):
    def __init__(self, s3_bucket, s3_prefix=None, s3_access_key_id=None, s3_secret_access_key=None,
                 s3_region_name=None, tmp_dir=None, db_name=None):
        """
        todo
        :param s3_bucket:
        :param s3_prefix:
        :param s3_access_key_id:
        :param s3_secret_access_key:
        :param s3_region_name:
        :param tmp_dir:
        """
        MongoSource.__init__(self, tmp_dir)
        AmazonS3Populator.__init__(
            self,
            s3_bucket,
            prefix=s3_prefix,
            aws_access_key_id=s3_access_key_id,
            aws_secret_access_key=s3_secret_access_key,
            region_name=s3_region_name
        )
    
    def get_dump_dir(self):
        # We create the local tmp dir
        tmpdir = os.path.join(self.tmp_dir, self.prefix)
        info(
            'Creating temporary dump directory: {}'.format(tmpdir),
            color='green'
        )
        os.makedirs(tmpdir)
        
        # Now we iterate over all objects in the S3 bucket and
        # copy to the tmp dir all the objects that have a certain
        # prefix. The prefix is a way of indicating a directory tree
        # inside a bucket.
        info(
            'Copying files from S3 bucket ({})'.format(self.bucket),
            color='green'
        )
        for obj in self.bucket.objects.filter(Prefix=self.prefix):
            if not obj.key.endswith('/'):
                info('-> {}'.format(obj.key), color='dark gray')
                self.bucket.download_file(
                    obj.key,
                    os.path.join(tmpdir, obj.key.split('/')[-1])
                )
                
        return tmpdir, self.prefix
