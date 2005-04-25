#
# This Makefile builds a number of TET packages
#
# lsb-tet3-lite
# lsb-tet3-lite-devel
#
# This will fetch upstream sources, and install them
# and a patch into the RPM_SOURCE_DIR and then
# call rpmbuild
#
# Author: Andrew Josey, The Open Group, April 2005
# 
#========================================================
# You probably need to edit RPM_SOURCE_DIR
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
#
RPM_SOURCE_DIR	=	/home/ajosey/rpm/SOURCES
SOURCE1	=	tet3.6b-lite.unsup.src.tgz
SOURCE2	=	tet3-lite-manpages.tgz
PATCH1	=	tet3.6b-lite-lsb.patch
UPSTREAMSOURCES = $(SOURCE1) $(SOURCE2)
TETURL	=	http://www.opengroup.org/infosrv/TET/TET3/
                                                                                
first_make_rule: all
                                                                                
# there follows an in-line shell script
# remember that all shell commands need to be terminated by a ';'
# dummy is a dummy file to copy in place 
                                                                                
all:	fetchsrc
	@cp $(PATCH1) $(RPM_SOURCE_DIR)/; 
	rpmbuild -ba lsb-tet3-lite.spec

fetchsrc:
	@for i in $(UPSTREAMSOURCES);                                       \
        do                                                                  \
                echo $(RPM_SOURCE_DIR)/$$i...;                              \
                wget -O $(RPM_SOURCE_DIR)/$$i $(TETURL)/$$i;                \
                chmod 644 $(RPM_SOURCE_DIR)/$$i;                            \
        done;           

clean clobber:
	rm -f $(RPM_SOURCE_DIR)/$(SOURCE1) $(RPM_SOURCE_DIR)/$(SOURCE2) $(RPM_SOURCE_DIR)/$(PATCH1)
