#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Copyright (c) 2016, Antonio Coratelli.
Released under BSD 3-Clause License. See 'LICENSE' file.
'''

import os
import sys
import argparse
import re
from chardet.universaldetector import UniversalDetector


class Timestamp(object):

    def __init__(self, initial_value):
        try:
            self.from_timestamp(initial_value)
        except:
            self.from_seconds(initial_value)

    def from_seconds(self, seconds):
        self.time = float(seconds)

    def from_timestamp(self, timestamp):
        t = list(map(int, re.split(r"[:,.]", timestamp)))
        seconds = t[0] * 3600.0 + t[1] * 60.0 + t[2] + t[3] / 1000.0
        self.from_seconds(seconds)

    def to_seconds(self):
        return self.time

    def to_timestamp(self):
        def scale(seconds, factor):
            unit = int(seconds / float(factor))
            remaining_seconds = seconds - unit * factor
            return remaining_seconds, unit
        seconds = self.time
        seconds, hours   = scale(seconds, 3600)
        seconds, minutes = scale(seconds,   60)
        tup = (hours, minutes, seconds)
        return ("%02d:%02d:%06.3f" % tup).replace('.', ',')


class TransformableTimestamp(Timestamp):

    def apply_transform(self, transform):
        x = self.time
        self.time = transform.M() * x + transform.Q()


class Point(object):

    def __init__(self, x=None, y=None):
        self.set(x, y)

    def set(self, x, y):
        self.x, self.y = x, y


class LinearTransform(object):

    def __init__(self, point_1, point_2):
        self.__M, self.__Q = None, None
        self.set_point_1(point_1)
        self.set_point_2(point_2)

    def set_point_1(self, point):
        self.p1 = point

    def set_point_2(self, point):
        self.p2 = point

    def M(self):
        if self.__M is None:
            self.__M = (self.p1.y - self.p2.y) / (self.p1.x - self.p2.x)
        return self.__M

    def Q(self):
        if self.__Q is None:
            self.__Q = (self.p1.y - self.M() * self.p1.x)
        return self.__Q


class SrtTransformer(object):

    def __init__(self, srt_in_path):
        self.load_file(srt_in_path)

    def load_file(self, filename):
        self.get_file_encoding(filename)
        with open(filename, 'r', encoding=self.encoding, errors='ignore') as f:
            self.srt_in = f.read()

    def get_file_encoding(self, filename):
        detector = UniversalDetector()
        for line in open(filename, 'rb'):
            detector.feed(line)
            if detector.done: break
        detector.close()
        self.encoding = detector.result['encoding']

    def transform(self, trasformation):
        self.srt_out = ''
        for line in self.srt_in.splitlines():
            m = re.match(r'(\d\d:\d\d:\d\d,\d\d\d).*-->.*(\d\d:\d\d:\d\d,\d\d\d)', line, re.M|re.I)
            if m:
                timestamp_1 = TransformableTimestamp(m.group(1))
                timestamp_2 = TransformableTimestamp(m.group(2))
                timestamp_1.apply_transform(trasformation)
                timestamp_2.apply_transform(trasformation)
                t = (timestamp_1.to_timestamp(), timestamp_2.to_timestamp())
                line = "%s --> %s" % t
            else:
                pass
            self.srt_out += "%s\r\n" % line

    def save_file(self, filename):
        with open(filename, 'w', encoding=self.encoding) as f:
            f.write(self.srt_out)


if __name__ == '__main__':

    usage = "srt-transform.py [-h] [PARAMS] INPUT OUTPUT"
    parser = argparse.ArgumentParser(usage=usage, epilog=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input", action="store", type=str, metavar='INPUT', help="input srt file")
    parser.add_argument("output", action="store", type=str, metavar='OUTPUT', help="output srt file")

    required = parser.add_argument_group('required arguments')
    required.add_argument("--SW", "--start-wrong", action="store", dest="start_wrong", required=True)
    required.add_argument("--SR", "--start-right", action="store", dest="start_right", required=True)
    required.add_argument("--EW", "--end-wrong", action="store", dest="end_wrong", required=True)
    required.add_argument("--ER", "--end-right", action="store", dest="end_right", required=True)

    args = parser.parse_args()

    s = SrtTransformer(args.input)

    x_1 = Timestamp(args.start_wrong).to_seconds()
    y_1 = Timestamp(args.start_right).to_seconds()
    point_1 = Point(x_1, y_1)

    x_2 = Timestamp(args.end_wrong).to_seconds()
    y_2 = Timestamp(args.end_right).to_seconds()
    point_2 = Point(x_2, y_2)

    transformation = LinearTransform(point_1, point_2)

    s.transform(transformation)
    s.save_file(args.output)
