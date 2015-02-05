# kamaki-xuser
A kamaki plugin implementing the Xtented USER Astakos API over Synnefo clouds

SETUP
=====

In the same enviroment as kamaki:

$ python setup build install
$ kamaki config set xuser_cli kamaki_xuser.cli

REQUIREMENTS
============

* A configured and running kamaki
* An admin token set as the kamaki token for this cloud

USAGE
=====

$ kamaki xuser --help
info: Info on an snf user
activate: Activate a user
deactivate: Deactivate a user
modify: Modify user information
create: Create a new SNF user
list: List snf users
newtoken: Renew user token

