import paramiko


# transport =  paramiko.Transport(("192.168.0.1", 22))
#
# transport.connect(username="root", password="nE7jA%5m")
# # channel = transport.open_session()
# # sftpclient = paramiko.SFTPClient(channel)
# sftpclient = paramiko.SFTPClient.from_transport(transport)
# sftpclient.put("config/burndata.config", "/config/work/burndata.config")
# sftpclient.close()


