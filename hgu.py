import paramiko
import subprocess
import time


class SSHOLT(object):

    def __init__(self):
        self.client = paramiko.SSHClient()

    def auth(self, host, port, usr, pwd):
        # key = paramiko.RSAKey.from_private_key_file(pkeyFile, password=pkeyPwd)
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 通过公共方式进行认证 (不需要在known_hosts 文件中存在)
        # self.client.connect(host, port, username=usr, password=pwd, pkey=key)
        self.client.connect(host, port, username=usr, password=pwd)

    def exec_cmd(self, cmd):
        return self.client.exec_command(cmd)

    def close(self):
        self.client.close()

class Programing(object):

    def __init__(self, ):
        pass

    def getLinkState(self, ip):
        ping_True = True
        sTime = time.time()
        # 运行ping程序
        while ping_True:
            runTime = time.time()
            if time.time() - sTime > 180:
                break
            p = subprocess.Popen("ping %s -w 100 -n 1" % (ip),
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 shell=True)

            # 得到ping的结果
            # print(p.stdout.read())
            out = str(p.stdout.read(), encoding="gb2312", errors="ignore")
            print('ont:', out)

            # #找出丢包率，这里通过‘%’匹配
            # regex = re.compile(r'\w*%\w*')
            # packetLossRateList = regex.findall()
            if 'Request timed out' in out:
                print('Request timed out')
            elif 'General failure' in out:
                print('General failure')
            elif "Destination host unreachable" in out:
                print("Destination host unreachable")
            elif "Destination net unreachable" in out:
                print("Destination net unreachable")
            elif "丢失 = 1 " in out:
                print("丢失 = 1 ")
            elif "字节=32" in out:
                print("字节=32")
                ping_True = False
            elif 'bytes=32' in out:
                print('bytes=32')
                ping_True = False
        print(ping_True)
        return ping_True

    def signalPro(self, ip, mac, sn, queue):
        logQueue = queue
        logQueue.put("正在连接HGU...")
        if not self.getLinkState(ip):
            logQueue.put("连接成功，开始烧写。")
            time.sleep(10)
            logQueue.put("烧写完成。")
            logQueue.put("finish")
        else:
            logQueue.append("连接超时...")
            logQueue.put("finish")


    def continuousPro(self):
        pass

    def manualPro(self):
        pass