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

class BucketObjectMock(object):
    def __init__(self, o):
        self.key = o


class S3BucketObjectsMock(object):
    def __init__(self):
        self.__objects = []

    def filter(self, Prefix=None):
        if Prefix:
            return [o for o in self.__objects if o.key.startswith(Prefix)]
        else:
            return self.__objects

    def add(self, o):
        self.__objects.append(BucketObjectMock(o))


class S3BucketMock(object):
    def __init__(self, bucket_name):
        self.objects = S3BucketObjectsMock()
        self.download_count = 0
        self.__name = bucket_name

    def __str__(self):
        return self.__name

    def __repr__(self):
        return self.__name

    def add_object(self, o):
        self.objects.add(o)

    def download_file(self, obj_key, dest):
        self.download_count += 1


class ChannelMock(object):
    def recv_exit_status(self):
        return 0


class StdoutMock(object):
    def __init__(self):
        self.channel = ChannelMock()


class SSHClientMock(object):
    def exec_command(self, cmd):
        return None, StdoutMock(), None


class SCPClientMock(object):
    def get(self, src, dest, recursive=False):
        return 0

    def put(self, src, dest, recursive=False):
        return 0

