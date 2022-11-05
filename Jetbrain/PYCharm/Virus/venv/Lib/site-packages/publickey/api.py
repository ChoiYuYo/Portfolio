# -*- coding:utf-8 -*-
import sys
from os.path import expanduser
from contextlib import closing
from tempfile import NamedTemporaryFile

import paramiko
import yaml
import requests


def put_authorized_keys(config):
    keyfile = config.keyfile
    filepath = config.filepath
    host = config.host
    assert bool(keyfile) ^ bool(filepath)
    if not keyfile:
        temp = NamedTemporaryFile()
        download_from_github(config, dest=temp)
        temp.seek(0)
        keyfile = temp.name
    with open(expanduser('~/.ssh/config'), 'r') as fp:
        config = paramiko.SSHConfig()
        config.parse(fp)

    with closing(paramiko.SSHClient()) as client:
        client.load_host_keys(expanduser('~/.ssh/known_hosts'))
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        _, params = config.lookup(host), {}

        def value_if(x, y, func=None):
            if x in _:
                params[y] = _[x] if not func else func(_[x])

        value_if('hostname', 'hostname')
        value_if('user', 'username')
        value_if('port', 'port', int)

        client.connect(**params)
        with closing(client.open_sftp()) as sftp:
            sftp.put(keyfile, '.ssh/authorized_keys')


def download_from_github(config, dest=None):
    if not dest:
        dest = sys.stdout

    filepath, host = config.filepath, config.host
    with open(filepath, 'r') as fp:
        doc = yaml.safe_load(fp.read())

    def _members(host):
        data = doc[host]
        assert 'members' in data
        return data['members']

    members = _members(host)
    for member in members:
        url = 'https://github.com/{0}.keys'.format(member)
        with closing(requests.get(url)) as response:
            assert response.ok
            items = enumerate(response.text.split('\n'), start=1)
            for number, line in items:
                dest.write('{0} {1}@github.com.{2}\n'.format(
                    line, member, number
                ))
