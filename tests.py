from __future__ import print_function

import time

import pytest
import subprocess

import requests
import shutil
import os


EMAIL = "mikko@example.com"
PASSWORD = "Iguazu Falls 2013"

EXTRAS = """
notify_email: test@example.com
mandrill: off
cloudflare: off
pem:
"""

def print_subprocess_fail(worker, cmdline):
    print("{} output:".format(cmdline))
    print(worker.stdout.read().decode("utf-8"))
    print(worker.stderr.read().decode("utf-8"))


def execute_command(cmdline, folder=os.getcwd(), timeout=5.0):
    """Run a command in a specific folder."""
    worker = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=folder)

    try:
        worker.wait(timeout)
    except subprocess.TimeoutExpired as e:
        print_subprocess_fail(worker, cmdline)
        raise AssertionError("execute_command did not properly exit") from e

    if worker.returncode != 0:
        print_subprocess_fail(worker, cmdline)
        raise AssertionError("execute_command did not properly exit: {}".format(" ".join(cmdline)))

    return worker.stdout


@pytest.fixture(scope="module")
def myapp_vagrant(request):

    with open("local-config.yml", "wt") as f:
        f.write(EXTRAS)

    # If the vagrant box was ramped up manually before tests
    # don't recreate it... just skip directly to running tests part
    status_stdout = execute_command(["vagrant", "status"])
    running = "running (virtualbox)" in status_stdout

    if not running:
        # 10 minutes of exciting waitment
        execute_command(["vagrant", "up"], timeout=10*60)

        # We care only about things that survive restart
        execute_vagrant_command("sudo poweroff", timeout=1*60)

        execute_command(["vagrant", "up"], timeout=1*60)

        def teardown():
            execute_command(["vagrant", "destroy"])
            os.remove("local-config.yml")

        request.addfinalizer(teardown)


def execute_vagrant_command(cmd, timeout=60):
    execute_command("vagrant ssh -c '{}'".format(cmd), timeout=timeout)


def test_http(myapp_vagrant):
    resp = requests.get("http://localhost:1080")
    assert resp.status_code == 200
    assert "<h1>myapp" in resp.content


def test_http(myapp_vagrant):
    resp = requests.get("http://localhost:1043", verify=False)
    assert resp.status_code == 200
    assert "<h1>myapp" in resp.content



def test_login(browser):
    """See we can create a user from command line and sign in."""

    execute_vagrant_command("sudo -u wsgi ws-create-user conf/development.ini {} {}".format(EMAIL, PASSWORD))

    web_server = "http://localhost:1080"
    b = browser
    b.visit(web_server)

    b.find_by_css("#nav-sign-in").click()

    assert b.is_element_present_by_css("#login-form")

    b.fill("username", EMAIL)
    b.fill("password", PASSWORD)
    b.find_by_name("login_email").click()

    # After login we see a profile link to our profile
    assert b.is_element_present_by_css("#nav-logout")


def test_signup(browser):
    """See we can sign up a new user."""

    web_server = "http://localhost:1080"
    b = browser
    b.visit(web_server)

    b.find_by_css("#nav-sign-up").click()

    assert b.is_element_present_by_css("#sign-up-form")

    b.fill("email", EMAIL)
    b.fill("password", PASSWORD)
    b.fill("password-confirm", PASSWORD)

    b.find_by_name("sign_up").click()

    assert b.is_element_present_by_css("#waiting-for-activation")


def test_notebook(browser):
    """See that context sensitive shell works through Nginx."""

    web_server = "http://localhost:1080"
    b = browser
    b.visit(web_server)

    b.find_by_css("#nav-sign-in").click()

    assert b.is_element_present_by_css("#login-form")

    b.fill("username", EMAIL)
    b.fill("password", PASSWORD)
    b.find_by_name("login_email").click()

    # After login we see a profile link to our profile
    assert b.is_element_present_by_css("#nav-admin")

    b.find_by_css("#nav-admin").click()
    b.find_by_css("#latest-user-shortcut").click()
    b.find_by_css("#btn-crud-shell").click()

    # Ramping up shell takes some extended time
    time.sleep(5)

    # We succesfully exposed obj
    assert b.is_text_present("test@example.com")





