#!/usr/bin/python
import paramiko
import boto3
import time
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
		return c
	except Exception:
		print("The Server is unavalible at the moment")
		return None

def add_user(name,password):
	c = connection()
	if (c != None):
		channel = c.invoke_shell()
		channel.send('sudo adduser '+ str(name) +'\n')
		channel.send('sudo passwd ' + str(name) +'\n')
		time.sleep(3)
		channel.send(str(password)+'\n')
		time.sleep(3)
		channel.send(str(password)+'\n')
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
	    elif sys.argv[1] == "--help":
			print ("Commandline arguments:")
			print ("		  	--add : to add users")
			print ("		  	--rm : to remove users")
	else:
	    print "Invalid command. Type " + sys.argv[0] + " --help for additional information"

if __name__ == '__main__':
  main()
