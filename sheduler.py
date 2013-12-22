#! /usr/bin/env python
#coding=utf-8
from datetime import datetime
from apscheduler.scheduler import Scheduler
from amazon.models import Amazon_class



# def shedule():
# 	print datetime.datetime.now()

# if __name__ == '__main__':
#     sched = Scheduler(standalone=True)
#     sched.add_cron_job(shedule, minute=1)
#     sched.start()
def updateall():
    a = Amazon_class()
    # a.ProductID = 'B001130JN8'
    UpdateRest = a.UpdateAll()
    print UpdateRest    


sched = Scheduler(standalone=True)

job = sched.add_cron_job(updateall, second = 0)

sched.start()
