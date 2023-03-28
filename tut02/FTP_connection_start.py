from scapy.all import *
from random import randint

DNS_IP = "8.8.8.8"
DNS_PORT = 53

QUERY_SITE = "zomato.com" #file given in spreadsheet is not working, so this is used


def getFTPopen():
    ftp_pkt = IP(dst='195.144.107.198')/TCP(sport=20, dport=21, flags="S")
    ftp_res = sr1(ftp_pkt)

    return [ftp_pkt, ftp_res]

wrpcap("FTP_connection_start_2001CS62.pcap", getFTPopen())
