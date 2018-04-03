import paramiko
import interactive
#记录日志
paramiko.util.log_to_file('log/test')
#建立ssh连接
ssh=paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.0.1',port=22,username='root',password='nE7jA%5m',compress=True)
#建立交互式shell连接
channel=ssh.invoke_shell()
#建立交互式管道
interactive.interactive_shell(channel)
#关闭连接
channel.close()
ssh.close()





class SSHConnection(object):
    def __init__(self, host='192.168.0.1', port=22, username='root', pwd='nE7jA%5m'):
        self.host = host
        self.port = port
        self.username = username
        self.pwd = pwd
        self.__k = None

    def run(self):
        self.connect()
        pass
        self.close()

    def connect(self):
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.pwd)
        self.__transport = transport

    def close(self):
        self.__transport.close()

    def cmd(self, command):
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        # 执行命令
        stdin, stdout, stderr = ssh.exec_command(command)
        # 获取命令结果
        result = stdout.read()
        return result

    def upload(self, local_path, target_path):
        # 连接，上传
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        # 将location.py 上传至服务器 /tmp/test.py
        sftp.put(local_path, target_path)
