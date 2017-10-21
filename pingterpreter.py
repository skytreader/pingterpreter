#! /usr/bin/env python3

from argparse import ArgumentParser
from sys import stdin
import re

ICMP_RE = re.compile(r".+icmp_seq=(\d+).+")
# Assumes time is the last field in ping output
TIME_RE = re.compile(r".+time=(\d+(\.\d+)*) ms")

class Pingterpreter(object):

    GOOD_TEMPLATE = "You're on a roll. %(connection_status)s."
    BAD_TEMPLATE = "We're hitting a rough patch here. %(connection_status)s."
    ICMP_REPORTS = {
        0: "%(icmp_count)d (%(total_icmp)d total recv) icmp packets in a row",
        2: "Uh oh %(icmp_count)d icmp packets skipped",
        5: "%(icmp_count)d icmp packets skipped"
    }
    TIME_REPORTS = "%(mean)dms mean for the last %(window)d packets"
    SND_RCV_REPORTS = "%(time)dms between this packet and last"

    def __init__(self, catch_icmp=True, catch_time=False, verbose=False, time_window_limit=8, mean_thresh=100):
        self.catch_icmp = catch_icmp
        self.catch_time = catch_time
        self.verbose = verbose
        self.time_window_limit = time_window_limit
        self.mean_threshold = mean_thresh

        # State fields
        self.current_icmp = 0
        self.consec_icmp = 0
        self.last_call = None
        self.time_window = []

    def interpret(self, pingline):
        status_components = []
        if self.verbose:
            print(pingline.strip())

        icmp_good = False
        if self.catch_icmp:
            icmp = ICMP_RE.match(pingline)
            if icmp:
                icmp = int(icmp.group(1))
                jump = icmp - (self.current_icmp + 1)
                if jump == 0:
                    self.consec_icmp += 1
                    icmp_good = True
                else:
                    self.consec_icmp = 0
                template_ctx = {
                    "icmp_count": self.consec_icmp if jump == 0 else jump,
                    "total_icmp": icmp
                }

                if jump >= 2:
                    status_components.append(Pingterpreter.ICMP_REPORTS[5] % template_ctx)
                else:
                    template = Pingterpreter.ICMP_REPORTS.get(jump)
                    if template:
                        status_components.append(template % template_ctx)
                self.current_icmp = icmp

        time_verdict = ""
        time_good = False
        if self.catch_time:
            time = TIME_RE.match(pingline)
            if time:
                time = float(time.group(1))
                if len(self.time_window) == self.time_window_limit:
                    self.time_window.pop(0)
                self.time_window.append(time)
                mean = sum(self.time_window) / len(self.time_window)
                time_verdict = Pingterpreter.TIME_REPORTS % {"mean": mean, "window": len(self.time_window)}
                time_good = mean < self.mean_threshold

        if status_components and self.catch_time: # contain icmp verdict
            if icmp_good == time_good:
                status_components.append("and")
            else:
                status_components.append("but")

        status_components.append(time_verdict)
        status = " ".join(status_components)

        if icmp_good and time_good:
            print(Pingterpreter.GOOD_TEMPLATE % {"connection_status": status})
        else:
            print(Pingterpreter.BAD_TEMPLATE % {"connection_status": status})

if __name__ == "__main__":
    parser = ArgumentParser(description="Humanize ping output for network heuristics.")
    parser.add_argument(
        "--icmp", "-i", required=False, type=bool, default=True,
        help="If true we will watch icmp as a metric"
    )
    parser.add_argument(
        "--time", "-t", required=False, type=bool, default=True,
        help="If true we will watch time as a metric"
    )
    parser.add_argument(
        "--verbose", "-v", required=False, action="store_true",
        help="If set then display the actual PING lines as well."
    )

    args = vars(parser.parse_args())

    pingterpreter = Pingterpreter(catch_icmp=args["icmp"], catch_time=args["time"], verbose=args["verbose"])

    for pingline in stdin:
        pingterpreter.interpret(pingline)
