#! /usr/bin/env python3

from sys import stdin
import re

ICMP_RE = re.compile(".+icmp_seq=(\d+).+")

class Pingterpreter(object):

    GOOD_TEMPLATE = "You're on a roll. %(connection_status)s"
    BAD_TEMPLATE = "We're hitting a rough patch here. %(connection_status)s"
    ICMP_REPORTS = {
        0: "%(icmp_count)d icmp packets in a row",
        2: "Uh oh %(icmp_count)d icmp packets skipped",
        5: "%(icmp_count)d icmp packets skipped"
    }
    TIME_REPORTS = {
        "good": "%(time)dms average for the last 10 packets",
        "bad": "%(ave_time)dms between last packet and latest"
    }

    def __init__(self, catch_icmp=True, catch_time=False, verbose=False):
        self.catch_icmp = catch_icmp
        self.catch_time = catch_time
        self.verbose = verbose

        # State fields
        self.current_icmp = 0
        self.consec_icmp = 0
        self.last_call = None
        self.last_time = None

    def interpret(self, pingline):
        status_components = []
        if self.verbose:
            print(pingline)

        if self.catch_icmp:
            icmp = ICMP_RE.match(pingline)
            if icmp:
                icmp = int(icmp.group(1))
                jump = icmp - (self.current_icmp + 1)
                if jump == 0:
                    self.consec_icmp += 1
                else:
                    self.consec_icmp = 0
                template_ctx = {
                    "icmp_count": self.consec_icmp if jump == 0 else jump
                }
                if jump > 5:
                    status_components.append(Pingterpreter.ICMP_REPORTS[5] % template_ctx)
                else:
                    template = Pingterpreter.ICMP_REPORTS.get(jump)
                    if template:
                        status_components.append(template % template_ctx)
                self.current_icmp = icmp

        print("".join(status_components))

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
        "--verbose", "-v", required=False, type=bool, default=False,
        help="If set then display the actual PING lines as well."
    )

    args = vars(parser.parse_args())

    pingterpreter = Pingterpreter(catch_icmp=args["icmp"], catch_time=args["catch_time"], verbose=args["verbose"])

    for pingline in stdin:
        pingterpreter.interpret(pingline)
