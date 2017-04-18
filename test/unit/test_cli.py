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

from unittest.mock import patch

from populator.cli import CLI

from test.unit import CLITestCase


class TestCLI(CLITestCase):
    def test_cli_flags_prevail(self):
        c = CLI([
            'script_name',
            '--source-db-name', 'test_db_1',
            '--source-db-user', 'test_user_1',
            '--source-db-password', 'test_password_1',
            '--source-use-local-db',
        ])
        c.parse()

        self.assertEqual(c.options['source_db_name'], 'test_db_1')
        self.assertEqual(c.options['source_db_user'], 'test_user_1')
        self.assertEqual(c.options['source_db_password'], 'test_password_1')
        self.assertEqual(c.options['source_use_local_db'], True)

    def test_exclude_collections_empty(self):
        c = CLI([
            'script_name'
        ])
        c.parse()

        self.assertIsNone(c.options['source_collections_to_exclude'])

    def test_exclude_collections_one_element(self):
        c = CLI([
            'script_name',
            '--source-exclude-collection', 'abc'
        ])
        c.parse()

        self.assertListEqual(['abc'], c.options['source_collections_to_exclude'])

    def test_exclude_collections_several_elements(self):
        c = CLI([
            'script_name',
            '--source-exclude-collection', 'abc',
            '--source-exclude-collection', 'def',
            '--source-exclude-collection', 'ghi'
        ])
        c.parse()

        self.assertListEqual(['abc', 'def', 'ghi'], c.options['source_collections_to_exclude'])

    def test_cli_cwd_config_file(self):
        c = CLI([])
        c.parse()

        self.assertEqual(c.options['source_db_name'], 'test_db')
        self.assertEqual(c.options['source_db_user'], 'test_user')
        self.assertEqual(c.options['source_db_password'], 'test_password')
        self.assertEqual(c.options['source_use_local_db'], True)

    def test_local_source_ssh_destination(self):
        with patch('paramiko.client.SSHClient.connect') as mock_ssh, \
                patch('populator.source.local.LocalDbSource.get_dump_dir') as mock_dump_dir, \
                patch('populator.destination.ssh.SSHDestination._populate') as mock_populate:
            mock_dump_dir.return_value = 'dir_a', 'dir_b'
            c = CLI([])
            c.parse()

            c.run()

            mock_ssh.assert_called()
            mock_dump_dir.assert_called()
            mock_populate.assert_called()
