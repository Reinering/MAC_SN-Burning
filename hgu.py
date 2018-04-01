# -*- coding: utf-8 -*-
#python35

import paramiko
import subprocess
import time
from pykeyboard import PyKeyboard
import sys

class SSHOLT(object):

    def __init__(self):
        self.client = paramiko.SSHClient()

    def auth(self, host, port, usr, pwd):
        try:
            # key = paramiko.RSAKey.from_private_key_file(pkeyFile, password=pkeyPwd)
            self.client.load_system_host_keys()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 通过公共方式进行认证 (不需要在known_hosts 文件中存在)
            # self.client.connect(host, port, username=usr, password=pwd, pkey=key)
            self.client.connect(host, port=port, username=usr, password=pwd)
            # self.transport = self.client.get_transport()
            # self.client._transport = self.transport
            self.channel = self.client.invoke_shell()
            # self.channel = self.transport.open_session()
        except paramiko.ssh_exception.NoValidConnectionsError as e:
            print("ssh登录错误：", e)
        except TimeoutError as e:
            print("登录超时：", e)
        except ConnectionError as e:
            print("建立失败：", e)
        self.read()

    def exec_cmd(self, cmd):
        print(cmd)
        self.client.exec_command(cmd)
        # self.channel.invoke_shell()
        # if self.channel.active:
        #     try:
        #         self.channel.exec_command(cmd)
        #         out = self.channel.recv(1024)
        #         sys.stdout.write(str(out, encoding="utf-8", errors="ignore"))
        #         sys.stdout.flush()
        #     except paramiko.SSHException as e:
        #         print(e)
        #         print("Channel已关闭")
        # else:
        #     print("Channel已关闭")


    def send(self, str):
        # print(str)
        # self.channel = self.transport.open_session()
        if self.channel.active:
            try:
                self.channel.send(str)
                self.channel.send(b'0x1b')
                self.channel.send(":wq")
            except paramiko.SSHException as e:
                print(e)
                print("Channel已关闭")
        else:
            print("Channel已关闭")
        # self.channel.close()

    def write(self, str):
        # self.stdin.write(str)
        pass

    def close(self):
        # self.transport.close()
        self.client.close()

    def read(self):
        import threading
        sys.stdout.write("Line-buffered terminal emulation. Press F6 or ^Z to send EOF.rnrn")

        def writeall(sock):
            while True:
                data = sock.recv(256)
                if not data:
                    sys.stdout.write('rn*** EOF ***rnrn')
                    sys.stdout.flush()
                    break
                sys.stdout.write(str(data, encoding="utf-8", errors="ignore"))
                sys.stdout.flush()

        writer = threading.Thread(target=writeall, args=(self.channel,))
        writer.start()


class Programing(object):

    def __init__(self, ):
        self.ssholt = SSHOLT()
        self.kb = PyKeyboard()

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
            try:
                self.ssholt.auth(ip, 22, "root", "nE7jA%5m")
                logQueue.put("连接成功，开始烧写。")
            except Exception as e:
                print(e)
                logQueue.put("SSH登录失败")
                return False
            time.sleep(2)
            logQueue.put("burndata文件开始烧写")
            self.ssholt.exec_cmd("rm -rf /config/work/burndata.config")
            time.sleep(0.5)
            print("rm -rf burndata.config执行成功")
            self.ssholt.exec_cmd("vi /config/work/burndata.config")
            time.sleep(0.5)
            print("vi burndata.config执行成功")
            # self.ssholt.send(self.makeBurndata(mac, sn))
            time.sleep(0.5)
            # self.ssholt.send(b'0x1b')
            # self.ssholt.send(":wq")
            # stdin.write(self.makeBurndata(mac, sn))
            # stdin.flush()
            # data = stdout.read().splitlines()
            # for line in data:
            #     if line:
            #         print(line)
            # # self.ssholt.exec_cmd(self.makeBurndata(mac, sn))
            # # self.ssholt.exec_cmd(self.kb.escape_key)                                               #退出Vi编辑器命令
            # self.ssholt.exec_cmd(":wq")
            # print(":wq执行成功")
            # logQueue.put("burndata文件烧写完成")
            #
            # logQueue.put("sysinfo文件开始烧写")
            # self.ssholt.exec_cmd("rm -rf /config/work/sysinfo.xml")
            # self.ssholt.exec_cmd("rm -rf sysinfo.xml")
            # self.ssholt.exec_cmd("vi sysinfo.xml")
            # self.ssholt.exec_cmd(self.makeSysinfo(mac,sn))
            # self.ssholt.exec_cmd(b'0x1b')                                               #退出Vi编辑器命令
            # self.ssholt.exec_cmd(":wq")
            # logQueue.put("sysinfo文件烧写完成")
            #
            # #需要用回读操作进行确认烧写成功
            # # logQueue.put("回读中...")
            # # stdin1, stdout1, stderr1 = self.ssholt.exec_cmd("cat burndata.config")
            # # out1 = str(stdout1, encoding="gb2312", errors="ignore")
            # # if mac not in out1:
            # #     logQueue.put("MAC烧写失败，请检查后重新烧写"),
            # #     return False
            # # if sn not in out1:
            # #     logQueue.put("SN烧写失败，请检查后重新烧写"),
            # #     return  False
            # # logQueue.put("回读完成")
            # #
            # logQueue.put("恢复出厂设置")
            # self.ssholt.exec_cmd("rm -rf lastgood.xml")
            # self.ssholt.exec_cmd("rm -rf backup_lastgood.xml")
            #
            # logQueue.put("重启设备中...")
            # self.ssholt.exec_cmd("reboot -f")
            # self.ssholt.close()
            # logQueue.put("烧写完成。")
            # logQueue.put("finish")
            return True
        else:
            logQueue.append("连接超时...")
            logQueue.put("finish")
            return False


    def continuousPro(self, ip, mac, sn, queue):
        logQueue = queue
        logQueue.put("正在连接HGU...")
        if not self.getLinkState(ip):
            logQueue.put("连接成功，开始烧写。")

            logQueue.put("烧写完成。")
            logQueue.put("finish")
        else:
            logQueue.append("连接超时...")
            logQueue.put("finish")

    def manualPro(self):
        pass

    def makeSysinfo(self, mac, sn):
        infoStr = "<sysinfo>\n\t<llid0_mac value = \"" + self.colonDelimited(mac) + "\"></llid0_mac>\n\t<llid1_mac value = \"" + self.colonDelimited(mac)[:8] + ":00:00:02\"></llid1_mac>\n\t<llid2_mac value = \"" + self.colonDelimited(mac)[:8] + ":00:00:03\"></llid2_mac>\n\t<llid3_mac value = \"" + self.colonDelimited(mac)[:8] + ":00:00:04\"></llid3_mac>\n\t<llid4_mac value = \"" + self.colonDelimited(mac)[:8] + ":00:00:05\"></llid4_mac>\n\t<llid5_mac value = \"" + self.colonDelimited(mac)[:8] + ":00:00:06\"></llid5_mac>\n\t<llid6_mac value = \"" + self.colonDelimited(mac)[:8] + ":00:00:07\"></llid6_mac>\n\t<llid7_mac value = \"" + self.colonDelimited(mac)[:8] + ":00:00:08\"></llid7_mac>\n\t<auid>\n\t\t<sn value = \"0x42 0x4C 0x4B 0x47 0x" + mac[-8:-6] + " 0x" + mac[-6:-4] + " 0x" + mac[-4:-2] + " 0x" + mac[-2:] + "\"></sn>\n\t\t<pwd value = \"0x20 0x20 0x20 0x20 0x20 0x20 0x20 0x20 0x20 0x20\"></pwd>\n\t</auid>\n\t<gateway_mac value = \"" + self.colonDelimited(mac) + "\"></gateway_mac>\n\t\t<product_sn value = \"" + self.colonDelimited(mac)[:8] + "-" + self.colonDelimited(mac) + "\"></product_sn>\n</sysinfo>"
        return infoStr
    def makeBurndata(self, mac, sn):
        burnStr = "WEB_USR=admin\nWEB_PWD=admin\nDEV_SN=6KYZG" + mac + "\nOUI=" + mac[:6] + "\nGPON_SN=" + sn + "\nPON_MAC="+ self.colonDelimited(mac) + "\nSSID=JSM-" + mac[-6:] + "\nSSID_PWD=00000000"
        return burnStr

    def colonDelimited(self,mac):
        return mac[:2] + ":" + mac[2:4] + ":" + mac[4:6] + ":" + mac[6:8] + ":" + mac[8:10] + ":" + mac[10:]
