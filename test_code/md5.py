import hashlib
#import md5 #Python2里的引用
s='python321'
# s.encode()#变成bytes类型才能加密
m= hashlib.md5(s.encode())
print("md51=",m.hexdigest())

m=hashlib.sha3_224(s.encode()) #长度是224
print("md52=",m.hexdigest())

m=hashlib.sha3_256(s.encode())  #长度是256
print("md53=",m.hexdigest())

m=hashlib.sha3_512(s.encode()) #长度是512
print("md54=",m.hexdigest())

data="123456789"
sha1 = hashlib.sha1(data.encode()).hexdigest()
print(sha1)

def sha256hex(data):
    sha256 = hashlib.sha256()
    sha256.update(data.encode())
    res = sha256.hexdigest()
    print("sha256加密结果:", res)
    return res
data = "123456789"
sha256hex(data)