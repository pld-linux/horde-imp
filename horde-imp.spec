%define	_hordeapp	imp
#define	_snap	2005-08-22
%define	_rc		rc2
%define	_rel	0.1
#
%include	/usr/lib/rpm/macros.php
Summary:	Web Based IMAP Mail Program
Summary(es):	Programa de correo vía Internet basado en IMAP
Summary(pl):	Program do obs³ugi poczty przez WWW korzystaj±cy z IMAP-a
Summary(pt_BR):	Programa de Mail via Web
Name:		%{_hordeapp}
Version:	4.0.4
Release:	%{?_rc:1.%{_rc}.}%{?_snap:0.%(echo %{_snap} | tr -d -).}%{_rel}
License:	GPL v2
Group:		Applications/WWW
#Source0:	http://ftp.horde.org/pub/snaps/%{_snap}/%{_hordeapp}-FRAMEWORK_3-%{_snap}.tar.gz
Source0:	ftp://ftp.horde.org/pub/imp/%{_hordeapp}-h3-%{version}-%{_rc}.tar.gz
# Source0-md5:	a573e10c1b53f45802f376826b9d6aaf
Source1:	%{_hordeapp}.conf
Patch0:		%{_hordeapp}-path.patch
URL:		http://www.horde.org/imp/
BuildRequires:	rpm-php-pearprov >= 4.0.2-98
BuildRequires:	rpmbuild(macros) >= 1.226
BuildRequires:	tar >= 1:1.15.1
Requires:	apache >= 1.3.33-2
Requires:	apache(mod_access)
Requires:	horde >= 3.0
Requires:	php-imap
Requires:	php-ctype
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# horde accesses it directly in help->about
%define		_noautocompressdoc  CREDITS
%define		_noautoreq			'pear(Horde.*)' 'pear(Text/Flowed.php)'

%define		hordedir	/usr/share/horde
%define		_sysconfdir	/etc/horde.org
%define		_appdir		%{hordedir}/%{_hordeapp}

%description
IMP is the Internet Messaging Program, one of the Horde components. It
provides webmail access to IMAP and POP3 accounts.

The Horde Project writes web applications in PHP and releases them
under the GNU Public License. For more information (including help
with IMP) please visit <http://www.horde.org/>.

%description -l es
Programa de correo vía Internet basado en IMAP.

%description -l pl
IMP jest programem do obs³ugi poczty przez WWW, bazowanym na Horde.
Daje dostêp do poczty poprzez IMAP oraz POP3.

Projekt Horde tworzy aplikacje WWW w PHP i wydaje je na licencji GNU
General Public License. Wiêcej informacji (w³±cznie z pomoc± dla
IMP-a) mo¿na znale¼æ na stronie <http://www.horde.org/>.

%description -l pt_BR
Programa de Mail via Web baseado no IMAP.

%prep
%setup -q -c -T -n %{?_snap:%{_hordeapp}-%{_snap}}%{!?_snap:%{_hordeapp}-%{version}%{?_rc:-%{_rc}}}
tar zxf %{SOURCE0} --strip-components=1
%patch0 -p1

sed -i -e '
	s,/somewhere/ca-bundle.crt,/usr/share/ssl/ca-bundle.crt,
	s,/usr/local/bin,%{_bindir},
' config/conf.xml

# considered harmful (horde/docs/SECURITY)
rm -f test.php

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp} \
	$RPM_BUILD_ROOT%{_appdir}/{docs,lib,locale,scripts,templates,themes}

cp -a *.php			$RPM_BUILD_ROOT%{_appdir}
for i in config/*.dist; do
	cp -a $i $RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp}/$(basename $i .dist)
done
echo '<?php ?>' >		$RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp}/conf.php
cp -p config/conf.xml	$RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp}/conf.xml
touch					$RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp}/conf.php.bak

cp -pR	lib/*			$RPM_BUILD_ROOT%{_appdir}/lib
cp -pR	locale/*		$RPM_BUILD_ROOT%{_appdir}/locale
cp -pR	templates/*		$RPM_BUILD_ROOT%{_appdir}/templates
cp -pR	themes/*		$RPM_BUILD_ROOT%{_appdir}/themes

ln -s %{_sysconfdir}/%{_hordeapp} 	$RPM_BUILD_ROOT%{_appdir}/config
ln -s %{_docdir}/%{name}-%{version}/CREDITS $RPM_BUILD_ROOT%{_appdir}/docs
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache-%{_hordeapp}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{_sysconfdir}/%{_hordeapp}/conf.php.bak ]; then
	install /dev/null -o root -g http -m660 %{_sysconfdir}/%{_hordeapp}/conf.php.bak
fi

%triggerin -- apache1 >= 1.3.33-2
%apache_config_install -v 1 -c %{_sysconfdir}/apache-%{_hordeapp}.conf

%triggerun -- apache1 >= 1.3.33-2
%apache_config_uninstall -v 1

%triggerin -- apache >= 2.0.0
%apache_config_install -v 2 -c %{_sysconfdir}/apache-%{_hordeapp}.conf

%triggerun -- apache >= 2.0.0
%apache_config_uninstall -v 2

%triggerpostun -- imp <= 3.2.6-0.1
for i in conf.php filter.txt header.txt html.php menu.php mime_drivers.php motd.php prefs.php servers.php trailer.txt; do
	if [ -f /home/services/httpd/html/horde/imp/config/$i.rpmsave ]; then
		mv -f %{_sysconfdir}/%{_hordeapp}/$i %{_sysconfdir}/%{_hordeapp}/$i.rpmnew
		mv -f /home/services/httpd/html/horde/imp/config/$i.rpmsave %{_sysconfdir}/%{_hordeapp}/$i
	fi
done

%triggerpostun -- imp <= 4.0.2-1
if [ -f /etc/httpd/imp.conf.rpmsave ]; then
	cp -f %{_sysconfdir}/apache-%{_hordeapp}.conf{,.rpmnew}
	mv -f /etc/httpd/imp.conf.rpmsave %{_sysconfdir}/apache-%{_hordeapp}.conf
fi

if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%files
%defattr(644,root,root,755)
%doc README docs/* scripts
%attr(750,root,http) %dir %{_sysconfdir}/%{_hordeapp}
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/apache-%{_hordeapp}.conf
%attr(660,root,http) %config(noreplace) %{_sysconfdir}/%{_hordeapp}/conf.php
%attr(660,root,http) %config(noreplace) %ghost %{_sysconfdir}/%{_hordeapp}/conf.php.bak
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/%{_hordeapp}/[!c]*.php
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/%{_hordeapp}/*.txt
%attr(640,root,http) %{_sysconfdir}/%{_hordeapp}/conf.xml

%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/config
%{_appdir}/docs
%{_appdir}/lib
%{_appdir}/locale
%{_appdir}/templates
%{_appdir}/themes
