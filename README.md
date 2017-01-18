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

### From a dump in a local directory to a Mongo database that you must connect via SSH
```
# mongo-populator --source-use-local-dump --source-dump-dir <dump-directory> --destination-use-ssh --destination-db-name <db-name>
--destination-ssh-host <host> --destination-ssh-user <user> --destintion-ssh-password <password> --destination-ssh-identity-file <file>
```

Note that if you specify a password, most likely you won't need to specify the identity file. The same goes for if you specify
an identity file, then you won't have to specify the password. Also if you have an authorized key pair, then you won't have
to specify neither the password or the identity file.
 
## License
Click on the [Link](https://github.com/PaladinStudiosBVs/mongo-populator/blob/master/COPYING) to see the full text.