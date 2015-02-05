"""
Copyright (c) 2015, Stavros Sachtouris
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from kamaki.cli import command
from kamaki.cli.cmds import CommandInit, errors
from kamaki.cli.cmdtree import CommandTree
from kamaki.cli.argument import (
    CommaSeparatedListArgument, ValueArgument, KeyValueArgument)
from kamaki_xuser.identity import IdentityClient
from kamaki.clients import ClientError

xuser_cmds = CommandTree('xuser', 'SNF User administrator commands')
# ldap_cmds = CommandInit('ldap', 'LDAP User commands')
namespaces = [xuser_cmds, ]


class _XuserInit(CommandInit):
    """Base class for all cuser commands"""

    @property
    def xuser(self):
        self._xuser = getattr(self, '_xuser', IdentityClient(
            self.astakos.endpoint_url, self.astakos.token))
        return self._xuser

    def user_by_email(self, email):
        for user in self.xuser.list_users():
            if user.get('email', None) == email:
                return user
        raise ClientError('Not Found', status=404)


@command(xuser_cmds)
class xuser_list(_XuserInit):
    """List snf users"""

    arguments = dict(
        select=CommaSeparatedListArgument('Keys to display', '--select'))

    @errors.Generic.all
    def _run(self):
        users = self.xuser.list_users()
        if self['select']:
            users_ = []
            for user in users:
                user_ = [u for u in user.items() if u[0] in self['select']]
                users_.append(dict(user_))
            users = users_
        self.print_list(users)

    def main(self):
        self._run()


@command(xuser_cmds)
class xuser_info(_XuserInit):
    """Info on an snf user"""

    arguments = dict(
        uuid=ValueArgument('Search by uuid', '--uuid'),
        email=ValueArgument('Search by email', '--email'),
    )
    required = ['uuid', 'email']

    @errors.Generic.all
    def _run(self):
        if self['uuid']:
            self.print_dict(self.xuser.get_user_details(self['uuid']))
        else:
            self.print_dict(self.user_by_email(self['email']))

    def main(self):
        self._run()


@command(xuser_cmds)
class xuser_create(_XuserInit):
    """Create a new SNF user"""

    arguments = dict(
        email=ValueArgument('Full name', '--email'),
        first_name=ValueArgument('First name', '--first-name'),
        last_name=ValueArgument('Last name', '--last-name'),
        affiliation=ValueArgument('Affiliation', '--affiliation'),
        metadata=KeyValueArgument('Key=Value', '--metadata'),
    )
    required = ('email', 'first_name', 'last_name', 'affiliation')

    @errors.Generic.all
    def _run(self):
        self.print_dict(self.xuser.create_user(
            self['email'],
            self['first_name'], self['last_name'],
            self['affiliation'],
            self['metadata'] or None))

    def main(self):
        self._run()


@command(xuser_cmds)
class xuser_modify(_XuserInit):
    """Modify user information"""

    arguments = dict(
        email=ValueArgument('Full name', '--email'),
        first_name=ValueArgument('First name', '--first-name'),
        last_name=ValueArgument('Last name', '--last-name'),
        affiliation=ValueArgument('Affiliation', '--affiliation'),
        metadata=KeyValueArgument('Key=Value', '--metadata'),
    )
    required = ['email', 'first_name', 'last_name', 'affiliation', 'metadata']

    @errors.Generic.all
    def _run(self, uuid):
        self.print_dict(self.xuser.modify_user(
            uuid,
            self['email'] or None,
            self['first_name'] or None, self['last_name'] or None,
            self['affiliation'] or None,
            self['metadata'] or None))

    def main(self, uuid):
        self._run(uuid)


@command(xuser_cmds)
class xuser_activate(_XuserInit):
    """Activate a user"""

    arguments = dict(
        uuid=ValueArgument('Search by uuid', '--uuid'),
        email=ValueArgument('Search by email', '--email'),
    )
    required = ['uuid', 'email']

    @errors.Generic.all
    def _run(self):
        uuid = self['uuid'] or self.user_by_email(self['email'])['id']
        self.print_dict(self.xuser.activate_user(uuid))

    def main(self):
        self._run()


@command(xuser_cmds)
class xuser_deactivate(_XuserInit):
    """Deactivate a user"""

    arguments = dict(
        uuid=ValueArgument('Search by uuid', '--uuid'),
        email=ValueArgument('Search by email', '--email'),
    )
    required = ['uuid', 'email']

    @errors.Generic.all
    def _run(self):
        uuid = self['uuid'] or self.user_by_email(self['email'])['id']
        self.print_dict(self.xuser.deactivate_user(uuid))

    def main(self):
        self._run()


@command(xuser_cmds)
class xuser_newtoken(_XuserInit):
    """Renew user token"""

    arguments = dict(
        uuid=ValueArgument('Search by uuid', '--uuid'),
        email=ValueArgument('Search by email', '--email'),
    )
    required = ['uuid', 'email']

    @errors.Generic.all
    def _run(self):
        uuid = self['uuid'] or self.user_by_email(self['email'])['id']
        self.print_dict(self.xuser.renew_user_token(uuid))

    def main(self):
        self._run()
