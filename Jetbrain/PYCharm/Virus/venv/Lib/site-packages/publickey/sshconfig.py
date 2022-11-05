# -*- coding:utf-8 -*-
import sys
import codecs

import jinja2
import yaml


template = jinja2.Template(u'''\
{% for id, x in items %}
Host {{ id }}
  {% if x.title %}# {{ x.title }}{% endif %}
  HostName {{ x.hostname }}
  Port {{ x.port|default(22) }}
  User {{ x.user|default('ubuntu') }}
  IdentityFile {{ x.identityfile|default('~/.ssh/id_rsa') }}
{% endfor %}
ServerAliveInterval 120
''')


def generate(config):
    text = _generate(config.filepath, config.tags)
    codecs.getwriter('utf-8')(sys.stdout).write(text)


def _generate(filepath, tags):
    with open(filepath, 'r') as fp:
        doc = yaml.safe_load(fp.read())
    items = ((name, x) for name, x in doc.items() if 'hostname' in x)
    if tags:
        criterion = set(tags)

        def filter_by_tags(iterable):
            for name, x in iterable:
                _tags = x.get('tags')
                if isinstance(_tags, basestring):
                    _tags = [_tags]
                if criterion <= set(_tags):
                    yield name, x
        items = list(filter_by_tags(items))
    return template.render(items=items)
