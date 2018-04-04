import socket

    ss = socket.socket()
    ss.bind()
    ss.listen()
    inf_loop:
    cs = ss.accept()
    comm_loop:
    cs.recv()/cs.send()
    cs.close()
ss.close()




