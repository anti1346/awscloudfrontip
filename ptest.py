#!/usr/bin/env python
import os
import requests
import ipaddress

ip_ranges = requests.get('https://ip-ranges.amazonaws.com/ip-ranges.json').json()['prefixes']
cloudfront_ips = [item['ip_prefix'] for item in ip_ranges if (item["service"] == "CLOUDFRONT" and item["region"] == "ap-northeast-2")]

### 클라우드프론트 아이피 대역대
cloudfront_ipaddress=[]
for ip in cloudfront_ips:
    cloudfront_ipaddress.append(ip)

### 클라우드프론트 아이피 리스트를 리스트(list)에 저장
cloudfrontlist=[]
for ip in cloudfront_ipaddress:
    net4 = ipaddress.ip_network(str(ip))
    print(net4.hosts)
    for x in net4.hosts():
        cloudfrontlist.append(format(ipaddress.IPv4Address(x)))
# print(cloudfrontlist)

### iplist.txt 파일을 읽어 리스트(list)에 저장
iplist=[]
with open('iplist.txt', 'r') as filehandle:
    for line in filehandle:
        curr_place = line[:-1]
        iplist.append(curr_place)
# print(iplist)

### iplist.txt의 아이피 리스트와 클라우드프론트 아이피 리스트 비교
for a in iplist:
    for b in cloudfrontlist:
        if a == b:
            print(a)

os.system('copy zonefile sangchul.kr.zone')

dnszonefile = open('sangchul.kr.zone', 'a')
for a in iplist:
    for b in cloudfrontlist:
        if a == b:
            # print(a)
            recode = ('sangchul.kr.\t\t\tIN\tA\t%s\n' %a)
            dnszonefile.write(recode)
dnszonefile.close()

# file1 = open('iplist.txt', 'r')
# Lines = file1.readlines()
# count = 0
# for line in Lines:
#     count += 1
#     print(line)



# for ip in cloudfront_ipaddress:
#     net4 = ipaddress.ip_network(str(ip))
#     for x in net4.hosts():
#         count = 0
#         for line in Lines:
#             count += 1
#             if [line == x]:
#                 print(line)
        
# cloudfrontip = os.system("cat cloudfrontiplist.txt")
# dnsip = os.system("cat iplist.txt")



# f = open("cloudfrontiplist.txt", 'r')
# line = f.readline()
# print(line)
# for ip in line:
#     if ip == dnsip:
#         print("==")
#         print(ip)