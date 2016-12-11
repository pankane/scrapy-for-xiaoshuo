#!/bin/bash
#!/usr/bin/python
PATH=$PATH:/usr/local/bin
export PATH
cd /home/pi/Documents/scrapy/xiaoshuo/xiaoshuo

startCrawl(){
echo $1 > novelName.jl
echo $(head -1 $1.jl) > pageNumber.jl
scrapy crawl xiaoshuo
echo $(head -1 'pageNumber.jl') > $1.jl
}

today=$(date +%w)
echo $today

case $today in
    
    
    1)
        startCrawl '择天记'
        ;;
    2)
        startCrawl '走进修仙'
        ;;
    3)
        startCrawl '重生之都市修仙'
        ;;
    4)
        startCrawl '不朽凡人'
        startCrawl '飞天'
        ;;
    5)
        startCrawl '异常生物见闻录'
        startCrawl '天道图书馆'
        ;;
    6)
        startCrawl '巫师之旅'
        ;;
    0)
        startCrawl '一念永恒'
        startCrawl '圣虚'
        ;;
esac
