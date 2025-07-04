import execjs
import hashlib
import requests
import json
from urllib.parse import quote
import time
import logging

username = ''
password = ''


# 配置日志记录
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s'
)



def check_domain_connectivity(domain='auth.nyist.edu.cn', port=80, timeout=1):
    """
    检查指定域名和端口的连通性。
    
    参数:
        domain (str): 要检查的域名，默认为 'auth.nyist.edu.cn'
        port (int): 要检查的端口，默认为 80
        timeout (int): 连接超时时间（秒），默认为 1
    
    返回:
        bool: 如果域名解析且连接成功返回 True，否则返回 False
    """
    try:
        # 解析域名，获取所有可能的地址信息（IPv4 和 IPv6）
        addrinfo_list = socket.getaddrinfo(
            domain, port, 
            family=socket.AF_UNSPEC,  # 接受所有地址族
            type=socket.SOCK_STREAM,  # 流式socket（TCP）
            proto=socket.IPPROTO_TCP
        )
    except socket.gaierror:
        # 域名解析失败
        return False
    
    # 遍历所有解析到的地址尝试连接
    for addrinfo in addrinfo_list:
        af, socktype, proto, _, sa = addrinfo
        try:
            # 创建socket对象，使用with确保关闭
            with socket.socket(af, socktype, proto) as sock:
                sock.settimeout(timeout)
                sock.connect(sa)
                # 连接成功
                return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            # 超时、拒绝连接或其他错误，继续尝试下一个地址
            continue
        except Exception:
            # 其他异常，继续尝试下一个地址
            continue
    
    # 所有地址均无法连接
    return False

def checkAuth():
    if check_domain_connectivity():
    	return 
    logging.warning('等待连接校园网中...')
    while True:
    	time.sleep(5)
    	if check_domain_connectivity():
    		break
    return 

def print(x,y=None,z=None):return
headers = {
  'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
  'Accept-Language': 'zh-CN,zh;q=0.9',
  'Cache-Control': 'no-cache',
  'Connection': 'keep-alive',
  'Pragma': 'no-cache',
  'Referer': 'https://auth.nyist.edu.cn/srun_portal_pc?ac_id=1&theme=pro',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
  'X-Requested-With': 'XMLHttpRequest',
  'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"'
}

def js_from_file(file_name):
    with open(file_name, 'r', encoding='UTF-8') as file:
        return file.read()

js_context = execjs.compile(js_from_file('./a.js'))



def get_challenge(username):
    url = f"https://auth.nyist.edu.cn/cgi-bin/get_challenge?callback=jQuery11&username={username}"

    response = requests.request("GET", url, headers=headers)

    data = json.loads(response.text[9:-1])
    return data['challenge'],data['client_ip']

def get_url(username,password,ip,acid,enc_ver,token):
    pram_password,pram_U_chksum,pram_info = js_context.call("GetPram", username, password,ip,acid,enc_ver,token).split("pram_js")
    pram_chksum = hashlib.sha1(pram_U_chksum.encode("utf-8")).hexdigest()
    logging.warning(f"username>>>{username}")
    print("password",password)
    logging.warning(f"ip>>>{ip}")
    print("acid",acid)
    print("enc_ver",enc_ver)
    print("token",token)
    print("pram_password",pram_password)
    print("pram_chksum",pram_chksum)
    print("pram_info",pram_info)
    timestamp = int(time.time() * 1000)-(1731589126170-1731589498000)
    print("timestamp",timestamp)
    url=f"https://auth.nyist.edu.cn/cgi-bin/srun_portal?callback=jQuery123&action=login&username={username}&password=%7BMD5%7D{pram_password}&os=不想996&name=Windows&double_stack=0&chksum={quote(pram_chksum)}&info={quote(pram_info).replace('/','%2F')}&ac_id={acid}&ip={ip}&n=200&type=1&_={timestamp}"
    return url
def get_srun_portal(username,password,ip,acid,enc_ver,token):
    url = get_url(username,password,ip,acid,enc_ver,token)
    print(url)
    response = requests.request("GET", url, headers=headers)
    logging.warning(response)
    return response.text




acid = '1'
enc_ver = 'srun_bx1'
def connectAuth():
    checkAuth()
    try:
        token,ip = get_challenge(username)
        print(get_srun_portal(username,password,ip,acid,enc_ver,token))
    except:
        time.sleep(1)
        connectAuth()


import socket



class UDPClient:
    def __init__(self, server_ip, server_port, auth_port=54321, retry_interval=5):
        self.server_ip = server_ip
        self.server_port = server_port
        self.auth_port = auth_port
        self.retry_interval = retry_interval
        self.auth_status = False  # 认证状态

    

    def run(self):
        """主运行循环"""
        while True:
            sock = None
            try:
                # 创建UDP套接字
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(2)
                sock.connect((self.server_ip, self.server_port))
                logging.info(f"已连接到服务器 {self.server_ip}:{self.server_port}")

                # 数据交互循环
                while True:
                    try:
                        time.sleep(4)
                        # 发送数据
                        data = b"\x01"
                        sock.send(data)
                        logging.info(f"已发送 {len(data)} 字节数据")

                        # 接收响应
                        response = sock.recv(1024)
                        logging.info(f"收到回显: {response.decode()}")

                    except socket.timeout:
                        logging.error("接收超时，触发重认证流程")
                        raise  # 跳出内层循环
                    except ConnectionResetError:
                        logging.error("连接被重置")
                        raise
                    except Exception as e:
                        logging.error(f"数据交互异常: {e}")
                        raise

            except Exception as e:
                logging.error(f"通信故障: {e}")
                if sock:
                    sock.close()

                # 执行认证流程
                connectAuth()
                

            else:
                break  # 正常退出循环

import socket
import logging
import time

class TCPClient:
    def __init__(self, server_ip, server_port, auth_port=54321, retry_interval=5):
        self.server_ip = server_ip
        self.server_port = server_port
        self.auth_port = auth_port
        self.retry_interval = retry_interval
        self.auth_status = False
        self.connection = None  # 新增TCP持久连接对象

    def _connect(self):
        """TCP连接建立（含三次握手）"""
        try:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.settimeout(2)
            # 显式建立连接（触发三次握手）
            self.connection.connect((self.server_ip, self.server_port))  # [1,2](@ref)
            logging.info(f"TCP连接已建立 {self.server_ip}:{self.server_port}")
            return True
        except Exception as e:
            logging.error(f"连接失败: {e}")
            return False

    def _authenticate(self):
        """独立的认证连接（可复用TCP连接或新建）"""
        auth_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            auth_sock.connect((self.server_ip, self.auth_port))
            # 发送认证数据（示例）
            auth_sock.send(b"auth_request")
            response = auth_sock.recv(1024)
            self.auth_status = (response == b"auth_ok")
        except Exception as e:
            logging.error(f"认证失败: {e}")
        finally:
            auth_sock.close()

    def run(self):
        while True:
            try:
                if not self._connect():
                    raise ConnectionError("连接初始化失败")
                
                # 保持长连接进行数据交互
                while True:
                    time.sleep(4)
                    # 发送数据（TCP流式传输）
                    data = b"\x01"
                    self.connection.sendall(data)  # 确保完整发送[2](@ref)
                    logging.info(f"已发送 {len(data)} 字节（TCP保证顺序）")

                    # 接收响应（需处理粘包）
                    response = self.connection.recv(1024)
                    if not response:
                        raise ConnectionError("连接被服务器关闭")
                    logging.info(f"收到响应: {response.decode()}")

            except:
                logging.error(f"传输异常")
                self.connection.close()
                connectAuth()
                time.sleep(self.retry_interval)
            


def check_connection1(ip, port=80, timeout=1):
    """
    检查指定IP和端口的连通性
    :param ip: 目标IP地址
    :param port: 目标端口，默认为80
    :param timeout: 超时时间（秒），默认为1秒
    :return: 成功返回True，失败返回False
    """
    try:
        # 创建socket连接（自动处理IPv4/IPv6）
        with socket.create_connection((ip, port), timeout=timeout):
            logging.info(f"{ip}:{port} 连接成功")
        return True
    except socket.timeout:
        logging.error(f"{ip}:{port} 连接超时")
        connectAuth()
    except OSError as e:
        logging.error(f"{ip}:{port} 连接错误: {e}")
        connectAuth()
    return False

def start_monitoring(ip, port=80, interval=5):
    """
    启动监控循环
    :param ip: 监控的IP地址
    :param port: 监控的端口，默认为80
    :param interval: 检查间隔（秒），默认为5秒
    """
    while True:
        check_connection1(ip, port)
        time.sleep(interval)

if __name__ == "__main__":
    # 示例用法：监控192.168.1.1的80端口
    start_monitoring('122.207.209.6', 8080)#nyist图书馆
    #start_monitoring('220.181.111.232', 80)#baidu
    

if __name__ == "__main__":
    client = UDPClient(server_ip='34.230.40.69', server_port=40000)
    client.run()
while True:
    time.sleep(5)
    if check_domain_connectivity(domain='220.181.111.232', port=80, timeout=1):
        logging.warning('1')
        continue
    else:
        connectAuth()