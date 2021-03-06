# $Id: __init__.py,v 1.13 2012/11/27 00:48:17 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 6.2 (SideWinder)
# 
# Copyright (c) 2000 - 2014 The Regents of the University of California.
# All rights reserved.	
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice unmodified and in its entirety, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided 
# with the distribution.
# 
# 3. All advertising and press materials, printed or electronic, mentioning
# features or use of this software must display the following acknowledgement: 
# 
# 	"This product includes software developed by the Rocks(r)
# 	Cluster Group at the San Diego Supercomputer Center at the
# 	University of California, San Diego and its contributors."
# 
# 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
# neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
# the associated name, interested parties should contact Technology 
# Transfer & Intellectual Property Services, University of California, 
# San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
# Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# @Copyright@
#
# $Log: __init__.py,v $
# Revision 1.13  2012/11/27 00:48:17  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.12  2012/05/06 05:48:27  phil
# Copyright Storm for Mamba
#
# Revision 1.11  2011/07/23 02:30:30  phil
# Viper Copyright
#
# Revision 1.10  2010/09/07 23:52:56  bruno
# star power for gb
#
# Revision 1.9  2009/05/01 19:06:58  mjk
# chimi con queso
#
# Revision 1.8  2008/10/18 00:55:50  mjk
# copyright 5.1
#
# Revision 1.7  2008/03/06 23:41:37  mjk
# copyright storm on
#
# Revision 1.6  2007/07/04 01:47:38  mjk
# embrace the anger
#
# Revision 1.5  2007/06/28 19:45:44  bruno
# all the 'rocks list host' commands now have help
#
# Revision 1.4  2007/06/19 16:42:41  mjk
# - fix add host interface docstring xml
# - update copyright
#
# Revision 1.3  2007/05/31 19:35:42  bruno
# first pass at getting all the 'help' consistent on all the rocks commands
#
# Revision 1.2  2007/05/10 20:37:01  mjk
# - massive rocks-command changes
# -- list host is standardized
# -- usage simpler
# -- help is the docstring
# -- host groups and select statements
# - added viz commands
#
# Revision 1.1  2007/04/30 17:46:03  bruno
# drop the 's' -- it makes the commands easier to use. for example, this type
# of interaction will be common:
#
#     # rocks list host partition compute-0-0
#     # rocks remove host partition compute-0-0 /var
#
# or:
#
#     # rocks list host interface compute-0-0
#     # rocks add host interface compute-0-0 if=eth1 ...
#
# by dropping the 's', we can use bash history and only change the verb and
# not also have to change 'interfaces' to 'interface'
#
# Revision 1.1  2007/04/24 17:58:09  bruno
# consist look and feel for all 'list' commands
#
# put partition commands under 'host'
#
# Revision 1.1  2007/04/05 20:51:55  bruno
# rocks-partition is now in the command line
#
#

import sys
import socket
import rocks.commands
import rocks.vm
import string

class Command(rocks.commands.list.host.command):
	"""
	Lists the partitions for hosts. For each host supplied on the command
	line, this command prints the hostname and partitions for that host.

	<arg optional='1' type='string' name='host' repeat='1'>
	Zero, one or more host names. If no host names are supplied, info about
	all the known hosts is listed.
	</arg>

	<param type='bool' name='bigmnt'>
	If true, then it will output only the biggest partition mount point
	(e.g. /state/partition1)
	</param>

	<example cmd='list host partition compute-0-0'>
	List partition info for compute-0-0.
	</example>

	<example cmd='list host partition'>
	List partition info for known hosts.
	</example>
	"""

	def run(self, params, args):

		(bigmnt,) = self.fillParams( [
			('bigmnt', 'n'),
			])

		bigmnt = self.str2bool(bigmnt)

		if bigmnt:
			# we just need to print the bigest partition mnt point
			vm = rocks.vm.VM(self.db)
			self.beginOutput()
			for host in self.getHostnames(args):
				self.addOutput(host, vm.getLargestPartition(host))
			self.endOutput(padChar='')
			return
	
		self.beginOutput()
		
		for host in self.getHostnames(args):
			self.db.execute("""select 
				p.device, p.mountpoint, p.sectorstart,
				p.partitionsize, p.partitionid, p.fstype,
				p.partitionflags, p.formatflags from 
				partitions p, nodes n where 
				n.name='%s' and n.id=p.node order by device""" %
				host)

			for row in self.db.fetchall():
				self.addOutput(host, row)

		self.endOutput(header=['host', 'device', 'mountpoint', 
			'start','size', 'id', 'type', 'flags', 'formatflags'])



