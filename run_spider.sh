#export PYTHONPATH=/Users/huijunzhang/PycharmProjects/CuteScrapy
cd /Users/huijunzhang/PycharmProjects/CuteScrapy
scrapy crawl cnblogs.list >> blogs.log 2>&1 &
scrapy crawl csdn.list >> blogs.log 2>&1 &
scrapy crawl oschina.list >> blogs.log 2>&1 &
scrapy crawl movies.dyxz5 >> movies.log 2>&1 &
#scrapy crawl movies.mp4ba >> movies.log 2>&1 &
