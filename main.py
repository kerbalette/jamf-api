import os
import sys
import argparse

from base import Base
from connectors.jamf import Jamf


class MainProg(Base):
    
    def run(self, attribute: str = "", value: str = "" ):

        jamf = Jamf()
        
        # TODO Framework for attribute searches
        if (attribute=="serial"):
            host = jamf.get_computer_by_serial(value)
            print("Computer: \t\t\t{0}".format(host["computer"]["general"]["name"]))
            print("Mac Address: \t\t\t{0}".format(host["computer"]["general"]["mac_address"]))
            print("IP Address: \t\t\t{0}".format(host["computer"]["general"]["ip_address"]))
            print("Last Known IP Address: \t\t{0}".format(host['computer']['general']['last_reported_ip']))
            print("Last Contact Time: \t\t{0}".format(host['computer']['general']['last_contact_time']))
            print("Model: \t\t\t\t{0}".format(host['computer']['hardware']['model']))
            print("OS: \t\t\t\t{0}".format(host['computer']['hardware']['os_name']))
            print("OS Version: \t\t\t{0}".format(host['computer']['hardware']['os_version']))
            print("User: \t\t\t\t{0}".format(host['computer']['location']['realname']))
            print("Email Address: \t\t\t{0}".format(host['computer']['location']['email_address']))
            print("Position: \t\t\t{0}".format(host['computer']['location']['position']))
        
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='JAMF Pro Query Tool')
    parser.add_argument('--query', help='Enter attribute you would like to search for', required=True)
    parser.add_argument('--value', help='Enter the value of the attribute to hunt for', required=True)
    parser.add_argument('--proxyhost', help='Proxy Server',required=False)
    parser.add_argument('--proxyport', help='Proxy Port', required=False, default="8080")
    args = parser.parse_args()

    if (args.proxyhost):
        proxies = {'http':'http://%s:%s' %(args.proxyhost, args.proxyport), 'https':'https://%s:%s' %(args.proxyhost, args.proxyport)}
    else:
        proxies = {}

    mainprog = MainProg()
    mainprog.run(args.query, args.value)
