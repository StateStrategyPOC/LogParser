#!/usr/bin/env python
from LogParser import LogParser
from unittest import TestCase


class TestLogParser(TestCase):
    def test_parse(self):
        LogParser("./test_log.txt", ".", "@ERROR_GROUP")
        with open("./test_log.txt_err_timestamps.txt") as f:
            lines = f.readlines()
            self.assertEquals(len(lines), 1)
            self.assertEquals(lines[0], "1502443757149")


