# -*- coding: utf-8 -*-
# Copyright (C)2014 DKRZ GmbH

"""Recipe conda"""

from mako.template import Template

mytemplate = Template(
"""
[program:${program}]
command=${command}
directory=${directory}
priority=${priority}
autostart=true
autorestart=true
redirect_stderr=true
environment=${environment}
"""
)

class Supervisor(object):
    """This recipe is used by zc.buildout"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        b_options = buildout['buildout']
        self.anaconda_home = b_options.get('anaconda-home', '/opt/anaconda')
        self.conda_channels = b_options.get('conda-channels')

        self.program = options.get('program', name)
        self.command = options.get('command')
        self.directory =  options.get('directory', '${buildout:anaconda-home}/bin')
        self.priority = options.get('priority', '10')
        self.environment = options.get('environment', 'PATH="${buildout:anaconda-home}/bin",LD_LIBRARY_PATH="${buildout:anaconda-home}/lib"')

    def install(self):
        self.execute()
        return tuple()

    def update(self):
        self.execute()
        return tuple()

    def execute(self):
        """run the commands
        """
        content = mytemplate.render(
            program=self.program,
            command=self.command,
            directory=self.directory,
            priority=self.priority,
            environment=self.environment)
        return content

def uninstall(name, options):
    pass

