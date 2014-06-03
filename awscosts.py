#!/usr/bin/python

from pprint import pprint
import locale
import logging
import sys

sys.path.append('./botowrapper')
from BotoWrapper import BotoWrapper

AWS_ACCESS_KEY_ID = "REPLACEME"
AWS_SECRET_ACCESS_KEY = "REPLACEME"
APPLIST = ['REPLACEME', 'REPLACEME']

AWS_COSTS = {
    't1.micro':.020,
    'm1.small':.044,
    'm1.medium':.087,
    'm1.large':.175,
    'm1.xlarge':.350,
    'c1.medium':.130,
    'c1.xlarge':.520,
    'cc2.8xlarge':2.00,
    'm2.xlarge':.245,
    'm2.2xlarge':.490,
    'm2.4xlarge':.980,
    'cr1.8xlarge':3.50,
    'm3.medium':.070,
    'm3.large':.140,
    'm3.xlarge':.280,
    'm3.2xlarge':.560,
    'c3.large':.105,
    'c3.xlarge':.210,
    'c3.2xlarge':.420,
    'c3.4xlarge':.840,
    'c3.8xlarge':1.680,
    'r3.large':.175,
    'r3.xlarge':.350,
    'r3.2xlarge':.700,
    'r3.4xlarge':1.40,
    'r3.8xlarge':2.80
}


def main(argv=None):
    _logger = setupLogging()
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    botowrapper = BotoWrapper(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY)

    run(_logger, botowrapper)


def run(_logger, botowrapper):

    resource = {}
    serverlist = botowrapper.getAllInstances()
    #_logger.info(serverlist)
    for res in serverlist:
        for instance in res.instances:
            #_logger.info(instance)
            if instance.state == 'running':
                type = getAppType(instance)
                #_logger.info('Type Found:' + type)
                #get instance data
                resource = addToGroup(resource, type, instance)
                if type == 'other':
                    _logger.info(instance.tags['Name'])

    #_logger.info(resource)
    printOutput(resource)


def printOutput(data):
    for app in data:
        print("APPLICATION: " + app + " \n")
        daily = 0
        hourly = 0
        weekly = 0

        for servers in data[app]:
            daily += servers['cost']['daily']
            hourly += servers['cost']['hourly']
            weekly += servers['cost']['weekly']
        print("Cost: Daily: " + "{0:.2f}".format(daily))
        print("Cost: Monthly: " + "{0:.2f}".format(daily*30))
        print("---------")


    for app in data:
        daily = 0
        hourly = 0
        weekly = 0

        for servers in data[app]:
            daily += servers['cost']['daily']
            hourly += servers['cost']['hourly']
            weekly += servers['cost']['weekly']


        print app+","+"{0:.2f}".format(daily)+","+"{0:.2f}".format(daily*30)+"\n"



def addToGroup(res, app, instance):
    cst = getCost(instance.instance_type)
    cost = {'hourly':cst, 'daily':float(cst)*24, 'weekly':float(cst)*24*7}
    grp = {'instance_type':instance.instance_type,
               'name':instance.tags['Name'],
               'launched':instance.launch_time,
               'state':instance.state,
               'cost':cost
               }
    if instance.state != 'running':
        return res

    if app in res:
        list = res[app]
        list.append(grp)
        res[app] = list
    else:
        res[app]=[grp]

    return res

def getCost(type):
    try:
        result = AWS_COSTS[type]
    except KeyError, e:
        result = 0.0

    return result

def getAppType(item):
    nametag = item.tags['Name']
    for app in APPLIST:
        if app in nametag.lower():
            return app

    return 'other'


def setupLogging(logname="awscosts"):
    logger = logging.getLogger(logname)
    logfile = logging.FileHandler(logname+'.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    logfile.setFormatter(formatter)
    logger.addHandler(logfile)
    logger.setLevel(logging.INFO)

    return logger

if __name__ == '__main__':
    main()

__author__ = 'warrenchang'
