#!/bin/bash
source ~/.bash_source
# conda activate scrapy
cd ~/weather_crawler
python main.py > ~/log/WeatherCrawlerLog/$(date +%Y-%m-%d_%T) 2>&1
