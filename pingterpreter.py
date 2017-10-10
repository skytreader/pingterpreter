#! /usr/bin/env python3

import re

ICMP_RE = re.compile("icmp_seq=(\d+)")

class Pingterpreter(object):

    GOOD_TEMPLATE = "You're on a roll. %(connection_status)"
    BAD_TEMPLATE = "We're hitting a rough patch here. %(connection_status)"
    ICMP_REPORTS = {
        "good": "%(icmp_count) icmp packets in a row",
        "bad": "%(icmp_count) icmp packets skipped"
    }
    TIME_REPORTS = {
        "good": "%(time)ms average for the last 10 packets"
        "bad": "%(ave_time)ms between last packet and latest"
    }

    def __init__(self, catch_icmp=True, catch_time=False):
        self.catch_icmp = catch_icmp
        self.catch_time = catch_time

        # State fields
        self.current_icmp = 0
        self.last_call = None
        self.last_time = None

    def interpret(self, pingline):
        pass
