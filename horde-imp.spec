%define	_hordeapp	imp
#define	_snap	2005-08-22
#define	_rc		rc2
%define	_rel	1.15
#
%include	/usr/lib/rpm/macros.php
Summary:	Web Based IMAP Mail Program
Summary(es):	Programa de correo v�a Internet basado en IMAP
Summary(pl):	Program do obs�ugi poczty przez WWW korzystaj�cy z IMAP-a
Summary(pt_BR):	Programa de Mail via Web
Name:		horde-%{_hordeapp}
Version:	4.0.4
Release:	%{?_rc:1.%{_rc}.}%{?_snap:0.%(echo %{_snap} | tr -d -).}%{_rel}
License:	GPL v2
Group:		Applications/WWW
Source0:	ftp://ftp.horde.org/pub/imp/%{_hordeapp}-h3-%{version}.tar.gz
# Source0-md5:	437767b420c6280e680a42c8e34182d1
#Source0:	http://ftp.horde.org/pub/snaps/%{_snap}/%{_hordeapp}-FRAMEWORK_3-%{_snap}.tar.gz
#Source0:	ftp://ftp.horde.org/pub/imp/%{_hordeapp}-h3-%{version}-%{_rc}.tar.gz
Source1:	%{_hordeapp}.conf
Patch0:		%{_hordeapp}-path.patch
Patch1:		%{_hordeapp}-prefs.patch
URL:		http://www.horde.org/imp/
BuildRequires:	rpm-php-pearprov >= 4.0.2-98
BuildRequires:	rpmbuild(macros) >= 1.226
BuildRequires:	tar >= 1:1.15.1
Requires:	apache(mod_access)
Requires:	horde >= 3.0
Requires:	php-ctype
Requires:	php-imap
Requires:	webapps
Requires:	webserver = apache
Obsoletes:	%{_hordeapp}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# horde accesses it directly in help->about
%define		_noautocompressdoc  CREDITS
%define		_noautoreq			'pear(Horde.*)' 'pear(Text/Flowed.php)'

%define		hordedir	/usr/share/horde
%define		_appdir		%{hordedir}/%{_hordeapp}
%define		_webapps	/etc/webapps
%define		_webapp		horde-%{_hordeapp}
%define		_sysconfdir	%{_webapps}/%{_webapp}

%description
IMP is the Internet Messaging Program, one of the Horde components. It
provides webmail access to IMAP and POP3 accounts.

The Horde Project writes web applications in PHP and releases them
under the GNU Public License. For more information (including help
with IMP) please visit <http://www.horde.org/>.

%description -l es
Programa de correo v�a Internet basado en IMAP.

%description -l pl
IMP jest programem do obs�ugi poczty przez WWW, bazowanym na Horde.
Daje dost�p do poczty poprzez IMAP oraz POP3.

Projekt Horde tworzy aplikacje WWW w PHP i wydaje je na licencji GNU
General Public License. Wi�cej informacji (w��cznie z pomoc� dla
IMP-a) mo�na znale�� na stronie <http://www.horde.org/>.

%description -l pt_BR
Programa de Mail via Web baseado no IMAP.

%prep
%setup -qcT -n %{?_snap:%{_hordeapp}-%{_snap}}%{!?_snap:%{_hordeapp}-%{version}%{?_rc:-%{_rc}}}
tar zxf %{SOURCE0} --strip-components=1
%patch0 -p1
%patch1 -p1

rm -f {,*/}.htaccess
for i in config/*.dist; do
	mv $i config/$(basename $i .dist)
done
# considered harmful (horde/docs/SECURITY)
rm -f test.php

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}/docs}

cp -a *.php $RPM_BUILD_ROOT%{_appdir}
cp -a config/* $RPM_BUILD_ROOT%{_sysconfdir}
echo '<?php ?>' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.php
touch $RPM_BUILD_ROOT%{_sysconfdir}/conf.php.bak
cp -a lib locale templates themes $RPM_BUILD_ROOT%{_appdir}

ln -s %{_sysconfdir} 	$RPM_BUILD_ROOT%{_appdir}/config
ln -s %{_docdir}/%{name}-%{version}/CREDITS $RPM_BUILD_ROOT%{_appdir}/docs
install %{SOURCE1} $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/httpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{_sysconfdir}/conf.php.bak ]; then
	install /dev/null -o root -g http -m660 %{_sysconfdir}/conf.php.bak
fi

%triggerin -- apache1
%webapp_register apache %{_webapp}

%triggerun -- apache1
%webapp_unregister apache %{_webapp}

%triggerin -- apache >= 2.0.0
%webapp_register httpd %{_webapp}

%triggerun -- apache >= 2.0.0
%webapp_unregister httpd %{_webapp}

%triggerpostun -- imp <= 3.2.6-0.1
for i in conf.php filter.txt header.txt html.php menu.php mime_drivers.php motd.php prefs.php servers.php trailer.txt; do
	if [ -f /home/services/httpd/html/horde/imp/config/$i.rpmsave ]; then
		mv -f %{_sysconfdir}/$i{,.rpmnew}
		mv -f /home/services/httpd/html/horde/imp/config/$i.rpmsave %{_sysconfdir}/$i
	fi
done

%triggerpostun -- imp <= 4.0.2-1
if [ -f /etc/httpd/imp.conf.rpmsave ]; then
	mv -f %{_sysconfdir}/apache.conf{,.rpmnew}
	mv -f %{_sysconfdir}/httpd.conf{,.rpmnew}
	cp -f /etc/httpd/imp.conf.rpmsave %{_sysconfdir}/apache.conf
	cp -f /etc/httpd/imp.conf.rpmsave %{_sysconfdir}/httpd.conf
	rm -f /etc/httpd/imp.conf.rpmsave
fi

if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd reload 1>&2
fi

%triggerpostun -- horde-imp < 4.0.4-1.10
for i in conf.php filter.txt header.txt menu.php mime_drivers.php motd.php prefs.php servers.php trailer.txt; do
	if [ -f /etc/horde.org/imp/$i.rpmsave ]; then
		mv -f %{_sysconfdir}/$i{,.rpmnew}
		mv -f /etc/horde.org/imp/$i.rpmsave %{_sysconfdir}/$i
	fi
done

if [ -f /etc/horde.org/apache-imp.conf.rpmsave ]; then
	mv -f %{_sysconfdir}/apache.conf{,.rpmnew}
	mv -f %{_sysconfdir}/httpd.conf{,.rpmnew}
	cp -f /etc/horde.org/apache-imp.conf.rpmsave %{_sysconfdir}/apache.conf
	cp -f /etc/horde.org/apache-imp.conf.rpmsave %{_sysconfdir}/httpd.conf
	rm -f /etc/horde.org/apache-imp.conf.rpmsave
fi

if [ -L /etc/apache/conf.d/99_horde-imp.conf ]; then
	/usr/sbin/webapp register apache %{_webapp}
	rm -f /etc/apache/conf.d/99_horde-imp.conf
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache reload 1>&2
	fi
fi
if [ -L /etc/httpd/httpd.conf/99_horde-imp.conf ]; then
	/usr/sbin/webapp register httpd %{_webapp}
	rm -f /etc/httpd/httpd.conf/99_horde-imp.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd reload 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc README docs/* scripts
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/httpd.conf
%attr(660,root,http) %config(noreplace) %{_sysconfdir}/conf.php
%attr(660,root,http) %config(noreplace) %ghost %{_sysconfdir}/conf.php.bak
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/[!c]*.php
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/*.txt
%attr(640,root,http) %{_sysconfdir}/conf.xml

%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/config
%{_appdir}/docs
%{_appdir}/lib
%{_appdir}/locale
%{_appdir}/templates
%{_appdir}/themes
