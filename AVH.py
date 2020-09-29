
#!/usr/bin/env python

##file here for py2exe

import re, sys, time, optparse, fileinput, subprocess

__version__ = "v0.0.2a"

USAGE = "%prog [options]"
VERSION = "%prog v" + __version__

AGENT = "%s / %s - Built By Jake Drew" % ("AVH", __version__)

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
        
        f = open("/var/www/%s/public_html/index.html" % (site_url), "w+")
        f.write("Server block for %s is now working" % (site_url))
        f.close()

        file_contents = "<VirtualHost *:80>\n\tServerName %s\n\tServerAlias www.%s\n\tServerAdmin webmaster@%s\n\tDocumentRoot /var/www/%s/public_html\n\n\n\t<Directory /var/www/%s/public_html>\n\t\tOptions -Indexes +FollowSymLinks\n\t\tAllowOverride All\n\t</Directory>\n\n\n\tErrorLog ${APACHE_LOG_DIR}/%s-error.log\n\tCustomLog ${APACHE_LOG_DIR}/%s-access.log combined\n</VirtualHost>\n" % (site_url,site_url,site_url,site_url,site_url,site_url,site_url)

        f = open("/etc/apache2/sites-available/%s.conf" % (site_url), "w+")
        f.write(file_contents)
        f.close()

        run("sudo a2ensite %s" % site_url)
        run("sudo systemctl reload apache2")

def run(command):
    # print command
    subprocess.call(command, shell=True)

def init():
    # print AGENT
    opts, args = parse_options()
    avh(opts)

init()
