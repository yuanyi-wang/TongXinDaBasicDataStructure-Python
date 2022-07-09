# -*- coding: utf-8 -*-

import os
import unittest

from TongXinDaBasicDataStructure import DayData, MinuteData, day_file_handler

class DayDataTest(unittest.TestCase):
    def test_parser(self):
        with open(os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "TestData", "sz000001.day"), 'rb') as f:
            day_raw_data = DayData(f.read(32))
            day_raw_data.print_log()

        self.assertEqual(day_raw_data.price_date,       20150902)
        self.assertEqual(day_raw_data.price_opening,    11.18)
        self.assertEqual(day_raw_data.price_highest,    12.0)
        self.assertEqual(day_raw_data.price_lowest,     11.06)
        self.assertEqual(day_raw_data.price_closing,    11.84)
        self.assertEqual(day_raw_data.turnover,         32738030.08)
        self.assertEqual(day_raw_data.volume,           281574592)
        pass

    def test_parser_full_file(self):
        data_file = day_file_handler(
            os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "TestData", "sz000001.day"))
        print(data_file.get_data_count())
        self.assertEqual(data_file.stock_code, "sz000001")
        self.assertEqual(data_file.file_type, "day")
        pass

class LC5_MinuteDataTest(unittest.TestCase):
    def test_parser(self):

        with open(os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "TestData", "sz000001.lc5"), 'rb') as f:
            lc5_raw_data = MinuteData(f.read(32))
            lc5_raw_data.print_log()

        self.assertEqual(lc5_raw_data.price_date,       20220309)
        self.assertEqual(lc5_raw_data.price_time,       935)
        self.assertEqual(lc5_raw_data.price_opening,    14.399999618530273)
        self.assertEqual(lc5_raw_data.price_highest,    14.449999809265137)
        self.assertEqual(lc5_raw_data.price_lowest,     14.069999694824219)
        self.assertEqual(lc5_raw_data.price_closing,    14.079999923706055)
        self.assertEqual(lc5_raw_data.turnover,         1292541759)
        self.assertEqual(lc5_raw_data.volume,           10187200)
        pass

if __name__ == '__main__':
    unittest.main()