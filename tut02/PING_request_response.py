from scapy.all import sr1, srp, send, wrpcap, IP, ICMP
from random import randint

DST_URL = "zomato.com" #site given in spreadsheet was not working, so this is used

SRC_PORT = randint(1024, 65535)
HTTPS_PORT = 443


def getPing():
    packet = IP(dst=DST_URL) / ICMP()
    response = sr1(packet, timeout=1)
    return [packet, response]


wrpcap("PING_2001CS62.pcap", getPing())
