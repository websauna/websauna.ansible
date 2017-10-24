Deploy Websauna website with Ansible.

.. contents:: :local:

Introduction
============

`See more documentation here <https://websauna.org/docs/narrative/deployment/index.html>`_.

This is an Ansible playbook for automatically deploying a single server Websauna website from a git repository for Ubuntu 14.04 Linux. It allows you to do deploy your Websauna application to a fresh server, where you just received SSH credentials, within 30 minutes. Alternatively you can gracefully upgrade any existing running site.

Automatic installation sets up

* PostgreSQL

* Nginx

* uWSGI

* Celery

* Email out via upstream SMTP server and locally configured Postfix

* Supervisor startup scripts

Furthermore

* No private SSH keys are placed on a server, all SSH communication is done over SSH agent

* Websauna application files and uWSGI processes are deployment under a normal UNIX user ``wsgi``

* Firewall is set up to allow only inbound SSH, HTTP, HTTPS

* The application is deployed in the folder ``/srv/pyramid/yourapplicationpackage`` per Filesystem Hierarchy Standard

* Safely run migrations: Run database migrations first and then update codebase with compatible model files to avoid breaking an existing running site

`See documentation <https://websauna.org/docs/narrative/deployment/index.html>`_.

production.ini
--------------

The playbook does not take the ``production.ini`` from your application package, but generates one from a template (see ``websauna.site/templates/production.ini``). If you want to customize this please override the template using a local file.

production-secrets.ini
----------------------

Secrets file for the production site is not kept in version control to avoid accidental leak of confidential credentials.To copy a secrets file to the server you need to set ``local_secrets_file``. E.g.::

    local_secrets_file: ~/myapp-production-secrets.ini

If no setting is given a dummy empty ``production-secrets.ini`` is created.

Local testing
=============

With the following command a virtual server is deployed with `myapp tutorial <https://github.com/websauna/myapp>`_ from its Github repository::

    vagrant up

And to update a running VM::

    vagrant provision


Issue backlog
=============

ANXS.postgresql broken:

* https://github.com/ANXS/postgresql/issues/156

setuptools broken:

* https://bitbucket.org/pypa/setuptools/issues/502/packaging-164-does-not-allow-whitepace