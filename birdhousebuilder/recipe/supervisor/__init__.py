# -*- coding: utf-8 -*-
# Copyright (C)2014 DKRZ GmbH

"""Recipe supervisor"""

import os
from mako.template import Template

from birdhousebuilder.recipe import conda

templ_config = Template(
"""
[unix_http_server]
file=${prefix}/var/run/supervisor.sock
chmod=0700 ; socket file mode (default 0700)

[inet_http_server]
port = *:${port}
;username = admin
;password = Admin123

[supervisord]
;user=www-data
childlogdir=${prefix}/var/log/supervisor
logfile=${prefix}/var/log/supervisor/supervisord.log
pidfile=${prefix}/var/run/supervisord.pid
logfile_maxbytes=5MB
logfile_backups=10
loglevel=info
nodaemon=false
minfds=1024
minprocs=200

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]
serverurl=unix:///${prefix}/var/run/supervisor.sock

[include]
files = conf.d/*.conf
"""
)

templ_program = Template(
"""
[program:${program}]
command=${command}
directory=${directory}
priority=${priority}
autostart=${autostart}
autorestart=${autorestart}
redirect_stderr=true
environment=${environment}
"""
)

templ_start_stop = Template(filename=os.path.join(os.path.dirname(__file__), "supervisord"))

class Recipe(object):
    """This recipe is used by zc.buildout"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        b_options = buildout['buildout']
        self.anaconda_home = b_options.get('anaconda-home', conda.anaconda_home())
        bin_path = os.path.join(self.anaconda_home, 'bin')
        lib_path = os.path.join(self.anaconda_home, 'lib')
        self.tmp_path = os.path.join(self.anaconda_home, 'var', 'tmp')
        self.conda_channels = b_options.get('conda-channels')

        #self.host = b_options.get('supervisor-host', 'localhost')
        self.port = b_options.get('supervisor-port', '9001')
        
        self.program = options.get('program', name)
        self.command = options.get('command')
        self.directory =  options.get('directory', bin_path)
        self.priority = options.get('priority', '999')
        self.autostart = options.get('autostart', 'true')
        self.autorestart = options.get('autorestart', 'false')
        self.environment = options.get(
            'environment',
            'PATH="/bin:/usr/bin:%s",LD_LIBRARY_PATH="%s",PYTHON_EGG_CACHE="%s"' % (bin_path, lib_path, self.tmp_path))

    def install(self):
        installed = []
        installed += list(self.install_supervisor())
        installed += list(self.install_config())
        installed += list(self.install_program())
        installed += list(self.install_start_stop())
        return tuple()

    def install_supervisor(self):
        script = conda.Recipe(
            self.buildout,
            self.name,
            {'pkgs': 'supervisor'})
        conda.makedirs(os.path.join(self.anaconda_home, 'var', 'run'))
        conda.makedirs(os.path.join(self.anaconda_home, 'var', 'log', 'supervisor'))
        conda.makedirs(os.path.join(self.tmp_path))
        return script.install()
        
    def install_config(self):
        """
        install supervisor main config file
        """
        result = templ_config.render(
            prefix=self.anaconda_home,
            port=self.port)

        output = os.path.join(self.anaconda_home, 'etc', 'supervisor', 'supervisord.conf')
        conda.makedirs(os.path.dirname(output))
                
        try:
            os.remove(output)
        except OSError:
            pass

        with open(output, 'wt') as fp:
            fp.write(result)
        return [output]
        
    def install_program(self):
        """
        install supervisor program config file
        """
        result = templ_program.render(
            program=self.program,
            command=self.command,
            directory=self.directory,
            priority=self.priority,
            autostart=self.autostart,
            autorestart=self.autorestart,
            environment=self.environment)

        output = os.path.join(self.anaconda_home, 'etc', 'supervisor', 'conf.d', self.program + '.conf')
        conda.makedirs(os.path.dirname(output))
        
        try:
            os.remove(output)
        except OSError:
            pass

        with open(output, 'wt') as fp:
            fp.write(result)
        return [output]

    def install_start_stop(self):
        result = templ_start_stop.render(
            prefix=self.anaconda_home)
        output = os.path.join(self.anaconda_home, 'etc', 'init.d', 'supervisord')
        conda.makedirs(os.path.dirname(output))
        
        try:
            os.remove(output)
        except OSError:
            pass

        with open(output, 'wt') as fp:
            fp.write(result)
            os.chmod(output, 0o755)
        return [output]

    def update(self):
        #self.install_supervisor()
        self.install_config()
        self.install_program()
        self.install_start_stop()
        return tuple()

def uninstall(name, options):
    pass

