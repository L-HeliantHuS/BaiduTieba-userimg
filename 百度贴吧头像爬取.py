#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author    : HeliantHuS
# Time      : 2018/9/13/19:08
import os
import re
import requests
from lxml import etree
from multiprocessing import Pool
class TieBa():
    def __init__(self):
        if 'images' not in os.listdir():
            os.mkdir('images')
        kw = input("输入贴吧名:")
        url = 'http://tieba.baidu.com/f?kw={}&ie=utf-8&pn=0'.format(kw)
        etg = self.get_etree(url)
        a_href = etg.xpath('//a[@class="last pagination-item "]/@href')
        href_page = re.findall('//(.*?)&ie=utf-8&pn=(.*)',a_href[0])[0][1]
        print('当前贴吧共有%s页'%(int(href_page)/50))
        start = input('请输入起始页数(默认为1):')
        end = input("请输入结束页数(默认为最多):")
        if start == '':
            if end == '':
                url = ['http://tieba.baidu.com/f?kw={}&ie=utf-8&pn={}'.format(kw, page) for page in range(0, int(href_page) + 1, 50)]
            elif end != '':
                url = ['http://tieba.baidu.com/f?kw={}&ie=utf-8&pn={}'.format(kw, page) for page in range(0, int(end)*50-50 + 1, 50)]
        elif end == '':
            if start == '':
                url = ['http://tieba.baidu.com/f?kw={}&ie=utf-8&pn={}'.format(kw, page) for page in range(0, int(href_page) + 1, 50)]
            elif start != '':
                url = ['http://tieba.baidu.com/f?kw={}&ie=utf-8&pn={}'.format(kw, page) for page in range(int(start)*50-50, int(href_page) + 1, 50)]
        else:
            url = ['http://tieba.baidu.com/f?kw={}&ie=utf-8&pn={}'.format(kw, page) for page in range(int(start)*50-50,int(end)*50+1, 50)]

        print('起始%s结束%s'%(start,end))
        pool = Pool(processes=4)
        pool.map(self.response, url)

    def response(self, url):
        try:
            res_ponse = self.get_etree(url)
            url_list = res_ponse.xpath('//div[@class="threadlist_title pull_left j_th_tit "]/a[@rel="noreferrer"]/@href')

            for xx_url in url_list:
                url_wz = "http://tieba.baidu.com" + xx_url
                img_etr = self.get_etree(url_wz)
                neibu_page = img_etr.xpath('//li[@class="l_reply_num"]/span[2]/text()')[0]

                for page in range(1, int(neibu_page)+1):
                    surl = url_wz  + '?pn={}'.format(page)
                    img_etr = self.get_etree(surl)
                    print(surl)
                    img_url = (img_etr.xpath('//div[@class="icon_relative j_user_card"]/a[@target="_blank"]/img/@data-tb-lazyload'))
                    img_url.extend(img_etr.xpath('//div[@class="icon_relative j_user_card"]/a[@target="_blank"]/img/@src')[0:3])
                    name = img_etr.xpath('//div[@class="icon_relative j_user_card"]/a[@target="_blank"]/img/@username')

                    for s,user in zip(img_url,name):
                        with open('images/{}.jpg'.format("".join(user)), 'wb') as fp:
                            print(user)
                            fp.write(requests.get(s).content)

        except:
            pass


    def get_etree(self, response):
        reg = etree.HTML(requests.get(response).text)
        return reg

if __name__ == '__main__':
    tieba = TieBa()
