from scapy.all import sr1, srp, send, wrpcap, IP, UDP, DNS, DNSQR
from random import randint

DNS_IP = "8.8.8.8"
DNS_PORT = 53

QUERY_SITE = "zomato.com" #site mentioned in spreadsheet was not working, therefore this is used


def getDNS():
    dns_query = (
        IP(dst=DNS_IP) / UDP(dport=DNS_PORT) / DNS(rd=1, qd=DNSQR(qname=QUERY_SITE))
    )
    dns_response = sr1(dns_query)

    return [dns_query, dns_response]


wrpcap("DNS_2001CS62.pcap", getDNS())
