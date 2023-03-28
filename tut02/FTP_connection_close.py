from scapy.all import *
from random import randint

DNS_IP = "8.8.8.8"
DNS_PORT = 53

QUERY_SITE = "zomato.com" #site given in spreadsheet is not working, so this is used


def getFTPclose():
    ftp_pkt = IP(dst='195.144.107.198')/TCP(sport=20, dport=21, flags="S")
    ftp_res = sr1(ftp_pkt)
    ftp_close = IP(dst='195.144.107.198')/TCP(sport=20, dport=21, seq=ftp_res.ack,
    ack=ftp_res.seq+1, flags="PA")

    return [ftp_close]

wrpcap("FTP_connection_close_2001CS62.pcap", getFTPclose())
