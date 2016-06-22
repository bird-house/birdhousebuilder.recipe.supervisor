# -*- coding: utf-8 -*-

"""Recipe supervisor"""

import os
from mako.template import Template

import logging

import zc.recipe.deployment
import birdhousebuilder.recipe.conda

templ_config = Template(filename=os.path.join(os.path.dirname(__file__), "supervisord.conf"))
templ_program = Template(filename=os.path.join(os.path.dirname(__file__), "program.conf"))
templ_start_stop = Template(filename=os.path.join(os.path.dirname(__file__), "supervisord"))

def make_dirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

class Recipe(object):
    """This recipe is used by zc.buildout.
    It installs supervisor as conda package and setups configuration."""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        b_options = buildout['buildout']

        self.name = options.get('name', name)
        self.options['name'] = self.name
        
        self.logger = logging.getLogger(self.name)

        # deployment layout
        self.deployment = zc.recipe.deployment.Install(buildout, "supervisor", {
                                                'prefix': self.options['prefix'],
                                                'user': self.options['user'],
                                                'etc-user': self.options['user']})
    
        self.options['etc_prefix'] = self.deployment.options['etc-prefix']
        self.options['var_prefix'] = self.deployment.options['var-prefix']
        self.options['etc-directory'] = self.deployment.options['etc-directory']
        self.options['log-directory'] = self.deployment.options['log-directory']
        self.prefix = self.options['prefix']

        # conda environment path
        self.conda = birdhousebuilder.recipe.conda.Recipe(self.buildout, self.name, {'pkgs': 'supervisor'})
        self.env_path = self.conda.options['env-path']
        self.options['env-path'] = self.options['env_path'] = self.env_path

        bin_path = os.path.join(self.env_path, 'bin')
        lib_path = os.path.join(self.env_path, 'lib')
        self.tmp_path = os.path.join(self.options['var_prefix'], 'tmp')
        make_dirs(self.tmp_path)

        # buildout options used for supervisord.conf
        
        self.options['host'] = b_options.get('supervisor-host', '127.0.0.1')
        self.options['port'] = b_options.get('supervisor-port', '9001')
        self.options['username'] = b_options.get('supervisor-username', '')
        self.options['password'] = b_options.get('supervisor-password', '')
        self.options['use_monitor'] = b_options.get('supervisor-use-monitor', 'true')
        self.options['chown'] = b_options.get('supervisor-chown', '')
        self.options['loglevel'] = b_options.get('supervisor-loglevel', 'info')

        # options used for program config
        
        self.program = self.options.get('program', name)
        logfile = os.path.join(self.options['log-directory'], self.program + ".log")
        # set default options
        self.options['user'] = self.options.get('user', '')
        self.options['directory'] =  self.options.get('directory', bin_path)
        self.options['priority'] = self.options.get('priority', '999')
        self.options['autostart'] = self.options.get('autostart', 'true')
        self.options['autorestart'] = self.options.get('autorestart', 'false')
        self.options['stdout_logfile'] = self.options.get('stdout_logfile', logfile)
        self.options['stderr_logfile'] = self.options.get('stderr_logfile', logfile)
        self.options['startsecs'] = self.options.get('startsecs', '1')
        self.options['numprocs'] = self.options.get('numprocs', '1')
        self.options['stopwaitsecs'] = self.options.get('stopwaitsecs', '10')
        self.options['stopasgroup'] = self.options.get('stopasgroup', 'false')
        self.options['killasgroup'] = self.options.get('killasgroup', 'true')
        self.options['stopsignal'] = self.options.get('stopsignal', 'TERM')
        self.options['environment'] = self.options.get(
            'environment',
            'PATH="/bin:/usr/bin:%s",LD_LIBRARY_PATH="%s",PYTHON_EGG_CACHE="%s"' % (bin_path, lib_path, self.tmp_path))

    def install(self, update=False):
        installed = []
        if not update:
            installed += list(self.deployment.install())
        installed += list(self.conda.install(update))
        installed += list(self.install_config())
        installed += list(self.install_program())
        installed += list(self.install_start_stop())
        return installed
     
    def install_config(self):
        """
        install supervisor main config file
        """
        text = templ_config.render(**self.options)

        conf_path = os.path.join(self.options['etc-directory'], 'supervisord.conf')
                
        with open(conf_path, 'wt') as fp:
            fp.write(text)
        return [conf_path]
        
    def install_program(self):
        """
        install supervisor program config file
        """
        text = templ_program.render(**self.options)
        conf_path = os.path.join(self.options['etc-directory'], 'conf.d', self.program + '.conf')
        make_dirs( os.path.dirname(conf_path) )
        
        with open(conf_path, 'wt') as fp:
            fp.write(text)
        return [conf_path]

    def install_start_stop(self):
        text = templ_start_stop.render(**self.options)
        conf_path = os.path.join(self.options['etc_prefix'], 'init.d', 'supervisord')
        make_dirs( os.path.dirname(conf_path) )
        
        with open(conf_path, 'wt') as fp:
            fp.write(text)
            os.chmod(conf_path, 0o755)
        return [conf_path]

    def update(self):
        return self.install(update=True)

def uninstall(name, options):
    pass

