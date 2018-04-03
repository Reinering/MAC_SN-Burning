# -*- coding: utf-8 -*-
#python35

import paramiko
import subprocess
import time
# from pykeyboard import PyKeyboard
from scp import SCPClient

class SSHOLT(object):

    def __init__(self):
        self.client = paramiko.SSHClient()

    def authSSH(self, host, port, usr, pwd):
        try:
            # key = paramiko.RSAKey.from_private_key_file(pkeyFile, password=pkeyPwd)
            self.client.load_system_host_keys()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 通过公共方式进行认证 (不需要在known_hosts 文件中存在)
            # self.client.connect(host, port, username=usr, password=pwd, pkey=key)
            self.client.connect(host, port=port, username=usr, password=pwd)
        except paramiko.ssh_exception.NoValidConnectionsError as e:
            print("ssh登录错误：", e)
            raise paramiko.ssh_exception.NoValidConnectionsError
        except TimeoutError as e:
            print("登录超时：", e)
            raise TimeoutError
        except ConnectionError as e:
            print("建立失败：", e)
            raise ConnectionError

    def exec_cmd(self, cmd):
        print(cmd)
        return self.client.exec_command(cmd)
    def upload(self, localpath, remotepath):
        self.sftpclient = SCPClient(self.client.get_transport(), socket_timeout=15.0)
        self.sftpclient.put(localpath, remotepath)

    def close(self):
        self.sftpclient.close()
        self.client.close()

    # def read(self):
    #     import threading
    #     sys.stdout.write("Line-buffered terminal emulation. Press F6 or ^Z to send EOF.rnrn")
    #
    #     def writeall(sock):
    #         while True:
    #             data = sock.recv(256)
    #             if not data:
    #                 sys.stdout.write('rn*** EOF ***rnrn')
    #                 sys.stdout.flush()
    #                 break
    #             sys.stdout.write(str(data, encoding="utf-8", errors="ignore"))
    #             sys.stdout.flush()
    #
    #     writer = threading.Thread(target=writeall, args=(self.channel,))
    #     writer.start()

class Programing(object):

    def __init__(self, ):
        self.ssholt = SSHOLT()
        self.usr = "root"
        self.pwd = "nE7jA%5m"

    def getLinkState(self, ip):
        ping_True = True
        sTime = time.time()
        # 运行ping程序
        while ping_True:
            # runTime = time.time()
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
            try:
                self.ssholt.authSSH(ip, 22, self.usr, self.pwd)
                logQueue.put("SSH连接成功，开始烧写。")
            except Exception as e:
                print(e)
                logQueue.put("SSH登录失败")
                return False

            logQueue.put("burndata文件开始烧写")
            self.ssholt.exec_cmd("rm -rf /config/work/burndata.config")
            print("rm -rf burndata.config执行成功")
            self.makeBurndataFile(mac, sn)
            logQueue.put("burndata文件生成")
            self.ssholt.upload("config/burndata.config", "/config/work/burndata.config")
            logQueue.put("burndata文件烧写完成")

            logQueue.put("sysinfo文件开始烧写")
            self.ssholt.exec_cmd("rm -rf /config/work/sysinfo.xml")
            print("rm -rf /config/work/sysinfo.xml执行成功")
            self.makeSysinfoFile(mac, sn)
            logQueue.put("sysinfo文件生成")
            self.ssholt.upload("config/sysinfo.xml", "/config/work/sysinfo.xml")
            logQueue.put("sysinfo文件烧写完成")

            # 需要用回读操作进行确认烧写成功
            logQueue.put("回读中...")
            stdin, stdout, stderr = self.ssholt.exec_cmd("cat /config/work/burndata.config")
            out1 = str(stdout.read(), encoding="utf-8", errors="ignore")
            if mac not in out1:
                logQueue.put("MAC烧写失败，请检查后重新烧写"),
                return False
            if sn not in out1:
                logQueue.put("SN烧写失败，请检查后重新烧写"),
                return  False
            logQueue.put("回读完成")

            logQueue.put("恢复出厂设置")
            self.ssholt.exec_cmd("rm -rf lastgood.xml")
            self.ssholt.exec_cmd("rm -rf backup_lastgood.xml")

            logQueue.put("重启设备中...")
            self.ssholt.exec_cmd("reboot -f")
            self.ssholt.close()
            logQueue.put("烧写完成。")
            logQueue.put("finish")

            self.ssholt.close()
            return True
        else:
            logQueue.append("连接超时...")
            logQueue.put("finish")
            return False

    def manualPro(self, ip, mac, sn, queue):
       return self.signalPro(ip, mac, sn, queue)

    def continuousPro(self, ip, mac, sn, queue):        # 后续补充
        logQueue = queue
        logQueue.put("正在连接HGU...")
        if not self.getLinkState(ip):
            logQueue.put("连接成功，开始烧写。")

            logQueue.put("烧写完成。")
            logQueue.put("finish")
        else:
            logQueue.append("连接超时...")
            logQueue.put("finish")

    def makeSysinfoFile(self, mac, sn):
        infoStr = "<sysinfo>\n\t<llid0_mac value = \"" + self.colonDelimited(mac) + "\"></llid0_mac>\n\t<llid1_mac value = \"" + self.colonDelimited(mac)[:8] + ":00:00:02\"></llid1_mac>\n\t<llid2_mac value = \"" + self.colonDelimited(mac)[:8] + ":00:00:03\"></llid2_mac>\n\t<llid3_mac value = \"" + self.colonDelimited(mac)[:8] + ":00:00:04\"></llid3_mac>\n\t<llid4_mac value = \"" + self.colonDelimited(mac)[:8] + ":00:00:05\"></llid4_mac>\n\t<llid5_mac value = \"" + self.colonDelimited(mac)[:8] + ":00:00:06\"></llid5_mac>\n\t<llid6_mac value = \"" + self.colonDelimited(mac)[:8] + ":00:00:07\"></llid6_mac>\n\t<llid7_mac value = \"" + self.colonDelimited(mac)[:8] + ":00:00:08\"></llid7_mac>\n\t<auid>\n\t\t<sn value = \"0x42 0x4C 0x4B 0x47 0x" + mac[-8:-6] + " 0x" + mac[-6:-4] + " 0x" + mac[-4:-2] + " 0x" + mac[-2:] + "\"></sn>\n\t\t<pwd value = \"0x20 0x20 0x20 0x20 0x20 0x20 0x20 0x20 0x20 0x20\"></pwd>\n\t</auid>\n\t<gateway_mac value = \"" + self.colonDelimited(mac) + "\"></gateway_mac>\n\t<product_sn value = \"" + mac[:6] + "-" + mac + "\"></product_sn>\n</sysinfo>"
        file = open("config/sysinfo.xml", 'wb')
        file.truncate()                                            # 若文件存在，清空文件
        file.write(infoStr.encode("ascii"))
        file.flush()
        file.close()


    def makeBurndataFile(self, mac, sn):
        burnStr = "WEB_USR=admin\nWEB_PWD=admin\nDEV_SN=6KYZG" + mac + "\nOUI=" + mac[:6] + "\nGPON_SN=" + sn + "\nPON_MAC="+ self.colonDelimited(mac) + "\nSSID=JSM-" + mac[-6:] + "\nSSID_PWD=00000000"
        file = open("config/burndata.config", 'wb')
        file.truncate()                                             # 若文件存在，清空文件
        file.write(burnStr.encode("ascii"))
        file.flush()
        file.close()

    def colonDelimited(self,mac):
        return mac[:2] + ":" + mac[2:4] + ":" + mac[4:6] + ":" + mac[6:8] + ":" + mac[8:10] + ":" + mac[10:]

# if __name__ == "__main__":
#     mac = "B8BA680F0001"
#     sn = "B8BA680F0001"
#     ssh = SSHOLT()
#     ssh.authSSH("192.168.0.1", 22, "root", "nE7jA%5m")
#     stdin, stdout, stderr = ssh.exec_cmd("cat /config/work/burndata.config")
#     # ssh.upload("config/burndata.config", "/config/work/burndata.config")
#     out1 = str(stdout.read(), encoding="utf-8", errors="ignore")
#     print(out1)
#     if mac not in out1:
#         print("MAC烧写失败，请检查后重新烧写"),
#     if sn not in out1:
#         print("SN烧写失败，请检查后重新烧写"),
#     print("回读完成")
#
#     ssh.close()
