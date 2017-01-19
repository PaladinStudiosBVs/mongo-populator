# Mongo Populator
Mongo Populator is a tool that effortlessly populates a Mongo database with a dump that was extracted from somewhere else.
You can either use a local dump, a dump from another Mongo database or a dump located in Amazon S3.

## Installation
In order to install Mongo Populator, follow these steps:
 1. `git clone https://github.com/PaladinStudiosBVs/mongo-populator.git`
 2. (optional) `make tests`
 3. `sudo make install`
 
## Usage
Here are are the current supported use cases:
### From a dump in a local directory to a local Mongo database.
```
# mongo-populator --source-use-local-dump --source-dump-dir <dump-directory> --destination-use-local-db --destination-db-name <db-name> 
```

### From a dump in a local directory to a remote Mongo database (via SSH)
```
# mongo-populator --source-use-local-dump --source-dump-dir <dump-directory> --destination-use-ssh --destination-db-name <db-name>
--destination-ssh-host <host> --destination-ssh-user <user> --destintion-ssh-password <password> --destination-ssh-identity-file <file>
```

Note that if you specify a password, most likely you won't need to specify the identity file. The same goes for if you specify
an identity file, then you won't have to specify the password. Also if you have an authorized key pair, then you won't have
to specify neither the password or the identity file.

### From a remote Mongo database (via SSH) to a remote Mongo database (via SSH)
 Snevens
```
# mongo-populator --source-use-ssh --source-ssh-host <host> --source-ssh-user <user> [--source-ssh-password <password>]
[--source-ssh-key-file <path-to-identity-file>] --source-db-name <db-name> [--source-db-user <db-user>]
[--source-db-password <db-password>] --destination-use-ssh --destination-ssh-host <host> --destination-ssh-user <user>
[--destination-ssh-password <password>] [--destination-ssh-key-file <path-to-identity-file>] [--destination-drop-db]
--destination-db-name <db-name> [--destination-db-user <db-user] [--destination-db-password <db-password>]
```

## Command-line options
Here is a full list of command-line options:

```
-h, --help                      show this help message and exit
-v, --verbose                   verbose mode (-vvv for more)
  
Source:
  --source-db-name              SOURCE_DB_NAME
                                Name of the local source Database (default: None)
  --source-db-user              SOURCE_DB_USER
                                User to connect to source database (default: None)
  --source-db-password          SOURCE_DB_PASSWORD
                                Password to connect to source database (default: None)
  --source-use-local-db         Indicates if you want to use a local database or not
                                (default: False)
  --source-use-local-dump       Indicates if you want to use a local dump or not
                                (default: True)
  --source-dump-dir             SOURCE_DUMP_DIR
                                Directory where the source dump is located (default: None)
  --source-tmp-dir              SOURCE_TMP_DIR
                                Directory where source dumps will be copied to
                                (default: /Users/pmpro/.mongo-populator/dump)
  --source-use-ssh              Indicates if you want to connect to source DB via SSH
                                (default: False)
  --source-ssh-host             SOURCE_SSH_HOST
                                SSH host we're connecting to if we decide to use SSH
                                for the source (default: 127.0.0.1)
  --source-ssh-user             SOURCE_SSH_USER
                                SSH user to connect to source (default: None)
  --source-ssh-password         SOURCE_SSH_PASSWORD
                                SSH password to connect to source (default: None)
  --source-ssh-key-file         SOURCE_SSH_KEY_FILE
                                SSH identity file to use to connect to host (default: None)
  --source-use-s3               Retrieve source dump from an Amazon S3 bucket
                                (default: False)

Destination:
  --destination-db-name         DESTINATION_DB_NAME
                                Name of the local destination Database (default: None)
  --destination-db-user         DESTINATION_DB_USER
                                User to connect to destination database (default: None)
  --destination-db-password     DESTINATION_DB_PASSWORD
                                Password to connect to destination database (default: None)
  --destination-drop-db         Indicates whether you want to drop the destination
                                database (default: True)
  --destination-use-local-db    Indicates whether you want to restore a local
                                database. (default: False)
  --destination-use-ssh         Indicates if you want to connect via SSH to
                                destination database. (default: False)
  --destination-ssh-host        DESTINATION_SSH_HOST
                                SSH host we're connecting to if we decide to use SSH
                                for the source (default: 52.209.222.134)
  --destination-ssh-user        DESTINATION_SSH_USER
                                SSH user to connect to destination (default: None)
  --destination-ssh-password    DESTINATION_SSH_PASSWORD
                                SSH password to connect to destination (default: None)
  --destination-ssh-key-file    DESTINATION_SSH_KEY_FILE
                                SSH identity file to use to connect to host (default: None)
```

## Environment variables
Instead of providing command-line options, you can define environment variables with the desired values. Note that
command-line options have the highest priority, which meands that if you provide them, the corresponding values will
be used instead. Here is a list of available environment variables that you can define:

```
MONGO_POPULATOR_SOURCE_DB_NAME
MONGO_POPULATOR_SOURCE_DB_USER
MONGO_POPULATOR_SOURCE_DB_PASSWORD
MONGO_POPULATOR_SOURCE_USE_LOCAL_DB
MONGO_POPULATOR_SOURCE_USE_LOCAL_DUMP
MONGO_POPULATOR_SOURCE_DUMP_DIR
MONGO_POPULATOR_SOURCE_TMP_DIR
MONGO_POPULATOR_SOURCE_USE_SSH
MONGO_POPULATOR_SOURCE_SSH_HOST
MONGO_POPULATOR_SOURCE_SSH_USER
MONGO_POPULATOR_SOURCE_SSH_PASSWORD
MONGO_POPULATOR_SOURCE_SSH_KEY_FILE
MONGO_POPULATOR_SOURCE_USE_S3
MONGO_POPULATOR_DESTINATION_DB_NAME
MONGO_POPULATOR_DESTINATION_DB_USER
MONGO_POPULATOR_DESTINATION_DB_PASSWORD
MONGO_POPULATOR_DESTINATION_DROP_DB
MONGO_POPULATOR_DESTINATION_USE_LOCAL_DB
MONGO_POPULATOR_DESTINATION_USE_SSH
MONGO_POPULATOR_DESTINATION_SSH_HOST
MONGO_POPULATOR_DESTINATION_SSH_USER
MONGO_POPULATOR_DESTINATION_SSH_PASSWORD
MONGO_POPULATOR_DESTINATION_SSH_KEY_FILE
MONGO_POPULATOR_FORCE_COLOR
MONGO_POPULATOR_NOCOLOR
MONGO_POPULATOR_COLOR_HIGHLIGHT
MONGO_POPULATOR_COLOR_VERBOSE
MONGO_POPULATOR_COLOR_WARN
MONGO_POPULATOR_COLOR_ERROR
MONGO_POPULATOR_COLOR_DEBUG
MONGO_POPULATOR_COLOR_DEPRECATE
MONGO_POPULATOR_COLOR_SKIP
MONGO_POPULATOR_COLOR_UNREACHABLE
MONGO_POPULATOR_COLOR_OK
MONGO_POPULATOR_COLOR_CHANGED
MONGO_POPULATOR_COLOR_DIFF_ADD
MONGO_POPULATOR_COLOR_DIFF_REMOVE
MONGO_POPULATOR_COLOR_DIFF_LINES
```

## Configuration file 
For the sake of convenience, you can have a configuration file with your desired values instead of passing command-line
options all the time. `mongo-populator` will first look up for a file called *mongo-populator.cfg* in the current working
directory. If it doesn't find, then it will try to locate *~/.mongo-populator.cfg*. On the event of not finding, it will
try to locate /etc/mongo-populator/mongo-populator.cfg. If none of these exist, then it will use default values. 
Here is an example of a configuration file:

```
[defaults]

#source_db_name =
#source_db_user =
#source_db_password =

#source_use_local_db = False
#source_use_local_dump = True
#source_dump_dir = ~/.mongo-populator/dump/
source_tmp_dir = ~/.mongo-populator/dump

#source_use_ssh = False
#source_ssh_host = 127.0.0.1
#source_ssh_user =
#source_ssh_password =
#source_ssh_key_file =

#source_use_s3 = False

#destination_db_name =
#destination_db_user =
#destination_db_password =
#destinatin_drop_db = True

#destination_use_local_db = True

#destination_use_ssh = False
#destination_ssh_host = 127.0.0.1
#destination_ssh_user =
#destination_ssh_password =
#destination_ssh_key_file =

# don't like colors?
# set to 1 if you don't want colors, or export MONGO_POPULATOR_NOCOLOR=1
#nocolor = 1

[colors]
#highlight = white
#verbose = blue
#warn = bright purple
#error = red
#debug = dark gray
#deprecate = purple
#skip = cyan
#unreachable = red
#ok = green
#changed = yellow
#diff_add = green
#diff_remove = red
#diff_lines = cyan
```

Lines startig with *#* are comments and will be ignored.
 
## License
Click on the [Link](https://github.com/PaladinStudiosBVs/mongo-populator/blob/master/COPYING) to see the full text.