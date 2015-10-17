#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import requests,collections,xml.etree.ElementTree as ET, sys


WARN_NOT_FIND = " 找不到该单词的释义"
ERROR_QUERY = " 有道翻译查询出错!"

def get_word_info(word):
    if not word:
        return ''
    r = requests.get("http://dict.youdao.com" + "/fsearch?q=" + word)
    if r.status_code == 200:

        doc = ET.fromstring(r.content)
        info = collections.defaultdict(list)


        if not len(doc.findall(".//content")):
            #TODO handle not found
            return WARN_NOT_FIND.decode('utf-8')

        for el in doc.findall(".//"):
            if el.tag in ('return-phrase','phonetic-symbol'):
                if el.text:
                    info[el.tag].append(el.text.encode("utf-8"))
            elif el.tag in ('content','value'):
                info[el.tag].append(el.text.encode("utf-8"))

        for k,v in info.items():
            info[k] = ' | '.join(v) if k == "content" else ' '.join(v)

        tpl = ' %(return-phrase)s'
        if info["phonetic-symbol"]:
            tpl = tpl + ' [%(phonetic-symbol)s]'
        tpl = tpl +' %(content)s'

        return tpl % info

    else:
        return  ERROR_QUERY.decode('utf-8')

def translate_visual_selection(word):

    word = word.decode('utf-8')
    info = get_word_info( word )
    print(info)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        translate_visual_selection(sys.argv[1])
    else:
        print("请输入要翻译的单词，多个以引号扩起来")

