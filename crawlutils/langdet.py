# -*- coding: utf-8 -*-
import chardet
import re
import langid

class Langdet(object):
    HEAD = re.compile("<head[^>]*>(.*?)</head>", re.IGNORECASE|re.MULTILINE|re.DOTALL)
    TITLE = re.compile("<title[^>]*>(.*?)</title>", re.IGNORECASE|re.MULTILINE|re.DOTALL)
    LANG_TAG = re.compile("<html[^>]*lang=\"?([a-zA-Z-]*)\"?[^>]*>", re.IGNORECASE|re.MULTILINE|re.DOTALL)
    VALID_J_TAG = re.compile("(ja)|(jp)", re.IGNORECASE)
    VALID_E_TAG = re.compile("en", re.IGNORECASE)
    CHARTAG = re.compile("<meta[^>]*charset=[\"' ]*([^> \"']*)[\"' ]*[/]?>", re.IGNORECASE|re.MULTILINE|re.DOTALL)
    CONTENT_TAG = re.compile("<meta[^>]*description[^>]*>", re.IGNORECASE|re.MULTILINE|re.DOTALL)
    CONTENT_CONTENT_TAG = re.compile("content=\"(.*?)\"", re.IGNORECASE|re.MULTILINE|re.DOTALL)
    HEAD_CHARTAG = re.compile("charset=[ \"']*([^ \"']*)[ \"']*", re.IGNORECASE|re.MULTILINE|re.DOTALL)
    JA_ENCODING = re.compile("(euc[-_]jp)|(shift[-_]jis)", re.IGNORECASE|re.MULTILINE|re.DOTALL)
    LANG_J = "JA"
    LANG_E = "EN"

    def __init__(self):
        pass

    def detect(self, header, body):
        header_enc = self._header_detect(header)
        result = self._body_detect(body, header_enc)
        return result

    def _body_detect(self, body, enc):
        head = self._group(self.HEAD.search(body), 0)
        if head:
            title = self._group(self.TITLE.search(head), 1)
            if enc is None:
                enc = self._enc_detect(head, title)
            lang = self._lang_detect(head, body, title, enc)
            if lang is not None:
                try:
                    return (lang, body.decode(enc, errors="ignore"))
                except Exception as e:
                    pass
        return None

    def _header_detect(self, header):
        if "Content-Type" in header:
            enc = self._group(self.HEAD_CHARTAG.search(header["Content-Type"][0]), 1)
            return enc
        return None

    def _extract_charset(self, body):
        enc = self._group(self.CHARTAG.search(body), 1)
        return enc

    def _langdet_by_tag(self, body):
        tag = self._group(self.LANG_TAG.search(body), 1)
        if tag:
            if self.VALID_J_TAG.search(tag):
                return self.LANG_J
            if self.VALID_E_TAG.search(tag):
                return self.LANG_E
        return None

    def _enc_detect(self, head, title):
        enc = self._extract_charset(head)
        if enc is None:
            enc = chardet.detect(title)["encoding"]
        return enc

    def _lang_detect(self, head, body, title, enc):
        lang = self._langdet_by_tag(body)
        if lang is None:
            if self.JA_ENCODING.match(enc):
                lang = self.LANG_J
        if lang is None:
            try:
                title = title.decode(enc, errors="ignore")
                meta = self._group(self.CONTENT_TAG.search(head), 0)
                if meta:
                    desc = self._group(self.CONTENT_CONTENT_TAG.search(meta), 1)
                    if desc:
                        title += ' ' + desc.decode(enc, errors="ignore")
                res = langid.classify(title)
                if res[0] == 'en':
                    lang = self.LANG_E
                if res[0] == 'ja':
                    lang = self.LANG_J
            except:
                pass
        return lang

    def _group(self, match, idx):
        if match:
            return match.group(idx)
        else:
            return None


if __name__ == '__main__':
    pass
