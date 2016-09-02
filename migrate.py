import os

#Migrate system script version 0.01
#This script will take forever without passwordless public key authentication.

userGroup = "group"
# trailing slashes are important
homeDir = "/home/"
sitesDir = "/var/www/sites/"
mysqlSource = "/var/lib/mysql"
mysqlDest = "/var/lib/"
nginxSource = "/etc/nginx"
nginxDest = "/etc"
systemGroup = "/etc/group"
remoteHost = "occulus" # remote hostname

def randString(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def getUsers():
    # This function will get all the users of a particular group.
    users = []
    f = open(systemGroups,'r')
    for line in f:
        splitted = line.split(':')
        if (splitted[0] == userGroup):
            userline = splitted[3].split(',')
            for user in userline:
                users.append(user.strip('\n'))
    return users

def getSites():
    # This function will get every users site, sites are a symlink
    sites = []
    users = getUsers()
    for user in users:
        directory=os.listdir(homeDir)
        for f in directory: #f is for file
            if (f.endswith(".onion")):
                sites.append(os.readlink(f)) #readlink might be the wrong way
    return sites

def doUsers():
    users = getUsers()
    for user in users:
        os.chdir(homeDir)
        os.system("rsync -av " + remoteHost + ":" + homeDir + user + " .")
        os.chmod(homeDir, 770)

def doSites():
    sites = getSites()
    for site in sites:
        os.chdir(sitesDir)
        os.system("rsync -av " + remoteHost + ":" + site + " .")
        os.chmod(site, 2750)

def doMySQL():
    os.chdir(mysqlDest)
    os.system("rsync -av " + mysqlSource + " .")

def doNginx():
    os.chdir(nginxDest)
    os.system("rsync -av " + nginxSource + " .")

def doPasswd():
    os.chdir("/etc")
    users = getUsers()
    os.system("rsync -av "+ remoteHost + ":/etc/passwd passwd-new")
    n = open("passwd-new", "r") #new users
    o = open("passwd", "w")     #old users
    for line in n:
        for user in users:
            if (line == user):
                o.write(line)

def doShadow():
