# -*- coding: utf-8 -*-

"""Recipe supervisor"""

import os
import pwd
from mako.template import Template

import logging

from zc.buildout.buildout import bool_option
import zc.recipe.deployment
from zc.recipe.deployment import Configuration
from zc.recipe.deployment import make_dir
import birdhousebuilder.recipe.conda

templ_config = Template(filename=os.path.join(os.path.dirname(__file__), "supervisord.conf"))
templ_program = Template(filename=os.path.join(os.path.dirname(__file__), "program.conf"))
templ_start_stop = Template(filename=os.path.join(os.path.dirname(__file__), "supervisord"))

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
        def add_section(section_name, options):
            if section_name in buildout._raw:
                raise KeyError("already in buildout", section_name)
            buildout._raw[section_name] = options
            buildout[section_name] # cause it to be added to the working parts
            
        self.deployment_name = self.name + "-supervisor-deployment"
        self.deployment = zc.recipe.deployment.Install(buildout, self.deployment_name, {
            'name': "supervisor",
            'prefix': self.options.get('prefix'),
            'user': self.options.get('user'),
            'etc-user': self.options.get('etc-user')})
        add_section(self.deployment_name, self.deployment.options)

        self.options['user'] = self.deployment.options['user']
        self.options['etc-user'] = self.deployment.options['etc-user']
        self.options['etc-prefix'] = self.options['etc_prefix'] = self.deployment.options['etc-prefix']
        self.options['var-prefix'] = self.options['var_prefix'] = self.deployment.options['var-prefix']
        self.options['etc-directory'] = self.options['etc_directory'] = self.deployment.options['etc-directory']
        self.options['log-directory'] = self.options['log_directory'] = self.deployment.options['log-directory']
        self.options['run-directory'] = self.options['run_directory'] = self.deployment.options['run-directory']
        self.options['cache-directory'] = self.options['cache_directory'] = self.deployment.options['cache-directory']
        self.options['bin-directory'] = b_options['bin-directory']
        self.prefix = self.options['prefix']

        # conda environment path
        self.options['env'] = self.options.get('env', '')
        self.options['pkgs'] = self.options.get('pkgs', 'supervisor')
        self.options['channels'] = self.options.get('channels', 'defaults')
        
        self.conda = birdhousebuilder.recipe.conda.Recipe(self.buildout, self.name, {
            #'prefix': self.options.get('conda-prefix', ''),
            'env': self.options['env'],
            'pkgs': self.options['pkgs'],
            'channels': self.options['channels']})
        self.options['conda-prefix'] = self.options['conda_prefix'] = self.conda.options['prefix']

        bin_path = os.path.join(self.options['conda-prefix'], 'bin')
        lib_path = os.path.join(self.options['conda-prefix'], 'lib')

        # buildout options used for supervisord.conf
        
        self.options['host'] = b_options.get('supervisor-host', '127.0.0.1')
        self.options['port'] = b_options.get('supervisor-port', '9001')
        self.options['username'] = b_options.get('supervisor-username', '')
        self.options['password'] = b_options.get('supervisor-password', '')
        self.options['use-monitor'] = self.options['use_monitor'] = bool_option(b_options, 'supervisor-use-monitor', True)
        self.options['loglevel'] = b_options.get('supervisor-loglevel', 'info')

        # options used for program config
        
        self.program = self.options.get('program', name)
        logfile = os.path.join(self.options['log-directory'], self.program + ".log")
        # set default options
        self.options['skip-user'] = self.options['skip_user'] = bool_option(self.options, 'skip-user', False)
        self.options['directory'] =  self.options.get('directory', bin_path)
        self.options['priority'] = self.options.get('priority', '999')
        self.options['autostart'] = self.options.get('autostart', 'true')
        self.options['autorestart'] = self.options.get('autorestart', 'false')
        self.options['stdout-logfile'] = self.options['stdout_logfile'] = self.options.get('stdout-logfile', logfile)
        self.options['stderr-logfile'] = self.options['stderr_logfile'] = self.options.get('stderr-logfile', logfile)
        self.options['startsecs'] = self.options.get('startsecs', '1')
        self.options['numprocs'] = self.options.get('numprocs', '1')
        self.options['stopwaitsecs'] = self.options.get('stopwaitsecs', '10')
        self.options['stopasgroup'] = self.options.get('stopasgroup', 'false')
        self.options['killasgroup'] = self.options.get('killasgroup', 'true')
        self.options['stopsignal'] = self.options.get('stopsignal', 'TERM')
        self.options['environment'] = self.options.get(
            'environment',
            'PATH="/bin:/usr/bin:%s",LD_LIBRARY_PATH="%s",PYTHON_EGG_CACHE="%s"' % (bin_path, lib_path, self.options['cache-directory']))

    def install(self, update=False):
        installed = []
        if not update:
            installed += list(self.deployment.install())
        installed += list(self.conda.install(update))
        installed += list(self.install_config())
        installed += list(self.install_program())
        installed += list(self.install_start_stop())
        installed += list(self.install_supervisord())
        installed += list(self.install_supervisorctl())
        return installed
     
    def install_config(self):
        """
        install supervisor main config file
        """
        text = templ_config.render(**self.options)
        config = Configuration(self.buildout, 'supervisord.conf', {
            'deployment': self.deployment_name,
            'text': text})
        return [config.install()]
        
    def install_program(self):
        """
        install supervisor program config file
        """
        text = templ_program.render(**self.options)
        config = Configuration(self.buildout, self.program + '.conf', {
            'deployment': self.deployment_name,
            'directory': os.path.join(self.options['etc-directory'], 'conf.d'),
            'text': text})
        return [config.install()]

    def install_start_stop(self):
        text = templ_start_stop.render(**self.options)
        config = Configuration(self.buildout, 'supervisord', {
            'deployment': self.deployment_name,
            'directory': os.path.join(self.options['etc-prefix'], 'init.d'),
            'text': text})
        configfile = config.install()
        os.chmod(configfile, 0o755)
        return [configfile]

    def install_supervisord(self):
        script = 'supervisord'
        source = os.path.join(self.options['etc-prefix'], 'init.d', script)
        target = os.path.join(self.options['bin-directory'], script)
        if not os.path.exists(target):
            os.symlink(source, target)
        return [target]

    def install_supervisorctl(self):
        conf_file = os.path.join(self.options['etc-directory'], 'supervisord.conf')
        init_stmt = 'import sys; sys.argv[1:1] = ["-c", "{0}"]'.format(conf_file)
        ctlscript = zc.recipe.egg.Egg(
            self.buildout,
            self.name, {
                'eggs': 'supervisor',
                'scripts': 'supervisorctl=supervisorctl',
                'initialization': init_stmt,
                'arguments': 'sys.argv[1:]',
                })
        return ctlscript.install()

    def update(self):
        return self.install(update=True)

def uninstall(name, options):
    pass

