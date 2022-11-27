#!/usr/bin/bash
################################################################################
#to set up cronjobs on a VM or on your own laptop or something:
#run <crontab -e> in your terminal
#paste this line:
#*/30 * * * * . /home/njf21/project/scraper/run_schedule.sh
#then save and quit (ctrl s, then ctrl x)
#then finally change all the absolute paths below.
################################################################################

#TODO change file name from project/scraper to project/scraper_app
#TODO not totally happy with the use of absolute paths but this is not prio to fix

#starts the virtualenv you need
. /home/njf21/project/venv/bin/activate

#navigates to the directory containing scrapy root (scrapy.cfg)
cd /home/njf21/project/scraper_app


#runs the spiders in series - each cronjob creates a new thread and mongo deals with
#concurrent writes so this solution is completely fine for us right now.
#If you want to add more scrapers just follow this pattern but replace the last arg
/home/njf21/project/venv/bin/scrapy crawl guardian_articles
/home/njf21/project/venv/bin/scrapy crawl andreessen_horowitz_articles
#/home/njf21/project/venv/bin/scrapy crawl zdnet_articles
/home/njf21/project/venv/bin/scrapy crawl bbc_articles

#kills virtualenv
deactivate
