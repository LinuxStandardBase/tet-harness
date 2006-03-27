# Non LSB Conforming version
Summary: Test Environment Toolkit
Name: tet3-lite
Version: 3.7
Release: 1
Source0: tet3.7-unsup.src.tgz
Source1: tet3-lite-manpages-v1.1.tgz
Patch0: tet3.7-lite.patch
License: Artistic
Group: Development/Tools
Buildroot: %{_builddir}/%{name}-root

#AutoReqProv: no

%description
This is a lite package of the Test Environment Toolkit.
The Test Environment Toolkit is a standard framework for
developing and running test cases.

%prep

%setup  -cn tet3-lite-3.7 -q -a1
%patch -p1


%build

python -V > .PYTHONINFO 2>&1
PYTHONVERSION=`cat .PYTHONINFO | cut -d " " -f 2 | cut -d "." -f 1,2`
echo $PYTHONVERSION
rm -f .PYTHONINFO

if [ ! -d /usr/lib/python$PYTHONVERSION ]
then
        echo "Can not find the python library in your system"
        exit 1
fi

export TET_ROOT=`pwd`

sh ./configure -t lite
cd src && make && make install
cd ..

mv contrib/python_api/Makefile contrib/python_api/Makefile.old
sed "s@/usr/include/python2.2@/usr/include/python2.3@g" contrib/python_api/Makefile.old > contrib/python_api/Makefile
rm -f contrib/python_api/Makefile.old
cd contrib/python_api && make

%install

rm -rf $RPM_BUILD_ROOT
cd src && make  install
cd ..
mkdir -p $RPM_BUILD_ROOT/opt/tet3-lite
find inc lib bin man contrib -print|grep -v .keep_me|cpio -pdv $RPM_BUILD_ROOT/opt/tet3-lite/
mkdir -p $RPM_BUILD_ROOT/opt/tet3-lite/doc
cp  README.FIRST Artistic Licence $RPM_BUILD_ROOT/opt/tet3-lite/doc/
install -m 555 contrib/scripts/vres $RPM_BUILD_ROOT/opt/tet3-lite/bin/vres
install -m 555 contrib/scripts/dres $RPM_BUILD_ROOT/opt/tet3-lite/bin/dres
mkdir -p $RPM_BUILD_ROOT/opt/tet3-lite/lib/python
install -m 644 contrib/python_api/README $RPM_BUILD_ROOT/opt/tet3-lite/lib/python/README
install -m 755 contrib/python_api/pytet.py $RPM_BUILD_ROOT/opt/tet3-lite/lib/python/pytet.py
install -m 755 contrib/python_api/_pytet.so $RPM_BUILD_ROOT/opt/tet3-lite/lib/python/_pytet.so

sed -e "/^HOME=/d" -e "s@^echo Unconfigured@TET_ROOT=/opt/tet3-lite@" profile.skeleton > $RPM_BUILD_ROOT/opt/tet3-lite/profile 


%files

%defattr(-,bin,bin)

/opt/tet3-lite/bin
#/opt/tet3-lite/inc
#/opt/tet3-lite/lib
/opt/tet3-lite/lib/ksh/tcm.ksh
/opt/tet3-lite/lib/ksh/tetapi.ksh
/opt/tet3-lite/lib/perl/api.pl
/opt/tet3-lite/lib/perl/tcm.pl
/opt/tet3-lite/lib/perl/README
/opt/tet3-lite/lib/python/README
/opt/tet3-lite/lib/python/pytet.py
/opt/tet3-lite/lib/python/_pytet.so
/opt/tet3-lite/lib/posix_sh/tcm.sh
/opt/tet3-lite/lib/posix_sh/tetapi.sh
/opt/tet3-lite/lib/tet3/libapi_s.so
/opt/tet3-lite/lib/tet3/libthrapi_s.so
/opt/tet3-lite/lib/xpg3sh/tcm.sh
/opt/tet3-lite/lib/xpg3sh/tetapi.sh
/opt/tet3-lite/lib/grw/example.css
/opt/tet3-lite/profile

%dir /opt/tet3-lite
%dir /opt/tet3-lite/man

%doc /opt/tet3-lite/doc
%doc /opt/tet3-lite/man/man1
%doc /opt/tet3-lite/man/man4



%post

# put out a message 

echo 
echo "To use the TET-lite package set your TET_ROOT, PATH, MANPATH and PYTHONPATH environment"
echo "variables, for example:"
echo "   export TET_ROOT=/opt/tet3-lite"
echo "   export PATH=\$PATH:\$TET_ROOT/bin"
echo "   export MANPATH=\$MANPATH:\$TET_ROOT/man"
echo "   export PYTHONPATH=\$TET_ROOT/lib/python"
echo "See /opt/tet3-lite/profile for sample profile additions"
echo


#-------------------------devel--------------------
%package devel
Summary: Development option for TET
Group: Development/Tools
Requires:       tet3-lite

%description devel
This is a package of the TET development environment for
building tests from source.  The Test Environment Toolkit is a standard
framework for developing and running test cases.

%files devel

%defattr(-,bin,bin)

/opt/tet3-lite/inc
#/opt/tet3-lite/lib
/opt/tet3-lite/lib/tet3/libapi.a
/opt/tet3-lite/lib/tet3/libthrapi.a
/opt/tet3-lite/lib/tet3/tcm.o
/opt/tet3-lite/lib/tet3/tcmchild.o
/opt/tet3-lite/lib/tet3/tcm_m.o
/opt/tet3-lite/lib/tet3/tcmc_m.o
/opt/tet3-lite/lib/tet3/thrtcm.o
/opt/tet3-lite/lib/tet3/thrtcmchild.o
/opt/tet3-lite/lib/tet3/thrtcm_m.o
/opt/tet3-lite/lib/tet3/thrtcmc_m.o
/opt/tet3-lite/lib/tet3/libtcm_s.a
/opt/tet3-lite/lib/tet3/tcm_s.o
/opt/tet3-lite/lib/tet3/tcmchild_s.o
/opt/tet3-lite/lib/tet3/tcm_ms.o
/opt/tet3-lite/lib/tet3/tcmc_ms.o
/opt/tet3-lite/lib/tet3/libthrtcm_s.a
/opt/tet3-lite/lib/tet3/thrtcm_s.o
/opt/tet3-lite/lib/tet3/thrtcmchild_s.o
/opt/tet3-lite/lib/tet3/thrtcm_ms.o
/opt/tet3-lite/lib/tet3/thrtcmc_ms.o
/opt/tet3-lite/lib/tet3/Ctcm.o
/opt/tet3-lite/lib/tet3/Ctcmchild.o
/opt/tet3-lite/lib/tet3/Cthrtcm.o
/opt/tet3-lite/lib/tet3/Cthrtcmchild.o
/opt/tet3-lite/lib/tet3/Ctcm_s.o
/opt/tet3-lite/lib/tet3/Ctcmchild_s.o
/opt/tet3-lite/lib/tet3/Cthrtcm_s.o
/opt/tet3-lite/lib/tet3/Cthrtcmchild_s.o
%doc /opt/tet3-lite/man/man3

#-------------------------contrib--------------------
%package contrib
Summary: Demo test suites and tools option for TET
Group: Development/Tools
Requires:       tet3-devel
AutoReqProv: no

%description contrib
This is a package of the TET contrib distribution featuring
demonstration test suites and tools (report writers etc)
for TET.
The Test Environment Toolkit is a standard
framework for developing and running test cases.

%files contrib

%defattr(-,bin,bin)

/opt/tet3-lite/contrib




#----------------------------------------
%changelog

* Mon Mar 27 2006 Rui Feng

Update to tet3.7

* Wed Jan 11 2006  Rui Feng                         

Add the support for python api 

* Tue Jun 07 2005  Andrew Josey

Ensure devel package lib/tet3 tree does not overlap with base package

* Thu Apr  28 2005  Andrew Josey

Include all the runtime components in the Base package

* Wed Mar  9 2005  Andrew Josey

Change payload to be gzip'd rather than bzip'd

* Thu Mar  3 2005  Andrew Josey

Add supplementary binaries, and also contrib addon package

* Wed Mar  2 2005  Andrew Josey

Add TET devel package

* Tue Mar  1 2005  Andrew Josey

Initial spec file for an tet lite package

