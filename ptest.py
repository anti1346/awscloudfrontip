#!/usr/bin/env python
import os
import requests
import ipaddress

ip_ranges = requests.get('https://ip-ranges.amazonaws.com/ip-ranges.json').json()['prefixes']
cloudfront_ips = [item['ip_prefix'] for item in ip_ranges if (item["service"] == "CLOUDFRONT" and item["region"] == "ap-northeast-2")]

cloudfront_ipaddress=[]

for ip in cloudfront_ips:
    cloudfront_ipaddress.append(ip)

sourceFile = open('cloudfrontiplist.txt', 'w')
for ip in cloudfront_ipaddress:
    net4 = ipaddress.ip_network(str(ip))
    for x in net4.hosts():
        print(x, file = sourceFile)
sourceFile.close()

cloudfrontip = os.system("cat cloudfrontiplist.txt")
dnsip = os.system("cat iplist.txt")

# f = open("cloudfrontiplist.txt", 'r')
# line = f.readline()
# print(line)
# for ip in line:
#     if ip == dnsip:
#         print("==")
#         print(ip)