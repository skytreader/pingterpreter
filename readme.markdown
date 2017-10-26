# pingterpreter

Humanize ping output and tell whether your connection is doing fine or what.

## Sample usage

Clone this repo then add the script to your `$PATH` (or just cd to the repo)
then

```
$ ping google.com | pingterpreter.py
```

## Compatibility

This script is guaranteed to work as invoked above on Ubuntu 16.04. `ping`
flags which might modify the output format are not take into account nor are
the output formats of other `ping` implementations.

## Sample output:

```
You're on a roll. 21 (243 total recv) icmp packets in a row and 91ms mean for the last 8 packets.
You're on a roll. 22 (244 total recv) icmp packets in a row and 91ms mean for the last 8 packets.
You're on a roll. 23 (245 total recv) icmp packets in a row and 93ms mean for the last 8 packets.
You're on a roll. 24 (246 total recv) icmp packets in a row and 93ms mean for the last 8 packets.
We're hitting a rough patch here. 93ms mean for the last 8 packets.
You're on a roll. 1 (249 total recv) icmp packets in a row and 93ms mean for the last 8 packets.
You're on a roll. 2 (250 total recv) icmp packets in a row and 93ms mean for the last 8 packets.
You're on a roll. 3 (251 total recv) icmp packets in a row and 94ms mean for the last 8 packets.
You're on a roll. 4 (252 total recv) icmp packets in a row and 94ms mean for the last 8 packets.
You're on a roll. 5 (253 total recv) icmp packets in a row and 94ms mean for the last 8 packets.
We're hitting a rough patch here. 91ms mean for the last 8 packets.
You're on a roll. 1 (256 total recv) icmp packets in a row and 91ms mean for the last 8 packets.
You're on a roll. 2 (257 total recv) icmp packets in a row and 91ms mean for the last 8 packets.
We're hitting a rough patch here. 91ms mean for the last 8 packets.
You're on a roll. 1 (260 total recv) icmp packets in a row and 91ms mean for the last 8 packets.
You're on a roll. 2 (261 total recv) icmp packets in a row and 92ms mean for the last 8 packets.
You're on a roll. 3 (262 total recv) icmp packets in a row and 92ms mean for the last 8 packets.
You're on a roll. 4 (263 total recv) icmp packets in a row and 92ms mean for the last 8 packets.
You're on a roll. 5 (264 total recv) icmp packets in a row and 92ms mean for the last 8 packets.
You're on a roll. 6 (265 total recv) icmp packets in a row and 92ms mean for the last 8 packets.
You're on a roll. 7 (266 total recv) icmp packets in a row and 92ms mean for the last 8 packets.
We're hitting a rough patch here. 2 icmp packets skipped but 92ms mean for the last 8 packets.
You're on a roll. 1 (270 total recv) icmp packets in a row and 92ms mean for the last 8 packets.
You're on a roll. 2 (271 total recv) icmp packets in a row and 91ms mean for the last 8 packets.
You're on a roll. 3 (272 total recv) icmp packets in a row and 91ms mean for the last 8 packets.
You're on a roll. 4 (273 total recv) icmp packets in a row and 91ms mean for the last 8 packets.
You're on a roll. 5 (274 total recv) icmp packets in a row and 90ms mean for the last 8 packets.
```

# License

MIT
