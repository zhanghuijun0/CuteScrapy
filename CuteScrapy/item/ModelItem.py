import scrapy

from CuteScrapy.model.blogs import Blogs


class ModelItem(scrapy.Item):
    model = scrapy.Field()

    @classmethod
    def getInstance(cls, model):
        modelItem = cls()
        modelItem['model'] = model
        return modelItem


if __name__ == '__main__':
    print ModelItem.getInstance(Blogs())
