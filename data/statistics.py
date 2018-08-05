import pymongo
import pygal


class Result(object):

    client = pymongo.MongoClient('localhost')
    db = client.bilibili
    data = db.recently_submission

    list = ['王者荣耀', '300英雄', '绝地求生', 'CS：GO', '穿越火线', '英雄联盟', '刺激战场', 'QQ飞车', '第五人格', '守望先锋',
            '星际争霸', '彩虹6号', 'DOTA2', '风暴英雄', '炉石传说', '决战平安京', '皇室战争', '崩坏']

    def picture(self):
        count = []
        for i in self.list:
            a = self.data.find({'logs':{'$regex': i}}).count()
            count.append(a)

        my_config = pygal.Config()
        # x轴的文字旋转45度
        my_config.x_label_rotation = -45
        result = pygal.Bar(my_config)

        result.title = "Results of Games Upload Counts."
        result.x_labels = self.list
        result.x_title = 'Games'
        result.y_title = 'Counts'

        result.add('Bilibili', count)
        result.render_to_file('result_visual.svg')


if __name__ == '__main__':
    result = Result()
    result.picture()