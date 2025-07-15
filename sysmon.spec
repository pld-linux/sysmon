# TODO:
#  - subpackages with stuff from OtherClients
Summary:	Network monitoring tool
Summary(pl.UTF-8):	Narzędzie do monitorowania sieci
Name:		sysmon
Version:	0.92.2
Release:	0.1
License:	GPL
Group:		Applications
Source0:	ftp://puck.nether.net/pub/jared/%{name}-%{version}.tar.gz
# Source0-md5:	be9304964bfd131be6098c4b7b502cd1
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-DESTDIR-headers.patch
URL:		http://www.sysmon.org
BuildRequires:	ncurses-devel
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Sysmon is a network monitoring tool designed to provide high
performance and accurate network monitoring. Currently supported
protocols include SMTP, IMAP, HTTP, TCP, UDP, NNTP, and PING tests.

%description -l pl.UTF-8
Sysmon to narzędzie monitorujace działanie sieci. Obecnie obsługiwane
protokoły to: SMTP, IMAP, HTTP, TCP, UDP, NNTP, oraz testy poprzez
PING.

%prep
%setup -q
%patch -P0 -p1

%build
%configure 
%{__make} -C src

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_mandir}/man1,%{_mandir}/man5,/etc/sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/sysmond
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/sysmond
install src/sysmon{,d} $RPM_BUILD_ROOT%{_bindir}
install docs/sysmon.man $RPM_BUILD_ROOT%{_mandir}/man1/sysmon.1
install docs/sysmon.conf.man $RPM_BUILD_ROOT%{_mandir}/man5/sysmon.conf.5
install examples/sysmon.conf.dist $RPM_BUILD_ROOT%{_sysconfdir}/sysmon.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add sysmond
%service sysmond restart

%preun
if [ "$1" = "0" ] ; then
	%service sysmond stop
	/sbin/chkconfig --del sysmond
fi

%files
%defattr(644,root,root,755)
%doc COPYRIGHT WISHLIST docs/[A-Z]* docs/*.jpg docs/*.html examples
%attr(755,root,root) %{_bindir}/*
%attr(754,root,root) /etc/rc.d/init.d/sysmond
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/sysmond
%{_sysconfdir}/sysmon.conf
%{_mandir}/man1/sysmon*
%{_mandir}/man5/sysmon.conf*
