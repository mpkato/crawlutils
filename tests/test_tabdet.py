# -*- coding: utf-8 -*-
import crawlutils as cu

class TestTabdet(object):

    def test_detect(self):
        GROUND_TRUTH = [0, 0, 0, 0, 3, 0, 3, 0, 0, 0,
            4, 0, 0, 0, 0, 1, 0, 3, 5, ]
        ld = cu.Langdet()
        td = cu.Tabdet()
        for i in range(1, 20):
            res = ld.detect({}, open("./tests/fixtures/test%s.html" % i).read())
            body = res[1]
            tables = list(td.detect(body))
            assert GROUND_TRUTH[i-1] == len(tables)

    def test_findone(self):
        ld = cu.Langdet()
        td = cu.Tabdet()
        res = ld.detect({}, open("./tests/fixtures/test11.html").read())
        body = res[1]
        td.findone(body)
