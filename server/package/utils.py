import socket
def getServerIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 不需要连接到真正的服务器，只需要尝试解析主机名即可触发IP配置的查询
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
    except Exception as e:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

if __name__ == '__main__':
    aa = getServerIp()
    print(aa)