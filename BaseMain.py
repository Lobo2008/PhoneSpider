



import sys

sys.path.append('/Users/lobo/Documents/Code/PhoneSpider')

# from Daddy import Daddy
# from Son import Son


from Base import Base
from Son_91Ma import Son_91Ma
from Son_XunMa import Son_XunMa
from Son_YunMa import Son_YunMa

from Son_XingGuangMa import Son_XingGuangMa
from Son_HuoYunMa import Son_HuoYunMa


if __name__ == '__main__':


    # son = Son('','')
    # son.spider()
    
    # son_91ma = Son_91Ma('hzw12356','123456qwe')
    # son_91ma.spider()

    # son_xunma = Son_XunMa('test_qq','12345678')
    # son_xunma.spider()

    # son_yunma = Son_YunMa('test_qq','12345678')
    # son_yunma.spider()


    # print(sys.getdefaultencoding()  ) # utf-8
    
    # xinguangma = Son_XingGuangMa('xiaoxiaolong668','123')
    # xinguangma.spider()

    huoyunma = Son_HuoYunMa('xiaoxiaolong668','z12345')
    huoyunma.spider()