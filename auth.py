#!/usr/bin/python
import paramiko
import boto3
import time
import subprocess
import awscli
import os
import sys
import getpass


def connection():
	print ("Creating ssh session")
	session = boto3.Session()
	ec2 = session.resource('ec2', region_name='us-east-2a')
	i = ec2.Instance(id='i-0f1343218c8520018') # instance id

	k = paramiko.RSAKey.from_private_key_file('sathi-ssh.pem')
	c = paramiko.SSHClient()
	c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try :
		c.connect( 'ec2-52-14-60-141.us-east-2.compute.amazonaws.com', username = "ec2-user", pkey = k)
		print(c)
		return c
	except Exception:
		print("The Server is unavalible at the moment")
		return None

def PerformCommand(command, information="", mode=None):
	print information
	if mode:
		return os.popen(command + " > /dev/null", mode)
	else:
		return os.popen(command + " > /dev/null")

def add_user(name,password):
	c = connection()
	if (c != None):
		stdin , stdout, stderr = c.exec_command(" printf 'Adding user info \n';" +
		                                        "sudo adduser " + str(name) + ";"
		                                        #"printf '\nAdding password \n';" +
		                                        #"sudo passwd sathi;" +
		                                        "printf '\n User added in SSH\n\n';")
		print ("User added in SSH")
		c.close()

def remove_user(name):
	c = connection()
	if (c != None):
		stdin , stdout, stderr = c.exec_command(" printf 'Removing user info \n';" +
		                                        "sudo userdel -r " + str(name) + ";"
		                                        "printf '\n User has been removed from SSH\n\n';")
		print ("User has been removed from SSH")
		c.close()



def main():
	if len(sys.argv) >= 2:
	    if sys.argv[1] == "--add":
	        name = raw_input("Enter the user name: ")
	        password = getpass.getpass('Enter your password: ')
	        add_user(name,password)
	    elif sys.argv[1] == "--rm":
			name = raw_input("Enter the user name: ")
			remove_user(name)
	else:
	    print "yolo"

if __name__ == '__main__':
  main()
