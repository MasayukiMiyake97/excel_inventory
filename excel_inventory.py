#!/usr/bin/python3.6
# -*- coding:utf-8 -*-
# This module reads the CSV file and converts it into inventory information.
#
# Copyright (C) 2018 Masayuki Miyake
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http:#www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

"""
This module reads the Excel file and converts it into inventory information.
"""

import csv
import yaml
import json
import sys
import copy
import openpyxl as px

def load_excel_inventory(file_name):
    """
    Read inventory file in Excel format.

    :param string file_name: Excel file name
    :rtype: dict
    :return: inventory information dict.
    """ 

    # load excel
    ret = {}

    workbook = px.load_workbook(file_name, data_only=True)
    sheet_names = workbook.sheetnames

    for sheet_name in sheet_names:
        ret[sheet_name] = load_sheet(workbook, sheet_name)

    return ret


def load_sheet(workbook, sheet_name):
    """
    Read sheet information.

    :param Book workbook: Excel book object.
    :param string sheet_name: target sheet name.
    :rtype: array
    :return: Array of sheet information.
    """ 

    ret = []
    header_list = []
    # select sheet
    sheet = workbook[sheet_name]

    # read row
    for row in sheet:
        row_data = {}
        cell_num = 0

        # read cell
        for cell in row:
            # get cell position
            row_pos = cell.row - 1
            col_pos = cell.col_idx - 1

            # get cell value
            if row_pos == 0:
                # header row read
                header_list.append(cell.value)
            else:
                # data row read
                if cell.value is not None:
                    row_data[header_list[col_pos]] = cell.value
                    cell_num += 1

        # set row values
        if row_data is not None and cell_num > 0:
            ret.append(row_data)

    return ret


def make_group_hostnames(inv_dataset):
    """
    Generate a list of host names belonging to the group.

    :param dict inv_dataset: inventory data set.
    :rtype: dict
    :return: Host name list information belonging to the group.
    """ 
    ret = {}

    for key, host_info_list in inv_dataset.items():
        key_hostname_list = []

        for host_info in host_info_list:
            host_name = host_info.get('host_name', None)
            group_name = host_info.get('group', None)

            if host_name is None or group_name is None:
                raise ValueError('unknown host_name or group_name '\
                                 'sheet=%s host_name=%s group_name=%s'
                                 % (key, host_name, group_name))

            key_hostname_list.append(host_name)

            group_hostname_list = ret.get(group_name, [])
            ret[group_name] = group_hostname_list
            group_hostname_list.append(host_name)

        if key != 'hosts':
            ret[key] = key_hostname_list

    return ret


def make_hostvars(inv_dataset):
    """
    Generate definition information for each host.

    :param dict inv_dataset: inventory data set.
    :rtype: dict
    :return: Definition information for each host.
    """ 

    ret = {}

    dataset = copy.deepcopy(inv_dataset)

    host_info_list = dataset.pop('hosts', None)
    if host_info_list is None:
        raise ValueError('unknown hosts sheet')

    # make hostvars
    for host_info in host_info_list:
        host_name = host_info.pop('host_name', None)
        group_name = host_info.pop('group', None)

        ret[host_name] = host_info

    # append host value
    for key, host_info_list in dataset.items():

        for host_info in host_info_list:
            host_name = host_info.pop('host_name', None)
            group_name = host_info.pop('group', None)

            hostvar = ret.get(host_name, None)
            if hostvar is None:
                raise ValueError('unknown host_name=%s' % host_name)

            hostvar.update(host_info)

    return ret


def load_common_info(file_name):
    """
    Read node information line.
    Returns an dict of node information.
    node information format => {item_name1: value1, item_name2: value2, ...}
    ex. {"host_name": "web001", "port_no": 80, ... }

    :param string file_name: Name of common definition file in yaml format.
    :rtype: dict
    :return: Dict of common information.
    """ 

    ret = None
    with open(file_name, 'r') as common_file:
        ret = yaml.load(common_file)

    return ret


def make_groupvars(common_info):
    """
    Extract groupvars from group information defined in common information.

    :param dict common_info: common information dictionary.
    :rtype: dict
    :return: groupvars dictionary.
    """ 

    ret = {}
    # get group_vars
    group_vars = common_info.get('group_vars', None)
    if group_vars is not None: 
        for name, val in group_vars.items():
            ret[name] = val
    # get all vars
    all_vars = common_info.get('all_vars', None)
    if all_vars is not None: 
        ret['all'] = all_vars

    return ret


def make_group_tree(groupvars, group_hostnames):

    ret = {}

    # add all group
    ret['all'] = {}

    for group_name, value in groupvars.items():
        ret[group_name] = {}

    for group_name, value in group_hostnames.items():
        ret[group_name] = {}

    return ret


def make_inventory(group_tree, groupvars, group_hostnames, hostvars):

    ret = {}

    # add groups
    for key, value in group_tree.items():
        ret[key] = value

    # add group vars
    for key, value in groupvars.items():
        group = ret.get(key, {})
        group['vars'] = value
        ret[key] = group

    # add hosts
    for key, value in group_hostnames.items():
        group = ret.get(key, {})
        group['hosts'] = value
        ret[key] = group

    # add hostvars
    ret['_meta'] = {'hostvars': hostvars}        

    return ret


def customize_process(group_tree, groupvars, group_hostnames, hostvars, specific_vars):
    """
    With this function, customize inventory data.

    :param dict group_tree: group tree information.
    :param dict groupvars: groupvars dictionary.
    :param dict group_hostnames: Host name list information belonging to the group.
    :param dict hostvars: Definition information for each host.
    :param dict specific_vars: specific values dictionary.
    """ 


def main():
    """
    main function.

    """ 
    # load common information file
    common_info = load_common_info('common_val.yml')

    # load inventory file
    inv_file = common_info.pop('inventory_file', 'inventory.xlsx')
    inv_dataset = load_excel_inventory(inv_file)

    groupvars = make_groupvars(common_info)

    group_hostnames = make_group_hostnames(inv_dataset)

    hostvars = make_hostvars(inv_dataset)

    group_tree = make_group_tree(groupvars, group_hostnames)

    specific_vars = common_info.pop('specific_vars', {})
    # call customize_process
    customize_process(group_tree, groupvars, group_hostnames, hostvars, specific_vars)

    inventory_data = make_inventory(group_tree, groupvars, group_hostnames, hostvars)

    # dump JSON format
    json.dump(inventory_data, sys.stdout)

 
if __name__ == '__main__':

    main()

