import hashlib


class crypo_ex:
    @staticmethod
    def get_md5(s=''):
        m = hashlib.sha3_512(s.encode())
        return m.hexdigest()

    @staticmethod
    def get_sha1(s=''):
        sha1 = hashlib.sha1(s.encode()).hexdigest()
        return sha1


class key_gen():
    @staticmethod
    def get_key(str1='', str2=''):
        ret1 = crypo_ex.get_md5(str1)
        ret2 = crypo_ex.get_sha1(str2)
        str3 = "{0}.{1}".format(ret1, ret2)
        ret3 = crypo_ex.get_sha1(str3)
        return ret3


if __name__ == "__main__":
    ret = key_gen.get_key('111', '222')
    print(ret)