AWS Costs
===========

What is it?
===========
 AWS costs is a simple script to scan your AWS ec2 list and get a cost breakdown of your servers based on the server Name Tag.

Dependencies
===========
 This script uses my BotoWrapper class that can be found here: https://github.com/changzone/botowrapper

Install
======
 Make sure to add this to your import paths prior to referencing this module

 assumes your file path is ./botowrapper contains the BotoWrapper.py file
 sys.path.append('./botowrapper')
 from BotoWrapper import BotoWrapper


Examples of use
===============
 You'll need to modify a few things prior to using this script.
 1. Put in your AWS ACCESS key and SECRET key:
 AWS_ACCESS_KEY_ID = "<your key>"
 AWS_SECRET_ACCESS_KEY = "<your key>"

 2. UPDATE the variable APPLIST with values of your tags you want to group by.
    For example, if your servers have the Name tag attribute set to things like EC2-APP1-DEV-APP-01  then APP1 is a tag you want to group by.  
       This script does a regex against the values in APPLIST.

