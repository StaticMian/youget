import threading, time, os

import lxml.html
import requests

from com.lsm.test.basic_util import exec_command

base_destination_dir = "/Users/lsm/Downloads/test"
base_command = "/Users/lsm/Downloads/software/you-get-develop/you-get -o "

def download_file_func(command, url):
    print("【%s】开始下载【%s】" % (threading.current_thread().getName(), url))
    # while True:
    #     time.sleep(1)
    #     print("%s ing.." % threading.current_thread().getName())
    # os.system("%s %s " % (command, url))
    # exec_command("%s %s " % (command, url))
    print("【%s】下载完成【%s】" % (threading.current_thread().getName(), url))


def download_multi_thread(urls):
    print("即将开始下载视频个数：%s" % len(urls))
    command = base_command + base_destination_dir
    batch = 20
    urls = list(urls)
    threads = []
    while len(urls) > 0:
        if len(urls) <= batch:
            for url in urls:
                threads.append(threading.Thread(target=download_file_func, args=(command, url,)))
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
            urls = []
        else:
            for i in range(0, batch):
                threads.append(threading.Thread(target=download_file_func, args=(command, urls[i],)))
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
            for i in range(0, batch):
                urls.remove(0)
        threads = []

# 下载B站上系列视频, 例如：
#     base_url = "https://www.bilibili.com/video/BV17K411N7hU\?p="
#     task_ids = range(37, 79)
def down_load_series(base_url, p_ids):
    threads = []
    for p_id in p_ids:
        command = base_command + base_destination_dir
        threads.append(threading.Thread(target=download_file_func, args=(command, base_url + str(p_id),)))
    for thread in threads:
        thread.start()


# 下载关键字搜索内容
def down_load_search_key_words(key_words, min_hit_count_in_wan):
    over = False
    for i in range(1, 100):
        if over:
            break
        contents = requests.get("https://search.bilibili.com/all?keyword=%s&from_source=web_search&order=click&duration=0&tids_1=0&page=%s" % (key_words, i)).text
        dom = lxml.html.fromstring(contents)
        all_links = dom.xpath('.//ul[@class]')
        result_pages = set()
        for link in all_links:
            if link.attrib.get("class") == "video-list clearfix":
                for li in link.xpath("li"):
                    watch_num = li.xpath(".//span[@title='观看']/text()")
                    watch_num = str(watch_num[0]).strip("\n").strip(" ")
                    if "万" in watch_num:
                        if float(watch_num.replace("万", "")) >= min_hit_count_in_wan:
                            video = li.xpath(".//a[@title]")[0]
                            url = video.attrib.get("href").lstrip("//")
                            url = "https://%s" % url.rstrip("?from=search")
                            if url not in result_pages:
                                name = video.attrib.get("title")
                                # print("=======================即将下载==========================")
                                # print("【%s】\n 地址是：【%s】\n 播放量：%s" % (name, url, watch_num))
                                result_pages.add(url)
                        else:
                            over = True
                    else:
                        over = True

        download_multi_thread(result_pages)


if __name__ == '__main__':
    down_load_search_key_words("毛泽东", 1)
