import threading, time


def thead(num):
    # time.sleep(1)
    print("线程%s开始执行" % num)
    time.sleep(3)
    print("线程%s执行完毕" % num)


def main():
    print("主方法开始执行")

    # 创建2个线程
    poll = []  # 线程池
    for i in range(1, 3):
        thead_one = threading.Thread(target=thead, args=(i,))
        poll.append(thead_one)  # 线程池添加线程
    for n in poll:
        n.start()  # 准备就绪,等待cpu执行

    print("主方法执行完毕")
    return


if __name__ == '__main__':
    print(time.ctime())
    num = main()
    print("返回结果为%s" % num)
    print(time.ctime())
