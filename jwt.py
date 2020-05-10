import base64
import copy
import hmac
import json
import time

class Jwt():
    def __init__(self):
        pass

    @staticmethod
    def encode(payload,key,exp=300):

        #创建header
        header = {'alg':'HS256','typ':'JWT'}
        #创建header json str
        #separators 表示json串中用什么相连
        #sort_keys 表示json串按key输出
        header_j = json.dumps(header,separators=(',',':'),sort_keys=True)
        #base64 header
        header_bs = Jwt.b64encode(header_j.encode())

        #创建payload部分
        payload = copy.deepcopy(payload)
        #创建过期时间标记
        payload['exp']=int(time.time() + exp)
        #生存payload json
        payload_j = json.dumps(payload,separators=(',',':'),sort_keys=True)
        #base64 payload
        payload_bs = Jwt.b64encode(payload_j.encode())

        #生存sign预签串
        to_sign_str = header_bs + b'.' + payload_bs
        if isinstance(key,str):
            key = key.encode()
        #hmac new 中参数 需要用bytes
        hmac_obj = hmac.new(key,to_sign_str,digestmod='SHA256')
        sign = hmac_obj.digest()
        #生成sign的base64
        sign_bs = Jwt.b64encode(sign)

        return header_bs + b'.' + payload_bs + b'.' + sign_bs
    @staticmethod
    def b64encode(s):
        #替换原生base64中的 '='
        return base64.urlsafe_b64encode(s).replace(b'=',b'')

    @staticmethod
    def b64decode(bs):
        #将替换=后的base64 补回原来长度
        rem = len(bs) % 4
        bs += b'=' * (4-rem)
        return base64.urlsafe_b64decode(bs)

    @staticmethod
    def decode(token,key):
        #拆解token
        header_bs , payload_bs , sign = token.split(b'.')

        if isinstance(key , str):
            key = key.encode()
        #重新计算签名
        hm = hmac.new(key,header_bs + b'.' + payload_bs,digestmod='SHA256')
        #base64 签名
        new_sign = Jwt.b64encode(hm.digest())
        if sign != new_sign:
            #token违法，则raise
            raise JwtError('Your token is valid')
        #base64 decode payload_bs 输出json串
        payload_j = Jwt.b64decode(payload_bs)
        payload = json.loads(payload_j.decode())
        #获取时间戳
        exp = payload['exp']
        now = time.time()
        #对比两个时间戳
        if now > exp:
            #token过期
            raise JwtError('Your token is expired')
        return payload

        #如果检验成功
        #return payload明文
        #如果失败
        #raise异常
        #标准:1.签名是否相符 2.exp是否过期
class JwtError(Exception):
    def __init__(self,error_msg):
        self.error = error_msg
    def __str__(self):
        return '<JwtError error %s>'%(self.error)
if __name__ == '__main__':
    res = Jwt.encode({'username':'guoxiaonao'},'abcdef1234')
    print(res)
    print(Jwt.decode(res,'abcdef1234'))
