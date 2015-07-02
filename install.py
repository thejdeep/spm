import sys
import os
import subprocess
from collections import OrderedDict
import xmlrpclib
import hawkey
import shutil
from pprint import pprint
import librepo

op_name=sys.argv[1]
if sys.argv[1] != "list":
	pkg_name = sys.argv[2]

# Librepo Configurations
MAIN_REPO = "/home/thejdeep/test_repo/"
DESTDIR = "/home/thejdeep/test_repo/repodata/"
PROGRESSBAR_LEN = 40
finished = False

# Hawkey Configurations
sack = hawkey.Sack()
path = "/home/thejdeep/test_repo/repodata/%s"
repo = hawkey.Repo("test")
repo.repomd_fn = path % "repomd.xml"
repo.primary_fn = path % "b6f6911f7d9fb63f001388f1ecd0766cec060c1d04c703c6a74969eadc24ec97-primary.xml.gz"
repo.filelists_fn = path % "df5897ed6d3f87f2be4432543edf2f58996e5c9e6a7acee054f9dbfe513df4da-filelists.xml.gz"
sack.load_repo(repo,load_filelists=True)
#sack.load_system_repo()

# Functions start

def callback(data, total_to_download, downloaded):
    """Progress callback"""
    global finished

    if total_to_download != downloaded:
        finished = False

    if total_to_download <= 0 or finished == True:
        return

    completed = int(downloaded / (total_to_download / PROGRESSBAR_LEN))
    print "%30s: [%s%s] %8s/%8s\r" % (data, '#'*completed, '-'*(PROGRESSBAR_LEN-completed), int(downloaded), int(total_to_download)),
    sys.stdout.flush()

    if total_to_download == downloaded and not finished:
        print
        finished = True
        return

# Main Function
if __name__ == "__main__":
	if op_name=="install":
		print "Querying the repository"
		print "-----------------------"
		print "Found packages :"
		print "--------------"
		q = hawkey.Query(sack)
		q = q.filter(name=pkg_name,latest_per_arch=True)[0]
		
		# TODO - CHANGE THIS
		ind = str(q).index(":")
		l = list(str(q))
		l[ind-1:ind+1]=[]
		s = "".join(l)
		pkg_url = s+".rpm"
		if q:
			print q
		else:
			print "No packages with name "+pkg_name+" found. Exiting"
			sys.exit()
	
		# TODO - FIX DEPENDENCY CHECK
		print "---------------------------"
		print "Performing Dependency Check"
		print "---------------------------"
	
		'''g = hawkey.Goal(sack)
		sltr = hawkey.Selector(sack).set(name=pkg_name)
		g.install(select=sltr)
		temp = g.run()
		#print temp
		if temp :
		#if(not temp)
		#	print "Failed to compute dependencies.Exiting"
		#	sys.exit()
			print "The following packages need to be changed :"
			print "To Install :"
			for p in map(str, g.list_installs()):
				print p
			print "To Upgrade :"
			for p in map(str, g.list_upgrades()):
				print p
			print "To Erase :"
			for p in map(str, g.list_erasures()):
				print p 
		else :
		print "Could not compute dependency check. Exiting"
		print ""
		sys.exit(0)'''
	
		print "DOWNLOADING PACKAGES ......"
	
		h = librepo.Handle()
    		h.setopt(librepo.LRO_URLS, ["/home/thejdeep/test_repo/"])
    		h.setopt(librepo.LRO_REPOTYPE, librepo.LR_YUMREPO)
    		h.setopt(librepo.LRO_PROGRESSCB, callback)
    		h.setopt(librepo.LRO_PROGRESSDATA, "")
	
		# TODO - ADD SUPPORT FOR MULTIPLE PACKAGES. DUH !
		h.progressdata = pkg_name
        	h.download(pkg_url)
		print "Finished Downloading Packages"
		print "Installing packages"
		print "-------------------"
		cmd_ins = "sudo rpm -ivh " + pkg_url
		subprocess.call(cmd_ins,shell=True)
		print "Finished Installing"
		print "Performing Cleanup"
		cmd_rm = "sudo rm "+pkg_url
		subprocess.call(cmd_rm,shell=True)
		print "DONE ...."
	if op_name=="remove":
		print "Checking if package is installed"
		cmd_check = "rpm -q "+pkg_name
		try:
			out_str = subprocess.check_output(cmd_check,shell=True)
			print out_str
			print "Package found. Removing..."
			cmd_rmv = "sudo rpm -e "+pkg_name
			subprocess.call(cmd_rmv,shell=True)
			print "DONE...."
		except subprocess.CalledProcessError, e:
    			print "Package "+pkg_name+" not installed"
			print "Exiting..."
			sys.exit()
	if op_name=="check":
		print "Checking if package is installed"
		cmd_check = "rpm -q "+pkg_name
		try:
			out_str = subprocess.check_output(cmd_check,shell=True)
			print out_str
		except subprocess.CalledProcessError, e:
			print "Package "+pkg_name+" not installed"
	if op_name=="list":
		print "Listing all installed packages"
		cmd_list = "rpm -qa"
		subprocess.call(cmd_list,shell=True)
	
	
