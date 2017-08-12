from LogParser import LogParser
import unittest


class TestLogParser(unittest.TestCase):
    def test_parse(self):
        LogParser("./test_log.txt", ".", "@ERROR_GROUP")
        with open("./test_log.text_err_timestamps.txt") as f:
            lines = f.readlines()
            self.assertEquals(len(lines), 1)
            self.assertEquals(lines[0], "1502443757149")


if __name__ == "__main__":
    unittest.main()
