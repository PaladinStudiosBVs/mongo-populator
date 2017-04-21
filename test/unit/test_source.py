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

import os
import unittest

from unit.mock import (
    S3BucketMock,
    SCPClientMock,
    SSHClientMock
)

from populator.source.direct import DirectSource
from populator.source.s3 import AmazonS3Source
from populator.source.ssh import SSHSource


class TestSource(unittest.TestCase):
    def test_direct_source(self):
        ds = DirectSource(
            db_name='test_db',
            db_host='localhost:27017',
            db_user='test_user',
            db_password='test_password',
            db_auth='admin',
            direct_use_ssl=True
        )

        self.assertEqual(
            ds.get_dump_str(),
            'mongodump -u test_user -p test_password --db test_db --ssl -h localhost:27017 --authenticationDatabase admin --out %s'
        )

    def test_direct_source_exclude(self):
        ds = DirectSource(
            db_name='test_db',
            db_user='test_user',
            db_password='test_password',
            db_auth='admin',
            exclude=['abc', 'def']
        )

        self.assertEqual(
            ds.get_dump_str(),
            'mongodump -u test_user -p test_password --db test_db --authenticationDatabase admin --excludeCollection abc --excludeCollection def --out %s'
        )

    def test_direct_source_collection(self):
        ds = DirectSource(
            db_name='test_db',
            db_user='test_user',
            collection='abc'
        )

        self.assertEqual(
            ds.get_dump_str(),
            'mongodump -u test_user --db test_db --collection abc --out %s'
        )

    def test_direct_source_collection_prevails(self):
        ds = DirectSource(
            db_name='test_db',
            db_user='test_user',
            collection='abc',
            exclude=['abc', 'def']
        )

        self.assertEqual(
            ds.get_dump_str(),
            'mongodump -u test_user --db test_db --collection abc --out %s'
        )

    def test_ssh_source(self):
        sshs = SSHSource(
            db_name='test_db',
            db_user='test_user',
            ssh_host='127.0.0.1',
            ssh_user='ssh_user',
            tmp_dir='/tmp/mongo-populator/',
            ssh_client=SSHClientMock(),
            scp_client=SCPClientMock()
        )

        tmp_dir, prefix = sshs.get_dump_dir()
        p = os.path.join('/tmp/mongo-populator', prefix)
        self.assertEqual(tmp_dir, os.path.join(p, 'test_db'))
        self.assertTrue(os.path.exists(p))
        self.assertTrue(os.path.isdir(p))
        os.rmdir(p)

    def test_s3_source(self):
        mock_bucket = S3BucketMock('test_bucket')
        mock_bucket.add_object('test/prefix/a')
        mock_bucket.add_object('test/prefix/b')
        mock_bucket.add_object('test/prefix/c')
        mock_bucket.add_object('test/d')
        mock_bucket.add_object('prefix/e')

        s3s = AmazonS3Source(
            s3_prefix='test/prefix',
            tmp_dir='/tmp/mongo-populator/',
            bucket_obj=mock_bucket
        )

        tmpdir, prefix = s3s.get_dump_dir()

        self.assertEqual(prefix, 'test/prefix')
        self.assertTrue(os.path.exists(tmpdir))
        self.assertTrue(os.path.isdir(tmpdir))
        self.assertEqual(3, mock_bucket.download_count)

        os.rmdir(tmpdir)

