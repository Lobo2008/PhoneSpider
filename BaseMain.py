



import sys

sys.path.append('/Users/lobo/Documents/Code/Spider')
from Son import Son

from Daddy import Daddy

from Base import Base
from Son_91Ma import Son_91Ma
from Son_XunMa import Son_XunMa

if __name__ == '__main__':

    # xunma = XunMa('test_qq','12345678')
    # xunma.spider()

    # jiuyima = JiuYiMa_91('hzw12356','123456qwe')
    # jiuyima.spider()

    # son = Son('','')
    # son.spider()
    son_91ma = Son_91Ma('hzw12356','123456qwe')
    son_91ma.spider()

    # son_xunma = Son_XunMa('test_qq','12345678')
    # son_xunma.spider()

