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

iptables -A INPUT -s 192.168.0.0/20 -p tcp --dport http -j ACCEPT
iptables -A INPUT -s 127.0.0.0/24 -p tcp --dport http -j ACCEPT

iptables -A INPUT -s 199.27.128.0/21 -p tcp --dport http -j ACCEPT
iptables -A INPUT -s 173.245.48.0/20 -p tcp --dport http -j ACCEPT
iptables -A INPUT -s 103.21.244.0/22 -p tcp --dport http -j ACCEPT
iptables -A INPUT -s 103.22.200.0/22 -p tcp --dport http -j ACCEPT
iptables -A INPUT -s 103.31.4.0/22 -p tcp --dport http -j ACCEPT
iptables -A INPUT -s 141.101.64.0/18 -p tcp --dport http -j ACCEPT
iptables -A INPUT -s 108.162.192.0/18 -p tcp --dport http -j ACCEPT
iptables -A INPUT -s 190.93.240.0/20 -p tcp --dport http -j ACCEPT
iptables -A INPUT -s 188.114.96.0/20 -p tcp --dport http -j ACCEPT
iptables -A INPUT -s 197.234.240.0/22 -p tcp --dport http -j ACCEPT
iptables -A INPUT -s 198.41.128.0/17 -p tcp --dport http -j ACCEPT
iptables -A INPUT -s 162.158.0.0/15 -p tcp --dport http -j ACCEPT
iptables -A INPUT -s 104.16.0.0/12 -p tcp --dport http -j ACCEPT

#
# CloudFlare Network has Access to Encrypted HTTPS (port 443)
#

iptables -A INPUT -s 192.168.0.0/20 -p tcp --dport https -j ACCEPT
iptables -A INPUT -s 127.0.0.0/24 -p tcp --dport https -j ACCEPT

iptables -A INPUT -s 199.27.128.0/21 -p tcp --dport https -j ACCEPT
iptables -A INPUT -s 173.245.48.0/20 -p tcp --dport https -j ACCEPT
iptables -A INPUT -s 103.21.244.0/22 -p tcp --dport https -j ACCEPT
iptables -A INPUT -s 103.22.200.0/22 -p tcp --dport https -j ACCEPT
iptables -A INPUT -s 103.31.4.0/22 -p tcp --dport https -j ACCEPT
iptables -A INPUT -s 141.101.64.0/18 -p tcp --dport https -j ACCEPT
iptables -A INPUT -s 108.162.192.0/18 -p tcp --dport https -j ACCEPT
iptables -A INPUT -s 190.93.240.0/20 -p tcp --dport https -j ACCEPT
iptables -A INPUT -s 188.114.96.0/20 -p tcp --dport https -j ACCEPT
iptables -A INPUT -s 197.234.240.0/22 -p tcp --dport https -j ACCEPT
iptables -A INPUT -s 198.41.128.0/17 -p tcp --dport https -j ACCEPT
iptables -A INPUT -s 162.158.0.0/15 -p tcp --dport https -j ACCEPT
iptables -A INPUT -s 104.16.0.0/12 -p tcp --dport https -j ACCEPT
######################################################

# General Access to the Web Server from the World
######################################################
# If we wanted to allow HTTP/HTTPS from anywhere, add this
#iptables -A INPUT -p tcp --dport http -j ACCEPT
#iptables -A INPUT -p tcp --dport https -j ACCEPT

# If we want to drop all traffic other not permitted already to HTTP and HTTPS
iptables -A INPUT -p tcp --dport http -j DROP
iptables -A INPUT -p tcp --dport https -j DROP