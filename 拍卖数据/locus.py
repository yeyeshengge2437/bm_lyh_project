# =======================
# --*-- coding: utf-8 --*--
# @Author  : 微信公众号：K哥爬虫
# @Software: PyCharm
# =======================
import random
from loguru import logger


class KsTrack:
    @staticmethod
    def __ease_out_expo(x) -> float:
        if x == 1:
            return 1
        else:
            return 1 - pow(2, -10 * x)

    @staticmethod
    def deal_track(slide_track: list) -> str:
        result = ''
        for i in slide_track:
            result += "|".join([str(x) for x in i]) + ','
        return result[:-1]

    def get_slide_track(self, distance) -> str:
        """
        根据滑动距离生成滑动轨迹
        :param distance: 需要滑动的距离
        :return: 滑动轨迹 <type 'list'>: [[x,y,t], ...]
            x: 已滑动的横向距离
            y: 已滑动的纵向距离, 除起点外, 均为 0
            t: 滑动过程消耗的时间, 单位: 毫秒
        """
        if not isinstance(distance, int) or distance < 0:
            raise ValueError(f"distance 类型必须是 >=0 的整数: distance: {distance}, type: {type(distance)}")

        # 初始化轨迹列表
        init_x = random.randint(0, 5)
        init_y = random.randint(15, 17)
        t = 0
        slide_track = [
            [init_x, init_y, t]
        ]
        # 共记录 count 次滑块位置信息
        count = 30 + int(distance / 2)
        # 记录上一次滑动的距离
        init_x = 0
        for i in range(count):
            # 已滑动的横向距离
            x = round(self.__ease_out_expo(i / count) * distance)
            # 滑动过程消耗的时间
            t += self.__ease_out_expo(i / count) * random.randint(10, 20)
            if t == 0:
                t += random.randint(5, 10)
            if x == init_x:
                continue
            y = random.randint(init_y - 3, init_y + 3)
            slide_track.append([x, y, int(t)])
            init_x = x
        # return self.deal_track(slide_track)
        return slide_track

    def main(self, slide_distance=500, fine_tune=1.62):
        # 500 -> 滑动距离
        # 1.62 -> 微调
        distance = int(slide_distance * fine_tune)
        # 轨迹
        track = self.get_slide_track(distance)
        logger.info(track)
        return track


# if __name__ == '__main__':
#     KsTrack().main()
