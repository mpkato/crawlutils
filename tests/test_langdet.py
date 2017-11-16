# -*- coding: utf-8 -*-
import crawlutils as cu

class TestLangdet(object):

    def test_detect(self):
        GROUND_TRUTH = ['EN', 'EN', 'JA', 'EN', 'JA', 'JA', 'JA', 'JA', 'EN',
            'EN', 'JA', 'JA', 'JA', 'JA', 'JA', 'JA', 'JA', 'JA', 'JA', ]
        ld = cu.Langdet()
        for i in range(1, 20):
            res = ld.detect({}, open("./tests/fixtures/test%s.html" % i).read())
            assert res is not None
            assert res[0] == GROUND_TRUTH[i-1]

    def test_encoding(self):
        GROUND_TRUTH = ['クラウド', 'AWS', 'インストール', 'EC2', 'クエリ',
            'コード', '文字コード表', 'Yahoo', '加藤', 'Tanaka', '政府',
            '構造', '統計', '東京都', '東京都', '東京都', 'ホーム', 'ブドウ',
            'ぶどう', ]
        ld = cu.Langdet()
        for i in range(1, 20):
            res = ld.detect({}, open("./tests/fixtures/test%s.html" % i).read())
            title = ld.TITLE.search(res[1]).group(1)
            assert GROUND_TRUTH[i-1].decode('utf-8') in title
