#!/bin/sh
#
# Block public IP access to anyone except CloudFlare and internal network
#
# https://www.cloudflare.com/ips
#
# http://rietta.com/blog/2012/09/10/using-iptables-to-require-cloudflare/
#
# Debugging: iptables -L
#
#

set -e
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -F
iptables -t mangle -X
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT
