#!/usr/bin/env python3

"""
rename proxmox qemu vms, in case:
 - they are located on in default locations (/var/lib/vz/images/...)
 - contain only a single disk
 - which is a qcow2 image
"""

import os
import sys



def usage(pve_path,vz_path):
	print()
	print("usage:")
	print("    ./" + os.path.basename(__file__) + " OLD_VM_ID DESIRED_VM_ID")
	print()
	print("    ./" + os.path.basename(__file__) + " 100 101")
	print()
	print("    this is only intended to be used with VMs, not LXC.")
	print("    will rename config filename, contents and fix image path and filename.")
	print()
	print("    predefined paths:")
	print("    config location: " + pve_path)
	print("    images location: " + vz_path) 
	sys.exit(0)

def check_if_config_exists(fname):
	if not os.path.isfile(fname):
		assert False,"Config missing"

def check_if_image_exists(fname):
	if not os.path.isfile(fname):
		assert False,"Image missing"

def get_config_absolute_filename(path, vmid):
	return path + "/" + vmid + ".conf"

def get_image_filename(vmid):
	return "vm-" + vmid + "-disk-0.qcow2"

def rename_config_contents_and_filename(oldid, newid, oldfilepath, newfilepath):
	searchstring = oldid + "/vm-" + oldid
	replacestring = newid + "/vm-" + newid
	old = open(oldfilepath, 'r')
	new = open(newfilepath, 'w')
	
	for i in old:
		new.write(i.replace(searchstring, replacestring))

	old.close
	new.close
	os.remove(oldfilepath)

def rename_image_and_its_path(oldid, newid, imagepath, oldfile, newfile):
	os.chdir(imagepath)
	os.rename(oldid,newid)
	os.chdir(newid)
	os.rename(oldfile, newfile)


def main():
	pve_config_path = "/etc/pve/qemu-server"
	vz_image_path = "/var/lib/vz/images"
	old_id = ""
	old_config = ""
	old_image = ""
	new_id = ""
	new_config = ""
	new_image = ""

	if not len(sys.argv) == 3:
		usage(pve_config_path, vz_image_path)
	else:
		old_id = sys.argv[1]
		new_id = sys.argv[2]

	old_config = get_config_absolute_filename(pve_config_path,old_id)
	new_config = get_config_absolute_filename(pve_config_path,new_id)
	old_image = get_image_filename(old_id)
	new_image = get_image_filename(new_id)

	check_if_config_exists(old_config)
	check_if_image_exists(vz_image_path + "/" + old_id + "/" + old_image)

	rename_config_contents_and_filename(old_id, new_id, old_config, new_config)
	rename_image_and_its_path(old_id, new_id, vz_image_path, old_image, new_image)

main()
