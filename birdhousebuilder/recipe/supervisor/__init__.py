# -*- coding: utf-8 -*-
# Copyright (C)2014 DKRZ GmbH

"""Recipe conda"""

import os
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
        bin_path = os.path.join(self.anaconda_home, 'bin')
        lib_path = os.path.join(self.anaconda_home, 'lib')
        self.conda_channels = b_options.get('conda-channels')

        self.program = options.get('program', name)
        self.command = options.get('command')
        self.directory =  options.get('directory', bin_path)
        self.priority = options.get('priority', '10')
        self.environment = options.get('environment',
                                       'PATH="%s",LD_LIBRARY_PATH="%s"' % (bin_path, lib_path))

    def install(self):
        """
        install supervisor config file from template
        """
        result = mytemplate.render(
            program=self.program,
            command=self.command,
            directory=self.directory,
            priority=self.priority,
            environment=self.environment)

        output = os.path.join(self.anaconda_home, 'etc', 'supervisor', 'conf.d', self.program + '.conf')
        try:
            os.makedirs(os.path.dirname(output))
        except OSError:
            pass
        
        try:
            os.remove(output)
        except OSError:
            pass

        with open(output, 'wt') as fp:
            fp.write(result)
        return self.options.created(output)

    def update(self):
        return self.install()

def uninstall(name, options):
    pass

