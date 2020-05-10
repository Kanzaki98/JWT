# 模拟Token加密解密工具jwt
## jwt的组成
#### 1.header
元数据格式如下：

​	{'alg':'HS256','typ':'JWT'}

​	alg算法 - 默认为HS256  typ - 默认JWT
#### 2.payload
{'exp':xxx,'iss':xx...}

​	1.公共声明

​		'exp'(Expiration Time) 过期时间（可选）

​		'nbf'(Not Before Time)生效时间，如果当前时间在nbf时间之前，则Token不被接受（可选）

​		'iss'(issuer) 签发者（可选）

​		'aud'(Audience)签发面向群体（可选）

​		'iat'(Issued At)创建时间（可选）

​	2.私有声明

​		用户可根据业务需要添加自己的标识

​		如username等

​		整体内容将会做base64处理，signature签名

​		用'.'连接header，payload和自定义的key
#### 3.sign
## jwt的加密过程
##### 1.将header和payload转换成json格式并用base64加密，再用'.'相连后用SHA256加密后生成sign，并用base64加密。
##### 2.最后用'.'连接base64加密后的header、payload、sign生成token。
## jwt的解密过程
##### 1.用'.'将token拆分成header、payload、sign。
##### 2.重新计算sign与拆分出来的sign比对是否相同，不相同则token错误
##### 3.将payload用base64解密转换城json格式，查看token是否过期
