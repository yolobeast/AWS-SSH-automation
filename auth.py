############################################################
#Name : Sathi.Ranganathan
#Porject : SSH autnentication manager
#date : Feburay,18.2018
############################################################
#!/usr/bin/python
import paramiko
import boto3
import time
import os
import sys
import getpass

#The function is used to connect the AWS instance
def connection():
	print ("Creating ssh session")
	session = boto3.Session()
	ec2 = session.resource('ec2', region_name='us-east-2a')
	instance = ec2.Instance(id='i-0f1343218c8520018') # instance id

	Connection_to_AWS = paramiko.SSHClient()
	Connection_to_AWS.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try :
		Connection_to_AWS.connect( 'ec2-52-14-60-141.us-east-2.compute.amazonaws.com', username = "ec2-user", password = "yolo_beast_123")
		return Connection_to_AWS
	except Exception:
		print("The Server is unavalible at the moment")
		return None

#This function is used to add the user to the SSH list
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
		print("User "+name+ " has been added to to SSH credintial")
		print("With "+name+"@ec2-52-14-60-141.us-east-2.compute.amazonaws.com")

#This function is used to remove the user from the SSH list
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
	        with open('name_list.txt') as f:
			    for line in f:
			        if name in line:
						check = 0
						break
			        else:
						check = 1
	        f.close()
	        if (check!=0):
			    with open('name_list.txt',"a+") as f:
				    f.write(name+'\n')
		            add_user(name,password)
			    f.close()
	        else:
				print("this user already has the SSH credinatials")
	    elif sys.argv[1] == "--rm":
			name = raw_input("Enter the user name: ")
			with open('name_list.txt') as f:
			    for line in f:
			        if name in line:
			            check = 0
			            break
			        else:
			            check = 1
			f.close()
			if (check==0):
			    remove_user(name)
			else:
			    print("This user does not have an account yet")
	    elif sys.argv[1] == "--help":
			print ("Commandline arguments:")
			print ("		  	--add : to add users")
			print ("		  	--rm : to remove users")
	else:
	    print "Invalid command. Type " + sys.argv[0] + " --help for additional information"

if __name__ == '__main__':
  main()
