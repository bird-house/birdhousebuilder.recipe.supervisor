**********************************
birdhousebuilder.recipe.supervisor
**********************************

.. contents::

Introduction
************

``birdhousebuilder.recipe.supervisor`` is a `Buildout`_ recipe to configure `Supervisor`_ services with `Anaconda`_.
This recipe is used by the `Birdhouse`_ project. 

.. _`Buildout`: http://buildout.org/
.. _`Anaconda`: http://continuum.io/
.. _`Supervisor`: http://supervisord.org/
.. _`Birdhouse`: http://bird-house.github.io/


Usage
*****

The recipe requires that Anaconda is already installed. It assumes that the default Anaconda location is in your home directory ``~/anaconda``. Otherwise you need to set the ``ANACONDA_HOME`` environment variable or the Buildout option ``anaconda-home``.

The recipe will install the ``supervisor`` package from a conda channel in a conda environment named ``birdhouse``. The location of the birdhouse environment is ``.conda/envs/birdhouse``. It deploys a supervisor configuration of a given service. The configuration will be deployed in the birdhouse enviroment ``~/.conda/envs/birdhouse/etc/supervisor/conf.d/myapp.conf``. Supervisor can be started with ``~/.conda/envs/birdhouse/etc/init.d/supervisord start``.

The recipe depends on ``birdhousebuilder.recipe.conda``.

Supported options
=================

This recipe supports the following options:

**anaconda-home**
   Buildout option with the root folder of the Anaconda installation. Default: ``$HOME/anaconda``.
   The default location can also be set with the environment variable ``ANACONDA_HOME``. Example::

     export ANACONDA_HOME=/opt/anaconda

   Search priority is:

   1. ``anaconda-home`` in ``buildout.cfg``
   2. ``$ANACONDA_HOME``
   3. ``$HOME/anaconda``

Buildout options for ``supervisord``:

**supervisor-port**
   Buildout option to set the supervisor port. Default is 9001.

**supervisor-host**
   Buildout option to set supervisor host. Default is 127.0.0.1.

**supervisor-username**
   Buildout option to set username for http monitor access. Default: None

**supervisor-password**
   Buildout option to set password for http monitor access. Default: None

**supervisor-use-monitor**
   Buildout option wheather to enable http monitor interface. Default: true

**supervisor-loglevel**
   Buildout option for supervisor log level. Default: info

Buildout part options for the program section:

**program**
   The name of the supervisor service.

**command**
   The command to start the service.

**directory**
   The directory where the command is started.

**priority**
   The priority to start service (optional). Default is 999.

**autostart**
    Start service automatically (optional). Default is ``true``.

**autorestart**
    Restart service automatically (optional). Default is ``false``.

**stdout_logfile**
    logfile for stdout (optional). Default is ``~/.conda/envs/birdhouse/var/log/supervisor/${program}.log``

**stderr_logfile**
    logfile for stderr (optional). Default is ``~/.conda/envs/birdhouse/var/log/supervisor/${program}.log``

**startsecs**
    Seconds the service needs to be online before marked as ``started`` (optional). Default is 1.

**stopwaitsecs**
    Seconds to wait before killing service (optional). Default 10.

**killasgroup**
    Kill also child processes (optional). Default ``false``.

.. note::

   The ``DAEMON_OPTS`` environment variable can be used to set additional start parameters for supervisord. 
   For example ``DAEMON_OPTS=-n`` to start supervisord in foreground.

For supervisor configuration details see the `documentation <http://supervisord.org/configuration.html>`_.

Example usage
=============

The following example ``buildout.cfg`` installs a Supervisor configuration for ``myapp`` web application::

  [buildout]
  parts = myapp

  anaconda-home = /opt/anaconda
  supervisor-host = 127.0.0.1
  supervisor-port = 9001
  supervisor-use-monitor = true

  [myapp]
  recipe = birdhousebuilder.recipe.supervisor
  program = myapp
  command = ${buildout:bin-directory}/gunicorn -b unix:///tmp/myapp.socket myapp:app 
  directory = /tmp




