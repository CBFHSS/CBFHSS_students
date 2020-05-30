import os
from apscheduler.schedulers.blocking import BlockingScheduler
import sys
import datetime
from datetime import date, datetime, timedelta
import time
import calendar
from services import delete,push,backuptemperture
if __name__ == '__main__':
    
    service = BlockingScheduler(timezone="Asia/Taipei")

    service.add_job(backuptemperture.run,'cron',hour=0,minute=0)
    service.add_job(delete.run,'cron',hour=16,minute=48)
    service.add_job(push.push,'cron',day_of_week='mon-fri',hour=16,minute=50)
 
    try:
        service.start()
        
    except (KeyboardInterrupt, SystemExit):
        pass
