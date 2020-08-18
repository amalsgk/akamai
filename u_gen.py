#!/usr/bin/env python3
# This script will not generate the unsuspension command for COBRA/ACS. Since extra checks are required work manually.

__author__ = "Amal S"
__email__ = "amals@akamai.com"

import sys
import subprocess
# noinspection PyUnresolvedReferences
from subprocess import Popen, PIPE
from multiprocessing import Process


class U_generator:
    def __init__(self):
        self.ips = []
        self.ips_C = []
        self.network_ip = []
        self.network_ip_C = []
        self.services_ip = []
        self.services_ip_C = []
        self.regions = []
        self.regions_C = []
        self.reg_networks = []
        self.reg_networks_C = []
        self.reg_service = []
        self.reg_service_C = []
        self.set_ips_def = []
        self.set_ips_non_def = []
        self.set_reg_def = []
        self.set_reg_non_def = []

    # Analyzing the suspendtell output and segregating the data based on REGION/MACHINE and SERVICE_KEY....

    def split_list(self, ticket_id):
        cmd = "suspendtell " + str(ticket_id)
        usage = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
        for row in usage.stdout:
            if "machine" in row:
                if "_default" in row:
                    val = row.split()
                    self.ips.append(val[0])
                    self.network_ip.append(val[-1])
                    self.services_ip.append(val[3])
                if "_default" not in row:
                    val = row.split()
                    self.ips_C.append(val[0])
                    self.network_ip_C.append(val[-1])
                    self.services_ip_C.append(val[3])
            if "region" in row:
                if "_default" in row:
                    val = row.split()
                    self.regions.append(val[0])
                    self.reg_networks.append(val[-1])
                    self.reg_service.append(val[3])
                if "_default" not in row:
                    val = row.split()
                    self.regions_C.append(val[0])
                    self.reg_networks_C.append(val[-1])
                    self.reg_service_C.append(val[3])


def s_gen_default_ip(ticket_id):
    s_gen_d = U_generator()
    s_gen_d.split_list(ticket_id)
    unique_network_ip = sorted(list(set(s_gen_d.network_ip)))
    s_I = 0
    for s_I in range(len(unique_network_ip)):
        s_J = 0
        for s_J in range(len(s_gen_d.network_ip)):
            if str(unique_network_ip[s_I]) == str(s_gen_d.network_ip[s_J]):
                s_gen_d.set_ips_def.append(s_gen_d.ips[s_J])
            s_J += 1
        if len(s_gen_d.set_ips_def) != 0:
            print("suspendtool --network '{}' --ip '{}' --tic '{}' -u ;".format(str(unique_network_ip[s_I]),
                                                                                str(' '.join(s_gen_d.set_ips_def)),
                                                                                str(ticket_id)))
            list.clear(s_gen_d.set_ips_def)
        s_I += 1


def s_gen_C_ip(ticket_id):
    s_gen_ip_C = U_generator()
    s_gen_ip_C.split_list(ticket_id)
    unique_network_ip_C = sorted(list(set(s_gen_ip_C.network_ip_C)))
    unique_services_ip_C = sorted(list(set(s_gen_ip_C.services_ip_C)))

    s_I = 0
    for s_I in range(len(unique_network_ip_C)):
        s_J = 0
        for s_J in range(len(s_gen_ip_C.network_ip_C)):
            if (str(unique_services_ip_C[s_I]) == str(s_gen_ip_C.services_ip_C[s_J])) and (
                    str(unique_network_ip_C[s_I]) == str(s_gen_ip_C.network_ip_C[s_J])):
                s_gen_ip_C.set_ips_non_def.append(s_gen_ip_C.ips_C[s_J])
            s_J += 1
        if len(s_gen_ip_C.set_ips_non_def) != 0:
            print("suspendtool --network '{}' --ip '{}' --service '{}' --tic '{}' -u ;".format(
                str(unique_network_ip_C[s_I]), str(' '.join(s_gen_ip_C.set_ips_non_def)),
                str(unique_services_ip_C[s_I]), str(ticket_id)))
            list.clear(s_gen_ip_C.set_ips_non_def)
        s_I += 1


def s_gen_reg_def(ticket_id):
    s_gen_reg_d = U_generator()
    s_gen_reg_d.split_list(ticket_id)
    unique_network_reg = sorted(list(set(s_gen_reg_d.reg_networks)))
    s_I = 0
    for s_I in range(len(unique_network_reg)):
        s_J = 0
        for s_J in range(len(s_gen_reg_d.reg_networks)):
            if str(unique_network_reg[s_I]) == str(s_gen_reg_d.reg_networks[s_J]):
                s_gen_reg_d.set_reg_def.append(s_gen_reg_d.regions[s_J])
            s_J += 1
        if len(s_gen_reg_d.set_reg_def) != 0:
            print("suspendtool --network '{}' --region '{}' --tic '{}' -u ;".format(str(unique_network_reg[s_I]),
                                                                                    str(' '.join(
                                                                                        s_gen_reg_d.set_reg_def)).replace(
                                                                                        'r', ''),
                                                                                    str(ticket_id)))
            list.clear(s_gen_reg_d.set_reg_def)
        s_I += 1


def s_gen_reg_C(ticket_id):
    s_gen_C_reg = U_generator()
    s_gen_C_reg.split_list(ticket_id)
    unique_network_reg_C = sorted(list(set(s_gen_C_reg.reg_networks_C)))
    unique_services_reg_C = sorted(list(set(s_gen_C_reg.reg_service_C)))
    s_I = 0
    for s_I in range(len(unique_network_reg_C)):
        s_J = 0
        for s_J in range(len(s_gen_C_reg.reg_networks_C)):
            if (str(unique_services_reg_C[s_I]) == str(s_gen_C_reg.reg_service_C[s_J])) and (
                    str(unique_network_reg_C[s_I]) == str(s_gen_C_reg.reg_networks_C[s_J])):
                s_gen_C_reg.set_reg_non_def.append(s_gen_C_reg.regions_C[s_J])
            s_J += 1
        if len(s_gen_C_reg.set_reg_non_def) != 0:
            print("suspendtool --network '{}' --region '{}' --service '{}' --tic '{}' -u ;".format(
                str(unique_network_reg_C[s_I]), str(' '.join(s_gen_C_reg.set_reg_non_def)).replace('r', ''),
                str(unique_services_reg_C[s_I]), str(ticket_id)))
            list.clear(s_gen_C_reg.set_reg_non_def)
        s_I += 1


if __name__ == '__main__':
    ticket_id = sys.argv[1]
    p1 = Process(target=s_gen_default_ip, args=(ticket_id,))
    p1.start()
    p2 = Process(target=s_gen_C_ip, args=(ticket_id,))
    p2.start()
    p3 = Process(target=s_gen_reg_def, args=(ticket_id,))
    p3.start()
    p4 = Process(target=s_gen_reg_C, args=(ticket_id,))
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
