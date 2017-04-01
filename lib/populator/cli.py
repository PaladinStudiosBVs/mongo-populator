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

import argparse

from populator import constants as C
from populator.destination.direct import DirectDestination
from populator.destination.s3 import AmazonS3Destination
from populator.destination.ssh import SSHDestination
from populator.errors import (
    MongoPopulatorNoDockerContainerNameError,
    MongoPopulatorNoDestinationError,
    MongoPopulatorNoS3BucketError,
    MongoPopulatorNoSourceError
)
from populator.source.local import LocalDbSource, LocalDumpSource
from populator.source.s3 import AmazonS3Source
from populator.source.ssh import SSHSource
from populator.utils.common import info


class CLI(object):
    def __init__(self, args):
        self.options = None
        self.args = args

    def parse(self):
        """
        :rtype : argparse.ArgumentParser
        :return:
        """
        parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            description='''
                    Tool that populates a Mongo database with a dump that
                    can either be local, fetched from another Mongo database via SSH
                    or from an Amazon S3 bucket.
                    ''',
            epilog='''
                    Visit the website for more information: https://github.com/PaladinStudiosBVs/mongo-populator
                    '''
        )
        parser.add_argument('-v', '--verbose', dest='verbosity', default=0, action='count',
                            help='verbose mode (-vvv for more)')

        # Source
        source_group = parser.add_argument_group('Source')
        # Source DB configurations
        source_group.add_argument('--source-db-name', dest='source_db_name',
                                  default=C.SOURCE_DB_NAME, action='store',
                                  help='Name of the local source Database')
        source_group.add_argument('--source-db-user', dest='source_db_user', default=C.SOURCE_DB_USER,
                                  action='store', help='User to connect to source database')
        source_group.add_argument('--source-db-password', dest='source_db_password',
                                  default=C.SOURCE_DB_PASSWORD, action='store',
                                  help='Password to connect to source database')

        source_group.add_argument('--source-use-local-db', dest='source_use_local_db',
                                  default=C.SOURCE_USE_LOCAL_DB, action='store_true',
                                  help='Indicates if you want to use a local database or not')
        source_group.add_argument('--source-exclude-collection', dest='source_collections_to_exclude',
                                  default=None, action='append', help='Collections you want to exclude in the dump')
        # Source local dump
        source_group.add_argument('--source-use-local-dump', dest='source_use_local_dump',
                                  default=C.SOURCE_USE_LOCAL_DUMP, action='store_true',
                                  help='Indicates if you want to use a local dump or not')
        source_group.add_argument('--source-dump-dir', dest='source_dump_dir', default=C.SOURCE_DUMP_DIR,
                                  action='store',
                                  help='Directory where the source dump is located')
        # Source temporary directory for dumps
        source_group.add_argument('--source-tmp-dir', dest='source_tmp_dir', default=C.SOURCE_TMP_DIR,
                                  action='store',
                                  help='Directory where source dumps will be copied to')
        # Source SSH configurations
        source_group.add_argument('--source-use-ssh', dest='source_use_ssh', default=C.SOURCE_USE_SSH,
                                  action='store_true', help='Indicates if you want to connect to source DB via SSH')
        source_group.add_argument('--source-ssh-host', dest='source_ssh_host', default=C.SOURCE_SSH_HOST,
                                  action='store',
                                  help='SSH host we\'re connecting to if we decide to use SSH for the source')
        source_group.add_argument('--source-ssh-user', dest='source_ssh_user', default=C.SOURCE_SSH_USER,
                                  action='store', help='SSH user to connect to source')
        source_group.add_argument('--source-ssh-password', dest='source_ssh_password',
                                  default=C.SOURCE_SSH_PASSWORD, action='store',
                                  help='SSH password to connect to source')
        source_group.add_argument('--source-ssh-key-file', dest='source_ssh_key_file',
                                  default=C.SOURCE_SSH_KEY_FILE, action='store',
                                  help='SSH identity file to use to connect to host')
        # Docker
        source_group.add_argument('--source-is-dockerized', dest='source_is_dockerized', default=C.SOURCE_IS_DOCKERIZED,
                                  action='store_true',
                                  help='Indicates whether the source database is running inside Docker or not.')
        source_group.add_argument('--source-docker-container-name', dest='source_docker_container_name',
                                  default=C.SOURCE_DOCKER_CONTAINER_NAME, action='store',
                                  help='The name of the Docker container where the database is running')
        # Source Amazon S3 configurations
        source_group.add_argument('--source-use-s3', dest='source_use_s3', default=C.SOURCE_USE_S3,
                                  action='store_true',
                                  help='Retrieve source dump from an Amazon S3 bucket')
        source_group.add_argument('--source-s3-access-key-id', dest='source_s3_access_key_id',
                                  default=C.SOURCE_S3_ACCESS_KEY_ID, action='store',
                                  help='Access key to the Amazon S3 bucket')
        source_group.add_argument('--source-s3-secret-access-key', dest='source_s3_secret_access_key',
                                  default=C.SOURCE_S3_SECRET_ACCESS_KEY, action='store',
                                  help='Secret access key to the Amazon S3 bucket')
        source_group.add_argument('--source-s3-region-name', dest='source_s3_region_name',
                                  default=C.SOURCE_S3_REGION_NAME, action='store',
                                  help='Region used by the Amazon S3 bucket (e.g. eu-west-1)')
        source_group.add_argument('--source-s3-bucket', dest='source_s3_bucket',
                                  default=C.SOURCE_S3_BUCKET, action='store',
                                  help='Amazon S3 bucket where the dump is stored')
        source_group.add_argument('--source-s3-prefix', dest='source_s3_prefix',
                                  default=C.SOURCE_S3_PREFIX, action='store',
                                  help='Prefix to be use when fetching objects from the S3 bucket')

        # Destination
        destination_group = parser.add_argument_group('Destination')
        destination_group.add_argument('--destination-db-name', dest='destination_db_name',
                                       default=C.DESTINATION_DB_NAME, action='store',
                                       help='Name of the destination Database')
        destination_group.add_argument('--destination-direct-host', dest='destination_direct_host',
                                       default=C.DESTINATION_DIRECT_HOST, action='store',
                                       help='Host or connection string for the destination DB')
        destination_group.add_argument('--destination-db-user', dest='destination_db_user',
                                       default=C.DESTINATION_DB_USER,
                                       action='store', help='User to connect to destination database')
        destination_group.add_argument('--destination-db-password', dest='destination_db_password',
                                       default=C.DESTINATION_DB_PASSWORD, action='store',
                                       help='Password to connect to destination database')
        destination_group.add_argument('--destination-db-restore-indexes', dest='destination_db_restore_indexes',
                                       default=C.DESTINATION_DB_RESTORE_INDEXES, action='store_true',
                                       help='Indicates whether you want to restore indexes from the dump or not')
        destination_group.add_argument('--destination-direct-use-ssl', dest='destination_direct_use_ssl',
                                       default=C.DESTINATION_DIRECT_USE_SSL, action='store_true',
                                       help='Indicates whether you want to use SSL to connect to the DB or not')
        destination_group.add_argument('--destination-drop-db', dest='destination_drop_db',
                                       default=C.DESTINATION_DROP_DB, action='store_true',
                                       help='Indicates whether you want to drop the destination database')

        destination_group.add_argument('--destination-use-direct',
                                       dest='destination_use_direct',
                                       default=C.DESTINATION_USE_DIRECT, action='store_true',
                                       help='Indicates whether you want to use direct access to a MongoDB.')

        destination_group.add_argument('--destination-use-ssh', dest='destination_use_ssh',
                                       default=C.DESTINATION_USE_SSH, action='store_true',
                                       help='Indicates if you want to connect via SSH to destination database.')
        destination_group.add_argument('--destination-ssh-host', dest='destination_ssh_host',
                                       default=C.DESTINATION_SSH_HOST, action='store',
                                       help='SSH host we\'re connecting to if we decide to use SSH for the source')
        destination_group.add_argument('--destination-ssh-user', dest='destination_ssh_user',
                                       default=C.DESTINATION_SSH_USER, action='store',
                                       help='SSH user to connect to destination')
        destination_group.add_argument('--destination-ssh-password', dest='destination_ssh_password',
                                       default=C.DESTINATION_SSH_PASSWORD, action='store',
                                       help='SSH password to connect to destination')
        destination_group.add_argument('--destination-ssh-key-file', dest='destination_ssh_key_file',
                                       default=C.DESTINATION_SSH_KEY_FILE, action='store',
                                       help='SSH identity file to use to connect to host')
        # Destination Amazon S3 configurations
        destination_group.add_argument('--destination-use-s3', dest='destination_use_s3', default=C.DESTINATION_USE_S3,
                                       action='store_true', help='Store dump in an Amazon S3 bucket')
        destination_group.add_argument('--destination-s3-access-key-id', dest='destination_s3_access_key_id',
                                       default=C.DESTINATION_S3_ACCESS_KEY_ID, action='store',
                                       help='Access key to the Amazon S3 bucket')
        destination_group.add_argument('--destination-s3-secret-access-key', dest='destination_s3_secret_access_key',
                                       default=C.DESTINATION_S3_SECRET_ACCESS_KEY, action='store',
                                       help='Secret access key to the Amazon S3 bucket')
        destination_group.add_argument('--destination-s3-region-name', dest='destination_s3_region_name',
                                       default=C.DESTINATION_S3_REGION_NAME, action='store',
                                       help='Region used by the Amazon S3 bucket (e.g. eu-west-1)')
        destination_group.add_argument('--destination-s3-bucket', dest='destination_s3_bucket',
                                       default=C.DESTINATION_S3_BUCKET, action='store',
                                       help='Amazon S3 bucket where the dump will stored')
        destination_group.add_argument('--destination-s3-prefix', dest='destination_s3_prefix',
                                       default=C.DESTINATION_S3_PREFIX, action='store',
                                       help='Prefix to be used when storing objects in the S3 bucket')

        self.options = vars(parser.parse_args(self.args[1:]))
        # Any aditional transformations needed should go here

    def _build_kwargs(self, prefixes, replacement):
        """
        :type prefixes: list[str]
        :param prefixes: List of accepted prefixes of keys for the dictionary
        :type replacement: str
        :param replacement: Whatever we pass here will be replaced by an empty string
        :rtype: dict
        :return:
        """
        d = {k.replace(replacement, ''): v for k, v in
             list(filter(lambda x: any(map(lambda y: str.startswith(x[0], y), prefixes)), list(self.options.items())))}

        return d

    def check_containerization(self):
        if self.options['source_is_dockerized'] and not self.options['source_docker_container_name']:
            raise MongoPopulatorNoDockerContainerNameError()

    def run(self):
        """
        This is where the main action happens. After having parsed the cli arguments,
        We'll check where is the source dump coming from and where is it going to.
        :return:
        """
        if C.CONFIG_FILE:
            info('Found configuration file {}'.format(C.CONFIG_FILE), color='blue')
        else:
            info('No configuration file found. Using default values.', color='yellow')

        # Now that we have enough info, let's see which objects do we build
        # for the source dump. Order is local dump > local db > ssh > s3
        if self.options['source_use_local_dump']:
            source = LocalDumpSource(self.options['source_dump_dir'])

        elif self.options['source_use_local_db']:
            self.check_containerization()

            source = LocalDbSource(
                **self._build_kwargs(
                    [
                        'source_db',
                        'source_collections_to_exclude',
                        'source_tmp',
                        'source_is_dockerized',
                        'source_docker'
                    ],
                    'source_'
                )
            )

        elif self.options['source_use_ssh']:
            self.check_containerization()

            source = SSHSource(
                **self._build_kwargs(
                    [
                        'source_db',
                        'source_collections_to_exclude',
                        'source_ssh',
                        'source_tmp',
                        'source_is_dockerized',
                        'source_docker'
                    ],
                    'source_'
                )
            )

        elif self.options['source_use_s3']:
            if not self.options['source_s3_bucket']:
                raise MongoPopulatorNoS3BucketError()

            source = AmazonS3Source(
                **self._build_kwargs(
                    ['source_db', 'source_s3', 'source_tmp'],
                    'source_'
                )
            )

        else:
            raise MongoPopulatorNoSourceError()

        # Now let's check the destination. The order is local dump > local db > ssh > s3
        if self.options['destination_use_direct']:
            opts = self._build_kwargs(
                ['destination_db', 'destination_drop_db', 'destination_direct'],
                'destination_'
            )
            opts['source'] = source
            destination = DirectDestination(**opts)

        elif self.options['destination_use_ssh']:
            opts = self._build_kwargs(
                ['destination_db', 'destination_ssh', 'destination_drop_db'],
                'destination_'
            )
            opts['source'] = source
            destination = SSHDestination(**opts)

        elif self.options['destination_use_s3']:
            if not self.options['destination_s3_bucket']:
                raise MongoPopulatorNoS3BucketError()

            opts = self._build_kwargs(
                ['destination_s3', 'destination_db'], 'destination_'
            )
            opts['source'] = source
            destination = AmazonS3Destination(**opts)

        else:
            raise MongoPopulatorNoDestinationError()

        return destination.run()
