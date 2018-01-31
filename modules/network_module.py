import dbus
from pyroute2 import IPRoute
from pyroute2 import IPDB

from module import PtyshModule

class network_module(PtyshModule):

    def __init__(self):
        super(network_module, self).__init__()
        super(network_module, self).init_node("network", "network node")
        super(network_module, self).add_command("show link", "show link [link name]", self.cmd_show_link, "show link [link name]")
        super(network_module, self).add_command("show link names", "show link names", self.cmd_show_link, "show link name")
        super(network_module, self).add_command("show link all", "show link all", self.cmd_show_link, "show link all")
        super(network_module, self).add_command("show route", "show route", self.cmd_show_route, "show route")

        self.iproute = IPRoute()

    def print_output_boarder(self, inner):
        print ("=" * 60) if inner else print ("-" * 60)

    def print_key_value(self, key, value):
        print ("%s : %s" % (key.ljust(25), value))

    def print_route_table(self, index, dest, gateway, mask, interface):
        print ("%s%s%s%s%s" % (index.ljust(8), dest.ljust(17), gateway.ljust(17), mask.ljust(8), interface))



    ##### cmd function. #####
    def cmd_show_link(self, *args):
        if len(args) != 1:
            return False

        if args[0][0] == "names":
            self.cmd_show_link_names()
        elif args[0][0] == "all":
            for link in self.iproute.get_links():
                self.cmd_show_link_info(link.get_attr("IFLA_IFNAME"))
        else:
            self.cmd_show_link_info(args[0][0])

    def cmd_show_link_names(self):
        print ("=" * 20)
        for link in self.iproute.get_links():
            print (link.get_attr("IFLA_IFNAME"))
        print ("=" * 20)

    def cmd_show_link_info(self, link_name):
        index = self.iproute.link_lookup(ifname=link_name)
        if len(index) == 0:
            print ("No interface")
            return

        link = self.iproute.get_links(index)[0]
        self.print_output_boarder(True)
        self.print_key_value("Index", link["index"])
        self.print_key_value("Name", link.get_attr("IFLA_IFNAME"))
        self.print_key_value("Mac address", link.get_attr("IFLA_ADDRESS"))
        self.print_key_value("Broadcast", link.get_attr("IFLA_BROADCAST"))
        self.print_key_value("MTU", link.get_attr("IFLA_MTU"))
        self.print_key_value("Status", link.get_attr("IFLA_OPERSTATE"))
        self.print_key_value("Promiscuity", link.get_attr("IFLA_PROMISCUITY"))

        stats = link.get_attr("IFLA_STATS64")
        self.print_key_value("multicast", stats["multicast"])
        self.print_key_value("collisions", stats["collisions"])

        for ip in self.iproute.get_addr(index=index[0]):
            print ("%s IP %s" % ("-" * 23, "-" *23))
            self.print_key_value("- IP", ip.get_attr("IFA_ADDRESS"))
            self.print_key_value("- Broadcast IP", ip.get_attr("IFA_BROADCAST"))
            self.print_key_value("- Subnet", ip["prefixlen"])
            self.print_output_boarder(False)

        print ("%s RX %s" % ("-" * 23, "-" *23))
        self.print_key_value("- rx_packets", stats["rx_packets"])
        self.print_key_value("- rx_bytes", stats["rx_bytes"])
        self.print_key_value("- rx_dropped", stats["rx_dropped"])
        self.print_key_value("- rx_errors", stats["rx_errors"])
        self.print_key_value("- rx_compressed", stats["rx_compressed"])
        self.print_key_value("- rx_over_errors", stats["rx_over_errors"])
        self.print_key_value("- rx_crc_errors", stats["rx_crc_errors"])
        self.print_key_value("- rx_length_errors", stats["rx_length_errors"])
        self.print_key_value("- rx_fifo_errors", stats["rx_fifo_errors"])
        self.print_key_value("- rx_missed_errors", stats["rx_missed_errors"])
        self.print_key_value("- rx_frame_errors", stats["rx_frame_errors"])
        self.print_output_boarder(False)

        print ("%s TX %s" % ("-" * 23, "-" *23))
        self.print_key_value("- tx_packets", stats["tx_packets"])
        self.print_key_value("- tx_bytes", stats["tx_bytes"])
        self.print_key_value("- tx_dropped", stats["tx_dropped"])
        self.print_key_value("- tx_errors", stats["tx_errors"])
        self.print_key_value("- tx_compressed", stats["tx_compressed"])
        self.print_key_value("- tx_heartbeat_errors", stats["tx_heartbeat_errors"])
        self.print_key_value("- tx_aborted_errors", stats["tx_aborted_errors"])
        self.print_key_value("- tx_window_errors", stats["tx_window_errors"])
        self.print_key_value("- tx_fifo_errors", stats["tx_fifo_errors"])
        self.print_key_value("- tx_carrier_errors", stats["tx_carrier_errors"])
        self.print_output_boarder(False)

        self.print_output_boarder(True)

    def cmd_show_route(self):
        self.print_output_boarder(True)
        self.print_route_table("Index", "Destination", "Gateway", "Mask", "Interface")
        self.print_output_boarder(False)

        for index, route in enumerate(self.iproute.get_routes(table=254)):
            if route.get_attr("RTA_DST", None) is None and route["dst_len"] == 0:
                destination = "default"
                gateway = route.get_attrs("RTA_GATEWAY")[0]
            else:
                destination = route.get_attrs("RTA_DST")[0]
                gateway = "0.0.0.0"

            interface_index = route.get_attrs("RTA_OIF")[0]
            interface = self.iproute.get_links(interface_index)[0].get_attrs("IFLA_IFNAME")[0]
            self.print_route_table(str(index), destination, gateway, str(route["dst_len"]), interface)
        self.print_output_boarder(True)
