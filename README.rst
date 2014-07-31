**********************************
birdhousebuilder.recipe.supervisor
**********************************

.. contents::

Introduction
************

``birdhousebuilder.recipe.supervisor`` is a `Buildout`_ recipe to configure `Supervisor`_ services with `Anaconda`_.

Birdhousebuilder recipes are used to build Web Processing Service components (Phoenix, Malleefowl, Nighthawk, FlyingPigeon, ...) of the ClimDaPs project. All Birdhousebuilder recipes need an existing `Anaconda`_ installation.  


.. _`Buildout`: http://buildout.org/
.. _`Anaconda`: http://continuum.io/
.. _`Supervisor`: http://supervisord.org/

Usage
*****

The recipe requires that Anaconda is already installed. It assumes that Anaconda is installed at the default location in your home directory ``~/anaconda``. Otherwise you need to set the Buildout option ``anaconda-home``.

The recipe will install the ``supervisor`` package from a conda channel and deploy a supervisor configuration of a given service. The configuration will be deployed in ``~/anaconda/etc/supervisor/conf.d/myapp.conf``. Supervisor can be started with ``~/anaconda/etc/init.d/supervisord start``.

The recipe depends on ``birdhousebuilder.recipe.conda``.

Supported options
=================

This recipe supports the following options:

``anaconda-home``
   Buildout option with the root folder of the Anaconda installation. Default: ``$HOME/anaconda``.

``supervisor-port``
   Buildout option (optional) to set the supervisor port. Default is 9001 (http://localhost:9001).

``program``
   The name of the supervisor service.

``command``
   The command to start the service.

``directory``
   The directory where the command is started.

Example usage
=============

The following example ``buildout.cfg`` installs a Supervisor configuration for ``myapp`` web application::

  [buildout]
  parts = myapp

  anaconda-home = /home/myself/anaconda
  supervisor-port = 9001

  [myapp]
  recipe = birdhousebuilder.recipe.supervisor
  program = myapp
  command = ${buildout:bin-directory}/gunicorn -b unix:///tmp/myapp.socket myapp:app 
  directory = /tmp




