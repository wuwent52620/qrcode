from wuwent_qrcode import BaseQr

a = BaseQr()

a.make(img_name='test1', data='微信扫码可得值wuwent, 自己定义', fonts_data=(('font1', '班级： 我也不知道'), ('font2', '姓名： 胡作超 ')))