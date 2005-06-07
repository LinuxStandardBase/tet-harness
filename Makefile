#
# This Makefile builds a number of TET packages
#
# lsb-tet3-lite
# lsb-tet3-lite-devel
#
# This will fetch upstream sources, and install them
# and a patch into the RPM_SOURCE_DIR and then
# call rpmbuild
# The rpms will install into /opt/lsb-tet3-lite,
# which is a LANANA registered path for the package
#
# You can also call 
# 	make tetpackages 
# to build non-LSB conforming rpms. These install into
# /opt/tet3-lite

# Author: Andrew Josey, The Open Group, April 2005
# 
#========================================================
# You will need to edit RPM_SOURCE_DIR
#
# If you use Fedora/RHEL you need write access to this 
# directory unless you set your own rpm build directory
#RPM_SOURCE_DIR	=	/usr/src/redhat/SOURCES
#
# To set your own rpm build directory, for example set
# 		%_topdir /home/ajosey/rpm
# in your ~/.rpmmacros file
#
# You should also set
#	%_binary_payload	w9.gzdio
#
#========================================================
#
# Edit the next line as required
#
RPM_SOURCE_DIR	=	/home/ajosey/rpm/SOURCES
#
#========================================================
# In theory the rest should not need changing
#
SOURCE1	=	tet3.6b-lite.unsup.src.tgz
SOURCE2	=	tet3-lite-manpages-v1.1.tgz
PATCH1	=	tet3.6b-lite-lsb.patch
UPSTREAMSOURCES = $(SOURCE1) $(SOURCE2)
TETURL	=	http://www.opengroup.org/infosrv/TET/TET3/

# this patch for building regular nonlsb tet packages
TPATCH1	=	tet3.6b-lite.patch
                                                                                
first_make_rule: all
                                                                                
# there follows an in-line shell script
# remember that all shell commands need to be terminated by a ';'
# dummy is a dummy file to copy in place 
                                                                                
all:	$(UPSTREAMSOURCES) $(PATCH1) lsb-tet3-lite.spec
	@cp $(UPSTREAMSOURCES) $(RPM_SOURCE_DIR)/;
	@cp $(PATCH1) $(RPM_SOURCE_DIR)/; 
	rpmbuild -ba lsb-tet3-lite.spec

fetchsrc: $(UPSTREAMSOURCES)

$(UPSTREAMSOURCES):
	@for i in $(UPSTREAMSOURCES);                                       \
        do                                                                  \
                echo fetching $(TETURL)/$$i ...;                              \
                wget -O $$i $(TETURL)/$$i;                \
                chmod 644 $$i;                            \
        done;           


# tetpackages are built using the regular gcc
tetpackages: $(UPSTREAMSOURCES) $(TPATCH1) tet3-lite.spec 
	@cp $(UPSTREAMSOURCES) $(RPM_SOURCE_DIR)/;
	@cp $(TPATCH1) $(RPM_SOURCE_DIR)/;
	rpmbuild -ba tet3-lite.spec

clean clobber:
	rm -f $(RPM_SOURCE_DIR)/$(SOURCE1) $(RPM_SOURCE_DIR)/$(SOURCE2) $(RPM_SOURCE_DIR)/$(PATCH1) $(RPM_SOURCE_DIR)/$(TPATCH1) $(SOURCE1) $(SOURCE2)
