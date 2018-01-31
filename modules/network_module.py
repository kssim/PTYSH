import dbus
from pyroute2 import IPRoute
from pyroute2 import IPDB

from module import PtyshModule

class network_module(PtyshModule):

    def __init__(self):
        super(network_module, self).__init__()
        super(network_module, self).init_node("network", "network node")
        super(network_module, self).add_command("show link name all", "show link name all", self.cmd_show_link_all)
        super(network_module, self).add_command("show link status", "show link name all", self.cmd_show_link_status, "show link status [link name]")
        self.iproute = IPRoute()

    def print_format(self, key, value):
        return ("%s : %s" % (key.ljust(25), value))


    ##### cmd function. #####
    def cmd_show_link_all(self):
        print ("=" * 20)
        for link in self.iproute.get_links():
            print (link.get_attr("IFLA_IFNAME"))
        print ("=" * 20)


    def cmd_show_link_status(self, args):
        index = self.iproute.link_lookup(ifname=args[0])
        if len(index) == 0:
            print ("No interface")
            return

        link = self.iproute.get_links(index)[0]
        print ("=" * 50)
        print (self.print_format("Index", link["index"]))
        print (self.print_format("Name", link.get_attr("IFLA_IFNAME")))
        print (self.print_format("Mac address", link.get_attr("IFLA_ADDRESS")))
        print (self.print_format("Broadcast", link.get_attr("IFLA_BROADCAST")))
        print (self.print_format("MTU", link.get_attr("IFLA_MTU")))
        print (self.print_format("Status", link.get_attr("IFLA_OPERSTATE")))
        print (self.print_format("Promiscuity", link.get_attr("IFLA_PROMISCUITY")))

        stats = link.get_attr("IFLA_STATS64")
        print (self.print_format("multicast", stats["multicast"]))
        print (self.print_format("collisions", stats["collisions"]))

        for ip in self.iproute.get_addr(index=index[0]):
            print ("%s IP %s" % ("-" * 23, "-" *23))
            print (self.print_format("- IP", ip.get_attr("IFA_ADDRESS")))
            print (self.print_format("- Broadcast IP", ip.get_attr("IFA_BROADCAST")))
            print (self.print_format("- Subnet", ip["prefixlen"]))
            print ("-" * 50)

        print ("%s RX %s" % ("-" * 23, "-" *23))
        print (self.print_format("- rx_packets", stats["rx_packets"]))
        print (self.print_format("- rx_bytes", stats["rx_bytes"]))
        print (self.print_format("- rx_dropped", stats["rx_dropped"]))
        print (self.print_format("- rx_errors", stats["rx_errors"]))
        print (self.print_format("- rx_compressed", stats["rx_compressed"]))
        print (self.print_format("- rx_over_errors", stats["rx_over_errors"]))
        print (self.print_format("- rx_crc_errors", stats["rx_crc_errors"]))
        print (self.print_format("- rx_length_errors", stats["rx_length_errors"]))
        print (self.print_format("- rx_fifo_errors", stats["rx_fifo_errors"]))
        print (self.print_format("- rx_missed_errors", stats["rx_missed_errors"]))
        print (self.print_format("- rx_frame_errors", stats["rx_frame_errors"]))
        print ("-" * 50)

        print ("%s TX %s" % ("-" * 23, "-" *23))
        print (self.print_format("- tx_packets", stats["tx_packets"]))
        print (self.print_format("- tx_bytes", stats["tx_bytes"]))
        print (self.print_format("- tx_dropped", stats["tx_dropped"]))
        print (self.print_format("- tx_errors", stats["tx_errors"]))
        print (self.print_format("- tx_compressed", stats["tx_compressed"]))
        print (self.print_format("- tx_heartbeat_errors", stats["tx_heartbeat_errors"]))
        print (self.print_format("- tx_aborted_errors", stats["tx_aborted_errors"]))
        print (self.print_format("- tx_window_errors", stats["tx_window_errors"]))
        print (self.print_format("- tx_fifo_errors", stats["tx_fifo_errors"]))
        print (self.print_format("- tx_carrier_errors", stats["tx_carrier_errors"]))
        print ("-" * 50)

        print ("=" * 50)
