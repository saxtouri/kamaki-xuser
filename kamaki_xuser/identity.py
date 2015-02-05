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

from kamaki.clients import Client


class IdentityClient(Client):
    """An Extended Identity Client"""

    def list_users(self):
        """List all users"""
        return self.get('users', success=200).json['users']

    def create_user(
            self, username, first_name, last_name, affiliation,
            metadata=None):
        """Create a new user"""
        kwargs = dict(
            username=username,
            first_name=first_name,
            last_name=last_name,
            affilication=affiliation)
        if metadata:
            kwargs['metadata'] = metadata
        # Success should be 201, but server is currently returning 200, so...
        r = self.post('users', json=dict(user=kwargs), success=(200, 201))
        return r.json['user']

    def get_user_details(self, user_id):
        """Get user details"""
        return self.get('users/%s' % user_id, success=200).json['user']

    def modify_user(
            self, user_id,
            username=None,
            first_name=None,
            last_name=None,
            affilication=None,
            password=None,
            email=None,
            metadata=None):
        """Modify User"""
        kwargs = dict()
        if username is not None:
            kwargs['username'] = username
        if first_name is not None:
            kwargs['first_name'] = first_name
        if last_name is not None:
            kwargs['last_name'] = last_name
        if affilication is not None:
            kwargs['affilication'] = affilication
        if password is not None:
            kwargs['password'] = password
        if email is not None:
            kwargs['email'] = email
        if metadata is not None:
            kwargs['metadata'] = metadata
        r = self.put('users/%s' % user_id, json=dict(user=kwargs), success=200)
        return r.json['user']

    def activate_user(self, user_id):
        """Activate a user"""
        r = self.post(
            'users/%s/action' % user_id, json=dict(activate={}), success=200)
        return r.json['user']

    def deactivate_user(self, user_id):
        """Deactivate a user"""
        r = self.post(
            'users/%s/action' % user_id, json=dict(deactivate={}), success=200)
        return r.json['user']

    def renew_user_token(self, user_id):
        """Renew user authentication token"""
        r = self.post(
            'users/%s/action' % user_id, json=dict(renewToken={}), success=200)
        return r.json['user']
