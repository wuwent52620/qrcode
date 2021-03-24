就看wuwent_qrcode文件里的make方法的传参说明就完事了

二维码生成在qrcodes文件夹里.

配置文件注意配置font时，每个font都要配置并且运行make时都要传值，

def make(self, img_name, data, fonts_data):
        '''
        :param img_name: 保存二维码的图片名
        :param data: 手机扫码后得到的数据
        :param fonts_data:  fonts_data: (('font1', str), ('font2', str), ...)  ------ 这些是显示在二维码上的文字信息
        '''

参考演示可运行test.py文件。