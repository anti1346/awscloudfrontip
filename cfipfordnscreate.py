#!/usr/bin/env python
import os, sys
import requests
import ipaddress
from pathlib import Path
import filecmp

ip_ranges = requests.get('https://ip-ranges.amazonaws.com/ip-ranges.json').json()['prefixes']
cloudfront_ips = [item['ip_prefix'] for item in ip_ranges if (item["service"] == "CLOUDFRONT" and item["region"] == "ap-northeast-2")]

### 클라우드프론트 서브넷
cloudfront_seoul_subnet=[]
for ip in cloudfront_ips:
    cloudfront_seoul_subnet.append(ip)

### 클라우드프론트 아이피 리스트를 리스트(list)에 저장
cloudfrontiplist=[]
for ip in cloudfront_seoul_subnet:
    net4 = ipaddress.ip_network(str(ip))
    print(net4.hosts)
    for x in net4.hosts():
        cloudfrontiplist.append(format(ipaddress.IPv4Address(x)))
# print(cloudfrontiplist)

### iplist.txt 파일을 읽어 리스트(list)에 저장
iplist=[]
with open('iplist.txt', 'r') as filehandle:
    for line in filehandle:
        curr_place = line[:-1]
        iplist.append(curr_place)
# print(iplist)

### iplist.txt의 아이피 리스트와 클라우드프론트 아이피 리스트 비교
for a in iplist:
    for b in cloudfrontiplist:
        if a == b:
            print(a)

### zonefile 템플릿 및 백업
dnszonefile = 'sangchul.kr.zone'
path = Path(dnszonefile)
if path.is_file():
    print(f'The file {dnszonefile} exists')
    os.system('copy sangchul.kr.zone sangchul.kr.zone.bk')
else:
    print(f'The file {dnszonefile} does not exist')
    os.system('copy zonefile sangchul.kr.zone')

# os.system('copy sangchul.kr.zone sangchul.kr.zone.bk')


### sangchul.kr zonefile 생성
os.system('copy zonefile sangchul.kr.zone')
dnszonefile = open('sangchul.kr.zone', 'a')
for a in iplist:
    for b in cloudfrontiplist:
        if a == b:
            # print(a)
            recode = ('sangchul.kr.\t\t\tIN\tA\t%s\n' %a)
            dnszonefile.write(recode)
dnszonefile.close()

### zonefile 비교, 원복
file1 = "sangchul.kr.zone"
file2 = "sangchul.kr.zone.bk"
def compare_files(file1,file2):
    compare = filecmp.cmp(file1,file2)
    if compare == True:
        print("The files are the same.")
    else:
        print("The files are different.")
compare_files(file1,file2)