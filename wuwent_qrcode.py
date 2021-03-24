import os
import configparser

import qrcode

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

base_url = os.path.dirname(__file__)


class BaseQr(object):
    def __init__(self):
        config_parser = configparser.ConfigParser()
        config_path = os.path.join(os.getcwd(), 'qrcode.ini')
        config_parser.read(config_path)
        self.font_size = self.__hander(config_parser, 'FONT_SIZE')
        self.font_location = self.__hander(config_parser, 'FONT_LOCATION')
        self.font_color = self.__hander(config_parser, 'FONT_COLOR')
        self.qr = config_parser._sections.get('QRCODE')
        self.qr_img = os.path.join(base_url, self.qr.get('qr_img') + '/')
        self.bg_bir = os.path.join(base_url, self.qr.get('bg_bir'))
        self.ttf_bir = os.path.join(base_url, self.qr.get('ttf_bir'))

    def __hander(self, config_parser, key):
        return [(key, value) for key, value in config_parser._sections.get(key).items()]

    def __split(self, data):
        return tuple([int(i) for i in data.split('-')])

    def init_data(self, img_name, data, fonts_data):
        self.data = data
        self.img_name = img_name
        self.fonts_data = list(zip(self.font_size, self.font_location, self.font_color, fonts_data))

    # 生成二维码
    def make_qr(self, data):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=self.qr.get('box_size'),
            border=self.qr.get('border'),
        )
        # 添加数据
        qr.add_data(data)
        # 填充数据
        qr.make(fit=True)
        # 生成图片
        img = qr.make_image(fill_color=self.qr.get("fill_color"), back_color=self.qr.get("back_color"))
        img = img.convert("CMYK")  # RGBA

        img = img.convert('RGB')
        img.save(self.qr_img + self.img_name + '.png')

    # 填充文字
    def add_font(self, font_info, font_size=None, font_location=None, font_color=None):
        oriImg = Image.open(self.qr_img + self.img_name + ".png")
        draw = ImageDraw.Draw(oriImg)
        font = ImageFont.truetype(self.ttf_bir, int(font_size))  # 设置字体
        # 字体的位置 、颜色
        draw.text(self.__split(font_location), font_info, self.__split(font_color), font=font)  # 把字添加到图片上
        oriImg = oriImg.convert('RGB')
        oriImg.save(self.qr_img + self.img_name + '.png')

    def add_fonts(self):
        for font_data in self.fonts_data:
            self.add_font(font_data[-1][-1], font_data[0][-1], font_data[1][-1], font_data[2][-1])

    # 在背景图片上布局二维码和字体
    def make(self, img_name, data, fonts_data):
        '''

        :param img_name: 保存二维码的图片名
        :param data: 手机扫码后得到的数据
        :param fonts_data: fonts_data: (('font1', str), ('font2', str), ...)
        :return:
        '''
        self.init_data(img_name, data, fonts_data)
        self.make_qr(data)
        oriImg = Image.open(self.bg_bir)
        oriImg2 = Image.open(self.qr_img + self.img_name + '.png')
        oriImg2 = oriImg2.resize(self.__split(self.qr.get('size')))  # 设置二维码大小
        oriImg.paste(oriImg2, self.__split(self.qr.get('location')))  # 将二维码放在底图上
        oriImg.save(self.qr_img + self.img_name + '.png')
        self.add_fonts()
