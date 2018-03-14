import paramiko



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