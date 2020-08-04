
#!/usr/bin/env python

##file here for py2exe

import re, sys, time, optparse, fileinput, subprocess

__version__ = "v0.0.1a"

USAGE = "%prog [options]"
VERSION = "%prog v" + __version__

AGENT = "%s / %s - Built By DrwDigital" % ("AVH", __version__)

def parse_options():

    parser = optparse.OptionParser(usage=USAGE, version=VERSION)

    parser.add_option("-u", "--url",
            action="store", default="null", dest="url",
            help="URL of your site")

    opts, args = parser.parse_args()
    return opts, args


def avh(opts):
    if(opts.url != 'null'):
        site_url = opts.url

        run("sudo mkdir -p /var/www/%s/public_html" % site_url)
        run("sudo chown -R $USER:$USER /var/www/%s/public_html " % site_url)
        run("sudo chmod -R 755 /var/www")
        run("sudo mkdir -p /var/www/%s/public_html" % site_url)
        
        f = open("/var/www/%s/public_html/index.html" % (site_url), "w")
        f.write("Server block for %s is now working" % (site_url))
        f.close()

        file_contents = """
            <VirtualHost *:80>
                ServerName %s
                ServerAlias www.%s
                ServerAdmin webmaster@%s
                DocumentRoot /var/www/%s/public_html

                <Directory /var/www/%s/public_html>
                    Options -Indexes +FollowSymLinks
                    AllowOverride All
                </Directory>

                ErrorLog ${APACHE_LOG_DIR}/%s-error.log
                CustomLog ${APACHE_LOG_DIR}/%s-access.log combined
            </VirtualHost>
        """ % site_url

        f = open("/etc/apache2/sites-available/%s.conf" % (site_url), "w")
        f.write(file_contents)
        f.close()

        run("sudo a2ensite %s" % site_url)
        run("sudo service apache2 restart")

    # subprocess.call("git checkout -b '%s'" % opts.branch, shell=True)

def run(command):
    print command

def init():
    # print AGENT
    opts, args = parse_options()
    avh(opts)

init()
