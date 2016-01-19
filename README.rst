Deploy Websauna website with Ansible.

.. contents:: :local:

Introduction
============

This is an Ansible playbook for automatically deploying a single server Websauna website from a git repository for Ubuntu 14.04 Linux. It allows you to do deploy your Websauna application to a fresh server, where you just received SSH credentials, within 30 minutes.

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

Requirements
============

Running Ansible should be possible on Windows, Linux and OSX.

Basic command line usage is required.

Installation
============

Git clone the repository from Github::

    git co git@github.com:websauna/websauna.git

Create a virtual environment for Ansible. This must be separate from any other virtual environment you are working with::

    virtualenv -p python2.7 venv
    source venv/bin/activate
    pip install ansible

.. note ::

    Ansible runs on Python 2.x for now. Ansible is a Red Hat product. Red Hat is commited to support Python 2.4 for their enterprise users. As long as Python 2.4 is supported, it is impossible to upgrade Ansible to support Python 3.x.

Install packaged roles we are going to use::

    ansible-galaxy install --roles-path=galaxy \
        ANXS.postgresql \
        Stouts.foundation \
        Stouts.nginx \
        Stouts.redis \
        Stouts.python


Create a vault with password. Vault is the secrets file where non-public configuration variables will be stored. To aovid retyping the password every time, the default password storing location is in ``~/websauna-ansible-vault.txt`` configured in ``ansible.cfg``::

    read -s pass | echo $pass > ~/websauna-ansible-vault.txt

    ansible-vault create secrets.yml

This will open your text editor and let you edit the unecrypted vault. For now you can leave it empty and just save the empty file.

Usage
=====

SSH agent forwarding
--------------------

You need to `enable SSH agent forwarding <https://opensourcehacker.com/2012/10/24/ssh-key-and-passwordless-login-basics-for-developers/>`_, so that Ansible uses your locally configured SSH key.

Usually the command is along the lines::

    ssh-add ~/.ssh/my_ssh_private_key_for_deployment

Likewise, `you need to have set up your public key on your Git repository service like Github <https://help.github.com/articles/generating-ssh-keys/>`_.

Frozen requirements
-------------------

You need to have ``requirements.txt`` file in your application root folder telling the exact version of package dependencies of your application.

Use ``pip freeze`` command to generate this.

    pip freeze > requirements.txt

After this you may need to hand edit ``requirements.txt``

Do not list your own package, like ``myapp`` in ``requirements.txt`` as it is handled specially.

If your ``pip freeze`` gives you dependency problems (incompatible packages) you can always get the latest Websauna compatible packages list from `continous integration service <https://travis-ci.org/websauna/websauna>`_ build log. Pick any successful build and ``pip freeze`` output is the very last line of build log.

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

Setting up email
================

Sign up to `mandrill.com <https://mandrill.com>`_. You get up to 12 000 monthly emails for free for reputable SMTP servers.

Add Mandrill credentils to your vault::

    ansible-vault edit secrets.yml

Add::

    mandrill_username: mikko@example.com
    mandrill_api_key: 51X5G2MFJMWKOXXXXXX

Enable ``mandrill`` in ``vars`` of your playbook::

  vars:
    - mandrill: on


`More information about Postfix and Mandrill <http://opensourcehacker.com/2013/03/26/using-postfix-and-free-mandrill-email-service-for-smtp-on-ubuntu-linux-server/>`_.

Log files
=========

Nginx logs::

    /var/www/nginx/myapp.access.log
    /var/www/nginx/myapp.error.log

Python log::

    /srv/pyramid/myapp/logs/websauna.log

Celery log::

    /srv/pyramid/myapp/logs/celery.log

Troubleshooting
===============

Manually SSH'ing in the box and checking why website doesn't start up
---------------------------------------------------------------------

SSH in to your server. If you are using Vagrant local testing you can do::

    vagrant ssh

Change to ``wsgi`` user::

    sudo -i -u wsgi

It should go directly the deployment folder, virtual environment activated::

    (venv)wsgi@vagrant-ubuntu-trusty-64:/srv/pyramid/myapp$

Test shell::

    ws-shell conf/production.ini

This will usually show import errors.


