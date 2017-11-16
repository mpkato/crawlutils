# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup

class Tabdet(object):
    TABLE = re.compile("<table.*?</table>", re.IGNORECASE|re.MULTILINE|re.DOTALL)
    PREFIX_TABLE = re.compile("<table.*?", re.IGNORECASE|re.MULTILINE|re.DOTALL)
    CALENDER = re.compile("<table[^>]*calendar[^>]*>", re.IGNORECASE|re.MULTILINE|re.DOTALL)
    CALENDER_HEIGHT_MIN = 4
    CALENDER_HEIGHT_MAX = 8
    CALENDER_WIDTH_MIN = 6
    CALENDER_WIDTH_MAX = 10
    INTEXP = re.compile("[1-9]?[0-9]", re.IGNORECASE|re.MULTILINE|re.DOTALL)
    CALENDER_RANGE_MAX = 29
    CALENDER_NUM_MAX = 32

    MIN_TR_NUM = 2
    MIN_THTD_NUM = 2
    MIN_SIZE = 10
    MAX_CELL_SIZE = 100
    MAX_EMPTY_CELL_RATIO = 0.40

    def findone(self, html):
        for table in self.detect(html):
            return table
        return None

    def detect(self, html):
        tables = self.TABLE.findall(html)
        for table in tables:
            if not self._is_nested(table)\
                and self._is_valid(table):
                print(table)
                yield table

    def _is_nested(self, table):
        matches = self.PREFIX_TABLE.findall(table)
        return len(matches) > 1

    def _is_valid(self, table):
        soup = BeautifulSoup(table, "html.parser")
        tr_matches = soup.find_all("tr")
        # tall?
        if len(tr_matches) < self.MIN_TR_NUM:
            return False
        thtd_matches = soup.find_all("th") + soup.find_all("td")
        # large?
        if len(thtd_matches) < self.MIN_SIZE:
            return False
        # wide?
        if len(thtd_matches) / len(tr_matches) < self.MIN_THTD_NUM:
            return False

        # dense and compact?
        if not self._is_dense_and_compact(thtd_matches):
            return False

        # non-calender?
        if self._is_calender(table, tr_matches, thtd_matches):
            return False

        return True

    def _is_dense_and_compact(self, thtd_matches):
        empty_cell = 0
        for thtd in thtd_matches:
            cell_content = thtd.get_text().strip()
            # compact?
            if len(cell_content) > self.MAX_CELL_SIZE:
                return False
            if len(cell_content) == 0:
                empty_cell += 1
        # dense?
        if float(empty_cell) / len(thtd_matches) > self.MAX_EMPTY_CELL_RATIO:
            return False

        return True

    def _is_calender(self, table, tr_matches, thtd_matches):
        if self.CALENDER.search(table):
            return True
        width = len(thtd_matches) / len(tr_matches)
        if len(tr_matches) >= self.CALENDER_HEIGHT_MIN\
            and len(tr_matches) <= self.CALENDER_HEIGHT_MAX\
            and width >= self.CALENDER_WIDTH_MIN\
            and width <= self.CALENDER_WIDTH_MAX:
            nums = set()
            for thtd in thtd_matches:
                cell_content = thtd.get_text()
                m = self.INTEXP.search(cell_content)
                if m:
                    nums.add(int(m.group(0)))
            if len(nums) < self.CALENDER_NUM_MAX\
                and all([n in nums
                    for n in range(1, self.CALENDER_RANGE_MAX)]):
                return True
        return False
