



import sys
sys.path.append('/Users/lobo/Documents/Code/PhoneDecode')


from XunMa import XunMa

from JiuYiMa_91 import JiuYiMa_91

from MaiZiMa import MaiZiMa



if __name__ == '__main__':

    xunma = XunMa('test_qq','12345678')
    xunma.spider()

    # jiuyima = JiuYiMa_91('hzw12356','123456qwe')
    # jiuyima.spider()

    # maizima = MaiZiMa('xiaoxiaolong668','123') #账户余额不足
    # maizima.spider()
