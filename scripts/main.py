#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
import signal
import subprocess
from subprocess import PIPE
import os
import psutil

from gstreamer_launcher.srv import *


def launcher(req):
    if req.message_type == "LAUNCH":
        proc = subprocess.Popen(req.command, shell=True, restore_signals=True, stdout=PIPE, stderr=PIPE)
        try:
            res = proc.communicate(timeout=0.1)
        except subprocess.TimeoutExpired:
            return GStreamerLauncherResponse(True, proc.pid)

        return GStreamerLauncherResponse(False, -1)
    elif req.message_type == "EXIT":
        try:
            os.killpg(os.getpgid(req.pid), signal.SIGTERM)
        except ProcessLookupError:
            return GStreamerLauncherResponse(False, -1)

        return GStreamerLauncherResponse(True, 0)

    return GStreamerLauncherResponse(False, -1)


def gst_launch_server():
    s = rospy.Service('gst_launch', GStreamerLauncher, launcher)
    rospy.spin()


def sigterm_handler(signal, frame):
    pass


def main():
    gst_launch_server()


if __name__ == "__main__":
    rospy.init_node('gstreamer_launcher', log_level=rospy.INFO)
    signal.signal(signal.SIGTERM, sigterm_handler)
    main()
