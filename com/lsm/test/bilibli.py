# -*- coding: utf-8 -*-
import requests
import lxml.html


if __name__ == '__main__':
     base_hits_wan = 14
     key_words = "马克思"
     contents = requests.get("https://search.bilibili.com/all?keyword=%s&from_source=web_search&page=1" % key_words).text
     dom = lxml.html.fromstring(contents)
     all_links = dom.xpath('.//ul[@class]')
     result_pages = set()
     for link in all_links:
          if link.attrib.get("class") == "video-list clearfix":
               for li in link.xpath("li"):
                    watch_num = li.xpath(".//span[@title='观看']/text()")
                    watch_num = str(watch_num[0]).strip("\n").strip(" ")
                    if "万" in watch_num:
                         if float(watch_num.replace("万", "")) > base_hits_wan:
                              video = li.xpath("..//a[@title]")[0]
                              url = video.attrib.get("href").lstrip("//")
                              url = "https://%s" % url.rstrip("?from=search")
                              if url not in result_pages:
                                   name = video.attrib.get("title")
                                   print("=======================即将下载==========================")
                                   print("【%s】\n 地址是：【%s】\n 播放量：%s" %(name, url, watch_num))
                                   result_pages.add(url)

     print(result_pages)
