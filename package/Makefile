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

PACKAGE=tet3-lite
LSB_PACKAGE=lsb-tet3-lite
VERSION=3.7
LSBRelease=3
RELEASE=10
LSB_RELEASE=$(RELEASE).lsb$(LSBRelease)

FULL_PACKAGE_NAME=$(PACKAGE)-$(VERSION)
LSB_FULL_PACKAGE_NAME=$(LSB_PACKAGE)-$(VERSION)

TET_DOC_DIR=/opt/$(PACKAGE)/doc
LSB_TET_DOC_DIR=/opt/$(LSB_PACKAGE)/doc

TET_SOURCE_NAME=$(FULL_PACKAGE_NAME)-$(RELEASE).src.rpm
TET_BINARY_NAME=$(FULL_PACKAGE_NAME)-$(RELEASE).$(RPM_BUILD_ARCH).rpm
TET_DEVEL_BINARY_NAME=$(PACKAGE)-devel-$(VERSION)-$(RELEASE).$(RPM_BUILD_ARCH).rpm
LSB_TET_SOURCE_NAME=$(LSB_FULL_PACKAGE_NAME)-$(LSB_RELEASE).src.rpm
LSB_TET_BINARY_NAME=$(LSB_FULL_PACKAGE_NAME)-$(LSB_RELEASE).$(RPM_BUILD_ARCH).rpm
LSB_TET_DEVEL_BINARY_NAME=$(LSB_PACKAGE)-devel-$(VERSION)-$(LSB_RELEASE).$(RPM_BUILD_ARCH).rpm

SOURCE1	=	tet3.7-unsup.src.tgz
SOURCE2	=	tet3-lite-manpages-v1.1.tgz
PATCH1	=	tet3.7-lite-lsb.patch
SUPPORT =	support.tgz
SOURCE3 =	$(SUPPORT)
UPSTREAMSOURCES = $(SOURCE1) $(SOURCE2)
TETURL	=	http://www.opengroup.org/infosrv/TET/TET3/

# this patch for building regular nonlsb tet packages
TPATCH1	=	tet3.7-lite.patch

PWD=$(shell pwd)

# Determine whether to use rpm or rpmbuild to build the packages
ifeq ($(wildcard /usr/bin/rpmbuild),)
	RPM_BUILD_CMD=rpm
else
	RPM_BUILD_CMD=rpmbuild 
endif

# Get RPM configuration information
# NOTE THAT RPM_TMP_BUILD_DIR IS DELETED AFTER THE RPM BUILD IS COMPLETED
# The rpmrc file translates targets where there are multiple choices per
# architecture. On build, the derived RPM_BUILD_ARCH is given as the target
RCFILELIST="/usr/lib/rpm/rpmrc:./rpmrc"
RPM_TMP_BUILD_DIR=$(HOME)/tmp/rpm-build
RPM_BUILD_ARCH=$(shell rpm --rcfile ${RCFILELIST} --eval=%{_target_cpu})
RPM_BINARY_DIR=$(RPM_TMP_BUILD_DIR)/RPMS/$(RPM_BUILD_ARCH)
RPM_SRPM_DIR=$(RPM_TMP_BUILD_DIR)/SRPMS

                                                                                
first_make_rule: all
                                                                                
# there follows an in-line shell script
# remember that all shell commands need to be terminated by a ';'
# dummy is a dummy file to copy in place 

ifndef BUILD_NO_DEB
all: lsbtetpackage deb_package
else
all: lsbtetpackage
endif

lsbtetpackage: $(LSB_TET_SOURCE_NAME) $(LSB_TET_BINARY_NAME) $(LSB_TET_DEVEL_BINARY_NAME)
                                                                                
$(LSB_TET_SOURCE_NAME) $(LSB_TET_BINARY_NAME) $(LSB_TET_DEVEL_BINARY_NAME):	$(UPSTREAMSOURCES) $(SUPPORT) $(PATCH1) $(LSB_PACKAGE).spec
	@mkdir -p $(RPM_TMP_BUILD_DIR)/BUILD
	@mkdir -p $(RPM_TMP_BUILD_DIR)/RPMS
	@mkdir -p $(RPM_TMP_BUILD_DIR)/SRPMS
ifdef SIGN_PACKAGES
	@expect -c 'set timeout -1' -c 'spawn $(RPM_BUILD_CMD) --sign --rcfile ${RCFILELIST} --define=_sourcedir\ $(PWD) --define=_topdir\ $(RPM_TMP_BUILD_DIR) --define=_target_cpu\ $(RPM_BUILD_ARCH) --define=_defaultdocdir\ $(LSB_TET_DOC_DIR) --define=rel\ $(RELEASE) -ba $(LSB_PACKAGE).spec' -c 'expect -ex "Enter pass phrase:"' -c 'send "\n"' -c 'expect "Executing(%clean)"' -c 'expect "exit 0"' -c 'send "\n"'
else
	@$(RPM_BUILD_CMD) --rcfile ${RCFILELIST} --define="_sourcedir $(PWD)" --define="_topdir $(RPM_TMP_BUILD_DIR)" --define="_target_cpu $(RPM_BUILD_ARCH)" --define="_defaultdocdir $(LSB_TET_DOC_DIR)" --define="rel $(RELEASE)" -ba $(LSB_PACKAGE).spec
endif
	@mv $(RPM_SRPM_DIR)/$(LSB_TET_SOURCE_NAME) .
	@mv $(RPM_BINARY_DIR)/$(LSB_TET_BINARY_NAME) .
	@mv $(RPM_BINARY_DIR)/$(LSB_TET_DEVEL_BINARY_NAME) .
	@rm -rf $(RPM_TMP_BUILD_DIR)


fetchsrc: $(UPSTREAMSOURCES)

$(UPSTREAMSOURCES):
	@for i in $(UPSTREAMSOURCES);                                       \
        do                                                                  \
                echo fetching $(TETURL)/$$i ...;                              \
                wget -O $$i $(TETURL)/$$i;                \
                chmod 644 $$i;                            \
        done;           

$(SUPPORT): support/tjreport support/tjreport.1
	tar zcvf $(SUPPORT) support

# tetpackages are built using the regular gcc
tetpackage: $(TET_SOURCE_NAME) $(TET_BINARY_NAME) $(TET_DEVEL_BINARY_NAME)
                                                                                
$(TET_SOURCE_NAME) $(TET_BINARY_NAME) $(TET_DEVEL_BINARY_NAME):	$(UPSTREAMSOURCES) $(PATCH1) $(PACKAGE).spec
	@mkdir -p $(RPM_TMP_BUILD_DIR)/BUILD
	@mkdir -p $(RPM_TMP_BUILD_DIR)/RPMS
	@mkdir -p $(RPM_TMP_BUILD_DIR)/SRPMS

	@$(RPM_BUILD_CMD) --rcfile ${RCFILELIST} --define="_sourcedir $(PWD)" --define="_topdir $(RPM_TMP_BUILD_DIR)" --define="_target_cpu $(RPM_BUILD_ARCH)" --define="_defaultdocdir $(LSB_TET_DOC_DIR)" -ba $(PACKAGE).spec

	@mv $(RPM_SRPM_DIR)/$(TET_SOURCE_NAME) .
	@mv $(RPM_BINARY_DIR)/$(TET_BINARY_NAME) .
	@mv $(RPM_BINARY_DIR)/$(TET_DEVEL_BINARY_NAME) .
	@rm -rf $(RPM_TMP_BUILD_DIR)

deb_package: $(LSB_TET_BINARY_NAME) $(LSB_TET_DEVEL_BINARY_NAME)
	@fakeroot alien -cdk $(LSB_TET_BINARY_NAME)
	@fakeroot alien -cdk $(LSB_TET_DEVEL_BINARY_NAME)

list_uploadable:
	@echo $(LSB_TET_BINARY_NAME) $(LSB_TET_DEVEL_BINARY_NAME)
ifndef BUILD_NO_DEB
	@ls *.deb
endif

clean clobber:
	rm -f $(RPM_SOURCE_DIR)/$(SOURCE1) $(RPM_SOURCE_DIR)/$(SOURCE2) $(RPM_SOURCE_DIR)/$(PATCH1) $(RPM_SOURCE_DIR)/$(TPATCH1) $(SOURCE1) $(SOURCE2) $(SOURCE3) *.rpm *.deb
