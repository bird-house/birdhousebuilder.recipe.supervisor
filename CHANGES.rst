Changes
*******

0.3.2 (2016-07-04)
==================

* fixed bool_options.

0.3.1 (2016-07-04)
==================

* added skip-user option.

0.3.0 (2016-06-30)
==================

* updated buildout and doctests.
* enabled travis.
* replaced conda.makedirs by os.makedirs.
* using zc.recipe.deployment.
* using run-directory.

0.2.8 (2015-12-22)
==================

* fixed use-monitor option.

0.2.7 (2015-12-22)
==================

* cleaned up configuration files.
* added more supervisord options: host, port, username, password, use_monitor.

0.2.6 (2015-12-07)
==================

* remove supervisor config files after uninstall.

0.2.5 (2015-09-21)
==================

* added DAEMON_OPTS env variable to set additional parameters when starting supervisord.

0.2.4 (2015-07-15)
==================

* added ``stopsignal`` option.
* fixed ``stopasgroup`` option.

0.2.2 (2015-06-25)
==================

* cleaned up templates.
* added user and chown option.

0.2.1 (2015-05-18)
==================

* added more options for program configuration.
* setting default logfile name for service.

0.2.0 (2015-02-24)
==================

* installing in conda enviroment ``birdhouse``.
* using ``$ANACONDA_HOME`` environment variable.
* separation of anaconda-home and installation prefix.

0.1.5 (2015-01-22)
==================

* bugfix: var/log/supervisor directory is now created.

0.1.4 (2014-12-06)
==================

* Don't update conda on buildout update.

0.1.3 (2014-07-31)
==================

* Updated documentation.

0.1.2 (2014-07-24)
==================

* Removed workaround "kill nginx".

0.1.1 (2014-07-22)
==================

* Not using supervisor-host option.

0.1.0 (2014-07-10)
==================

* Initial Release.
