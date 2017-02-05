# Mongo Populator
Mongo Populator is a tool that effortlessly populates a Mongo database with a dump that was extracted from somewhere else.
You can either use a local dump, a dump from another Mongo database or a dump located in Amazon S3.

 - **Supported sources**: local directory, local database (dockerized or not), remote database via SSH (dockerized or 
    not), Amazon S3 bucket.
 - **Supported destinations**: local database (dockerized or not), remote database via SSH (dockerized or not),
    Amazon S3 bucket.

**Disclaimer**: this is still under heavy development, so use it at your own risk!

## Installation
In order to install Mongo Populator, follow these steps:
 1. `git clone https://github.com/PaladinStudiosBVs/mongo-populator.git`
 2. (optional) `make tests`
 3. `sudo make install`
 4. **Note for macports users**: the executable file *mongo-populator* will be copied to
 `/opt/local/Library/Frameworks/Python.framework/Versions/Current/bin/`. So unless you have
 this directory in your PATH, you will have to create a symbolic link inside some directory
 in your PATH to the executable in the former directory.
 
## Compatibility notes
Mongo Populator is supposed to work with Python 3.3+. If you want your version of Python to be
supported, feel free to contribute to the project.
 
## Usage
    
Here are some examples of the supported use cases. I will be showing how to do it with command-line options and with
configuration file properties. I assume you will then be able to do the same with environment variables.

### From a dump in a local directory to a local Mongo database.
#### Command-line options

```
mongo-populator --source-use-local-dump \
                --source-dump-dir /path/to/dump/directory \
                --destination-use-local-db \
                --destination-db-name <db-name> \
                [--destination-db-user <db-user> \]
                [--destination-db-password <db-password> \]
                [--destination-db-restore-indexes \]
                [--destination-drop-db]
```
#### Properties in configuration file
```ini
source_use_local_dump = True
source_dump_dir = /path/to/local/dump/dir

destination_db_name = test_db
destination_db_user = test_user
destination_db_password = test_password
# mongorestore will use --noIndexRestore
destination_db_restore_indexes = False
# mongorestore will use --drop option
destination_drop_db = True

destination_use_local_db = True
```

### From a dump in a local directory to a remote Mongo database (via SSH)
#### Command-line options

```
mongo-populator   --source-use-local-dump \
                  --source-dump-dir /path/to/dump/directory \
                  --destination-use-ssh \
                  --destination-db-name <db-name> \
                  [--destination-db-user <db-user> \]
                  [--destination-db-password <db-password> \]
                  [--destination-db-restore-indexes \]
                  [--destination-drop-db \]
                  --destination-ssh-host <host> \
                  --destination-ssh-user <user> \
                  [--destintion-ssh-password <password> \]
                  [--destination-ssh-identity-file <file>]
```

#### Properties in configuration file
```ini
source_use_local_dump = True
source_dump_dir = /path/to/local/dump/dir

destination_db_name = test_db
destination_db_user = test_user
destination_db_password = test_password
# mongorestore will use --noIndexRestore
destination_db_restore_indexes = False
# mongorestore will use --drop option
destination_drop_db = True

destination_use_ssh = True
destination_ssh_host = 127.0.0.1
destination_ssh_user = ubuntu
# Password can be empty, as long as you have a key file or 
# you have an authorized key pair
destination_ssh_password =
destination_ssh_key_file = /path/to/key_file.pem
```

Note that if you specify a password, most likely you won't need to specify the identity file. The same goes for if you specify
an identity file, then you won't have to specify the password. Also if you have an authorized key pair, then you won't have
to specify neither the password or the identity file.

### From a remote Mongo database (via SSH) inside a Docker container to a remote Mongo database (via SSH)
#### Command-line options
 
```
mongo-populator --source-use-ssh \
                 --source-ssh-host 123.123.123.123 \
                 --source-ssh-user some_user \
                 [--source-ssh-password <password> \]
                 [--source-ssh-key-file /path/to/source/key_file.pem \]
                 --source-db-name source_db \
                 [--source-db-user source_user \]
                 [--source-db-password source_password \]
                 --source-is-dockerized \
                 --source-docker-container-name test_mongo \
                 --destination-use-ssh \
                 --destination-ssh-host 127.0.0.1 \
                 --destination-ssh-user ubuntu \
                 [--destination-ssh-password <password> \]
                 [--destination-ssh-key-file /path/to/key_file.pem \]
                 [--destination-drop-db \]
                 --destination-db-name test_db \
                 [--destination-db-user test_user \]
                 [--destination-db-password test_password \]
                 [--destination-db-restore-indexes \]
                 [--destination-drop-db \]
```

#### Properties in configuration file
```ini
source_db_name = source_db
source_db_user = source_user
source_db_password = source_password

source_use_ssh = True
source_ssh_host = 123.123.123.123
source_ssh_user = some_user
source_ssh_password =
source_ssh_key_file = /path/to/source/key_file.pem

source_is_dockerized = True
source_docker_container_name = test_mongo

destination_db_name = test_db
destination_db_user = test_user
destination_db_password = test_password
# mongorestore will use --noIndexRestore
destination_db_restore_indexes = False
# mongorestore will use --drop option
destination_drop_db = True

destination_use_ssh = True
destination_ssh_host = 127.0.0.1
destination_ssh_user = ubuntu
# Password can be empty, as long as you have a key file or 
# you have an authorized key pair
destination_ssh_password =
destination_ssh_key_file = /path/to/key_file.pem
```

### From an Amazon S3 bucket to a local Mongo database
Note that if you have previously configured your AWS credentials (for example, using `aws configure`), then
you don't have to specify the access key id nor the secret access key (or even the region name).

#### Command-line options
```
mongo-populator --source-use-s3 \
                [--source-s3-access-key-id <s3-access-key-id> \]
                --source s3-secret-access-key <s3-secret-access-key> \
                --source-s3-region-name <s3-region-name> \
                --source-s3-bucket <s3-bucket-name> \
                --source-s3-prefix <s3-prefix> \
                --destination-use-local-db \
                --destination-db-name <db-name> \
                [--destination-db-user <db-user> \]
                [--destination-db-password <db-password> \]
                [--destination-db-restore-indexes \]
                [--destination-drop-db]
```

#### Properties in configuration file
```ini
source_use_s3 = True
source_s3_access_key_id = access_key_id
source_s3_secret_access_key = secret_access_key
source_s3_region_name = region_name (e.g. eu-west-1)
source_s3_bucket = bucket_name
source_s3_prefix = some_prefix

destination_db_name = test_db
destination_db_user = test_user
destination_db_password = test_password
# mongorestore will use --noIndexRestore
destination_db_restore_indexes = False
# mongorestore will use --drop option
destination_drop_db = True

destination_use_local_db = True
```

### From a remote Mongo database (via SSH) to an Amazon S3 bucket
Note that if you specify an s3 prefix, files will be stored under `s3-bucket/prefix/%Y%m%d-%H%M%S/destination_db_name/`.

#### Command-line options
```
mongo-populator --source-use-ssh \
                 --source-ssh-host 123.123.123.123 \
                 --source-ssh-user some_user \
                 [--source-ssh-password <password> \]
                 [--source-ssh-key-file /path/to/source/key_file.pem \]
                 --source-db-name source_db \
                 [--source-db-user source_user \]
                 [--source-db-password source_password \]
                 --destination-db-name test_db \
                 --destination-use-s3 \
                 --destination-s3-access-key-id access_key_id \
                 --destination-s3-secret-access-key secret_access_key \
                 --destination-s3-region eu-west-1 \
                 --destination-s3-bucket bucket_name \
                 --destination-s3-prefix some_prefix
```

#### Properties in configuration file
```ini
source_db_name = source_db
source_db_user = source_user
source_db_password = source_password

source_use_ssh = True
source_ssh_host = 123.123.123.123
source_ssh_user = some_user
source_ssh_password =
source_ssh_key_file = /path/to/source/key_file.pem

destination_db_name = test_db

destination_use_s3 = True
destination_s3_access_key_id = access_key_id
destination_s3_secret_access_key = secret_access_key
destination_s3_region = region_name (e.g. eu-west-1)
destination_s3_bucket = bucket_name
destination_s3_prefix = some_prefix
```

## Command-line options
Here is a full list of command-line options:

```
-h, --help                              show this help message and exit
-v, --verbose                           verbose mode (-vvv for more)
  
Source:
  --source-db-name                      SOURCE_DB_NAME
                                        Name of the local source Database (default: None)
  --source-db-user                      SOURCE_DB_USER
                                        User to connect to source database (default: None)
  --source-db-password                  SOURCE_DB_PASSWORD
                                        Password to connect to source database (default: None)
  --source-use-local-db                 Indicates if you want to use a local database or not
                                        (default: False)
  --source-use-local-dump               Indicates if you want to use a local dump or not
                                        (default: False)
  --source-dump-dir                     SOURCE_DUMP_DIR
                                        Directory where the source dump is located (default: None)
  --source-tmp-dir                      SOURCE_TMP_DIR
                                        Directory where source dumps will be copied to
                                        (default: ~/.mongo-populator/tmp)
  --source-use-ssh                      Indicates if you want to connect to source DB via SSH
                                        (default: False)
  --source-ssh-host                     SOURCE_SSH_HOST
                                        SSH host we're connecting to if we decide to use SSH
                                        for the source (default: 127.0.0.1)
  --source-ssh-user                     SOURCE_SSH_USER
                                        SSH user to connect to source (default: None)
  --source-ssh-password                 SOURCE_SSH_PASSWORD
                                        SSH password to connect to source (default: None)
  --source-ssh-key-file                 SOURCE_SSH_KEY_FILE
                                        SSH identity file to use to connect to host (default: None)
  --source-is-dockerized                Indicates whether the source database is running
                                        inside Docker or not. (default: False)
  --source-docker-container-name        SOURCE_DOCKER_CONTAINER_NAME    
                                        The name of the Docker container where the database is
                                        running (default: None)
  --source-use-s3                       Retrieve source dump from an Amazon S3 bucket
                                        (default: False)
  --source-s3-access-key-id             SOURCE_S3_ACCESS_KEY_ID
                                        Access key to the Amazon S3 bucket (default: None)
  --source-s3-secret-access-key         SOURCE_S3_SECRET_ACCESS_KEY
                                        Secret access key to the Amazon S3 bucket (default: None)
  --source-s3-region-name               SOURCE_S3_REGION_NAME
                                        Region used by the Amazon S3 bucket (e.g. eu-west-1)
                                        (default: None)
  --source-s3-bucket                    SOURCE_S3_BUCKET
                                        Amazon S3 bucket where the dump is stored (default: None)
  --source-s3-prefix                    SOURCE_S3_PREFIX
                                        Prefix to be use when fetching objects from the S3
                                        bucket (default: None)

Destination:
  --destination-db-name                 DESTINATION_DB_NAME
                                        Name of the local destination Database (default: None)
  --destination-db-user                 DESTINATION_DB_USER
                                        User to connect to destination database (default: None)
  --destination-db-password             DESTINATION_DB_PASSWORD
                                        Password to connect to destination database (default: None)
  --destination-db-restore-indexes      Indicates whether you want to restore indexes from the
                                        dump or not (default: False)
  --destination-drop-db                 Indicates whether you want to drop the destination
                                        database (default: False)
  --destination-use-local-db            Indicates whether you want to restore a local
                                        database. (default: False)
  --destination-use-ssh                 Indicates if you want to connect via SSH to
                                        destination database. (default: False)
  --destination-ssh-host                DESTINATION_SSH_HOST
                                        SSH host we're connecting to if we decide to use SSH
                                        for the source (default: 127.0.0.1)
  --destination-ssh-user                DESTINATION_SSH_USER
                                        SSH user to connect to destination (default: None)
  --destination-ssh-password            DESTINATION_SSH_PASSWORD
                                        SSH password to connect to destination (default: None)
  --destination-ssh-key-file            DESTINATION_SSH_KEY_FILE
                                        SSH identity file to use to connect to host (default: None)
  --destination-use-s3                  Store dump in an Amazon S3 bucket (default: False)
  --destination-s3-access-key-id        DESTINATION_S3_ACCESS_KEY_ID
                                        Access key to the Amazon S3 bucket (default: None)
  --destination-s3-secret-access-key    DESTINATION_S3_SECRET_ACCESS_KEY
                                        Secret access key to the Amazon S3 bucket (default: None)
  --destination-s3-region-name          DESTINATION_S3_REGION_NAME
                                        Region used by the Amazon S3 bucket (e.g. eu-west-1) (default: None)
  --destination-s3-bucket               DESTINATION_S3_BUCKET
                                        Amazon S3 bucket where the dump will stored (default: None)
  --destination-s3-prefix               DESTINATION_S3_PREFIX
                                        Prefix to be used when storing objects in the S3 bucket (default: None)
```

## Environment variables
Instead of providing command-line options, you can define environment variables with the desired values. Note that
command-line options have the highest priority, which means that if you provide them, the corresponding values will
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

MONGO_POPULATOR_SOURCE_IS_DOCKERIZED
MONGO_POPULATOR_SOURCE_DOCKER_CONTAINER_NAME

MONGO_POPULATOR_SOURCE_USE_S3
MONGO_POPULATOR_SOURCE_S3_ACCESS_KEY_ID
MONGO_POPULATOR_SOURCE_S3_SECRET_ACCESS_KEY
MONGO_POPULATOR_SOURCE_S3_REGION_NAME
MONGO_POPULATOR_SOURCE_S3_BUCKET
MONGO_POPULATOR_SOURCE_S3_PREFIX

MONGO_POPULATOR_DESTINATION_DB_NAME
MONGO_POPULATOR_DESTINATION_DB_USER
MONGO_POPULATOR_DESTINATION_DB_PASSWORD
MONGO_POPULATOR_DESTINATION_DROP_DB
MONGO_POPULATOR_DESTINATION_DB_RESTORE_INDEXES

MONGO_POPULATOR_DESTINATION_USE_LOCAL_DB

MONGO_POPULATOR_DESTINATION_USE_SSH
MONGO_POPULATOR_DESTINATION_SSH_HOST
MONGO_POPULATOR_DESTINATION_SSH_USER
MONGO_POPULATOR_DESTINATION_SSH_PASSWORD
MONGO_POPULATOR_DESTINATION_SSH_KEY_FILE

MONGO_POPULATOR_DESTINATION_USE_S3
MONGO_POPULATOR_DESTINATION_S3_ACCESS_KEY_ID
MONGO_POPULATOR_DESTINATION_S3_SECRET_ACCESS_KEY
MONGO_POPULATOR_DESTINATION_S3_REGION_NAME
MONGO_POPULATOR_DESTINATION_S3_BUCKET
MONGO_POPULATOR_DESTINATION_S3_PREFIX

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

```ini
#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
# Unless you are using a local directory with a dump or an Amazon S3
# bucket, you'll have to fill in these. The values should be either of
# your local source database or your local
source_db_name = test_db
source_db_user = test_user
source_db_password = test_password

#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
# Set this to True if you intend to extract a dump from a database running
# locally.
source_use_local_db = True

#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
# If you want to use a dump in a local directory instead, set this to True
# and change source_dump_dir accordingly, with a path to the dump directory.
#source_use_local_dump = True
#source_dump_dir = /path/to/dump/directory

#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
# When extracting a dump from a database, mongo-populator stores it locally.
# Use this property to specify where dumps should be stored or leave it as is.
# A new dump from a database called xpto will exist in ~/.mongo-populator/tmp/%Y%m%d-%H%M%S/xpto
source_tmp_dir = ~/.mongo-populator/tmp

#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
# Set source_use_ssh to True in case you need to access your source database
# via SSH. You should also fill in the following properties with the correct values.
# If you specify a key file, most likely you won't need to specify the password,
# and vice-versa.
#source_use_ssh = False
#source_ssh_host = 127.0.0.1
#source_ssh_user =
#source_ssh_password =
#source_ssh_key_file =

#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
# Sometimes, the source database is running inside a docker container.
# In such situation, mongodump must be executed inside the container and
# the output directory must be copied from the container to the host.
source_is_dockerized = True
source_docker_container_name = test_db_container

#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
# In case you want to populate a Mongo database with a dump stored
# in Amazon S3. Note that if you have aws command-line tools and if you
# have configured your credentials using `aws configure`, then you don't
# need to fill in the access_key_id, the secret_access_key and the region,
# as long as your credentials give you access to the bucket.
#source_use_s3 = False
#source_s3_access_key_id =
#source_s3_secret_access_key =
#source_s3_region =
#source_s3_bucket =
#source_s3_prefix =

#;;;;;;;;;;;;;;;;;;;;;;;;;;;;
destination_db_name = some_db_name
destination_db_user = some_db_user
destination_db_password = some_db_password
destination_db_restore_indexes = False
destination_drop_db = True

#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
#destination_use_local_db = False

#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
destination_use_ssh = True
destination_ssh_host = 123.123.123.123
destination_ssh_user = ubuntu
destination_ssh_password =
destination_ssh_key_file = /path/to/key.pem

#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
#destination_use_s3 = False
#destination_s3_access_key_id =
#destination_s3_secret_access_key =
#destination_s3_region =
#destination_s3_bucket =
#destination_s3_prefix =

# set to 1 if you don't want colors, or export MONGO_POPULATOR_NOCOLOR=1
#nocolor = 1

[colors]
highlight = white
verbose = blue
warn = bright purple
error = red
debug = dark gray
deprecate = purple
skip = cyan
unreachable = red
ok = green
changed = yellow
diff_add = green
diff_remove = red
diff_lines = cyan
```

## TODO
 - Add the ability to specify a configuration file as a command-line argument. Something like `$ mongo-populator /path/to/file.cfg`
 - Allow custom temporary directory in remote hosts. Right now, by default it stores dumps inside `/tmp/mongodumps/`
 - Add proper logging (useful if I'm running mongo-populator as a cron job)
 - Improve tests :}
 
## License
Click on the [Link](https://github.com/PaladinStudiosBVs/mongo-populator/blob/master/COPYING) to see the full text.