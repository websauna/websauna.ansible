Deploy Websauna website with Ansible.

.. contents:: :local:

Introduction
============

`See more documentation here <https://websauna.org/narrative/deployment/index.html>`_.

This is an Ansible playbook for automatically deploying a single server Websauna website from a git repository for Ubuntu 14.04 Linux. It allows you to do deploy your Websauna application to a fresh server, where you just received SSH credentials, within 30 minutes. Alternatively you can gracefully upgrade any existing running site.

Automatic installation sets up

* PostgreSQL

* Nginx

* uWSGI

* Celery

* Postfix

* Email out via Mandrill

* Supervisot startup scripts

Furthermore

* No private SSH keys are placed on a server, all SSH communication is done over SSH agent

* Websauna application files and uWSGI processes are deployment under a normal UNIX user ``wsgi``

* Firewall is set up to allow only inbound SSH, HTTP, HTTPS

* The application is deployed in the folder ``/srv/pyramid/yoursitename`` per Filesystem Hierarchy Standard

* Safely run migrations: Run database migrations first and then update codebase with compatible model files to avoid breaking an existing running site

`See documentation <https://websauna.org/narrative/deployment/index.html>`_.

production.ini
--------------

The playbook does not take the ``production.ini`` from your application package, but generates one from a template (see ``websauna.site/templates/production.ini``). If you want to customize this please override the template using a local file.

production-secrets.ini
----------------------

Secrets file for the production site is not kept in version control to avoid accidental leak of confidential credentials.To copy a secrets file to the server you need to set ``local_secrets_file``. E.g.::

    local_secrets_file: ~/myapp-production-secrets.ini

If no setting is given a dummy empty ``production-secrets.ini`` is created.

Create hosts.ini
----------------

Below is an example ``hosts.ini`` for Amazon EC2 server::

    [default]
    production ansible_ssh_host=1.2.3.4 ansible_ssh_user=ubuntu public_ip=1.2.3.4 server_name=websauna.example.com ansible_ssh_private_key_file=~/.ssh/example.pem site_id=production git_repo= git_branch=master


* Ansible connects to the server via host IP ``1.2.3.4``

* ``public_ip`` is the server IP address where HTTP/HTTPS port is bound. It may differ from SSH IP.

* ``server_name`` is for Nginx - the HTTP host we are serving

* ``site_id`` is used e.g. when generating ids for backup scripts, New Relic monitoring ids and such.

* ``git_repo`` is the Git repository of the source code of the project based on ``websauna_app`` scaffold

* ``git_branch`` is the name of the branch to deploy

Local testing
=============

With the following command a virtual server is deployed with `myapp tutorial <https://github.com/websauna/myapp>`_ from its Github repository::

    vagrant up

And to update a running VM::

    vagrant provision

