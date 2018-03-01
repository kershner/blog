cd /home/tylerkershner

venv/bin/python -m app.scripts.scrape_reddit
sleep 5
venv/bin/python -m app.scripts.clean_up_urls
