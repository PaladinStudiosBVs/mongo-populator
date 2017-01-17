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

import argparse

from populator.utils.common import info, die
from populator import constants as C
from populator.source.local import LocalDumpSource, LocalDbSource
from populator.source.ssh import SSHSource
from populator.destination.local import LocalDestination
from populator.destination.ssh import SSHDestination


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
        source_group.add_argument('--source-db-name', dest='source_db_name',
                                       default=C.SOURCE_DB_NAME, action='store',
                                       help='Name of the local source Database')
        
        source_group.add_argument('--source-use-local-db', dest='source_use_local_dump',
                                  default=C.SOURCE_USE_LOCAL_DB, action='store_true',
                                  help='Indicates if you want to use a local database or not')
        source_group.add_argument('--source-use-local-dump', dest='source_use_local_dump',
                                        default=C.SOURCE_USE_LOCAL_DUMP, action='store_true',
                                        help='Indicates if you want to use a local dump or not')
        source_group.add_argument('--source-dump-dir', dest='source_dump_dir', default=C.SOURCE_DUMP_DIR,
                                        action='store',
                                        help='Directory where the source dump is located (or to create, if necessary)')

        source_group.add_argument('--source-use-ssh', dest='source_use_ssh', default=C.SOURCE_USE_SSH,
                                      action='store_true', help='Indicates if you want to connect to source DB via SSH')
        source_group.add_argument('--source-ssh-host', dest='source_ssh_host', default=C.SOURCE_SSH_HOST,
                                      action='store',
                                      help='SSH host we\'re connecting to if we decide to use SSH for the source')
        source_group.add_argument('--source-ssh-user', dest='source_ssh_user', default=C.SOURCE_SSH_USER,
                                      action='store', help='SSH user to connect to source')
        source_group.add_argument('--source-ssh-password', dest='source_ssh_password',
                                      default=C.SOURCE_SSH_PASSWORD, action='store',
                                      help='SSH password to connec to source')

        source_group.add_argument('--source-use-s3', dest='source_use_s3', default=C.SOURCE_USE_S3,
                                   action='store_true',
                                   help='Retrieve source dump from an Amazon S3 bucket')
        
        # Destination
        destination_group = parser.add_argument_group('Destination')
        destination_group.add_argument('--destination-db-name', dest='destination_db_name',
                                             default=C.DESTINATION_DB_NAME, action='store',
                                             help='Name of the local destination Database')
        
        destination_group.add_argument('--destination-use-local-db', dest='destination_use_local_db',
                                             default=C.DESTINATION_USE_LOCAL_DB, action='store_true',
                                             help='Indicates whether you want to restore a local database.')
        
        destination_group.add_argument('--destination-use-ssh', dest='destination_use_ssh',
                                           default=C.DESTINATION_USE_SSH, action='store_true',
                                           help='Indicates if you want to connect via SSH to destination database.')

        self.options = vars(parser.parse_args(self.args[1:]))
        print(self.options)
        # Any aditional transformations needed should go here
    
    def run(self):
        """
        This is where the main action happens. After having parsed the cli arguments,
        We'll check where is the source dump coming from and where is it going to.
        :return:
        """
        if C.CONFIG_FILE:
            info(f'Using {C.CONFIG_FILE} as configuration file')
        else:
            info('No configuration file found. Using default values.')
            
        # Now that we have enough info, let's see which objects do we build
        # for the source dump. Order is local dump > local db > ssh > s3
        source = None
        if self.options['source_use_local_dump']:
            source = LocalDumpSource(self.options['source_dump_dir'])
        elif self.options['source_use_local_db']:
            source = LocalDbSource(self.options['source_db_name'])
        elif self.options['source_use_ssh']:
            source = SSHSource(
                ssh_host=self.options['source_ssh_host'],
                ssh_user=self.options['source_ssh_user'],
                ssh_password=self.options['source_ssh_password']
            )
        elif self.options['source_use_s3']:
            source = None
        else:
            die('You must specify the source of your dump. Use --help')
            
        # Now let's check the destination. The order is local db > ssh
        destination = None
        if self.options['destination_use_local_db']:
            destination = LocalDestination(
                source=source,
                db_name=self.options['destination_db_name']
            )
        elif self.options['destination_use_ssh']:
            destination = SSHDestination(
                ssh_host=self.options['destination_ssh_host'],
                ssh_user=self.options['destination_ssh_user'],
                ssh_password=self.options['destination_ssh_password'],
                source=source
            )
        else:
            die('You must specify where the dump is going to. Use --help')
            
        destination.run()
