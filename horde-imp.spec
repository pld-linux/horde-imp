
%define name imp
%define version 4.0.2
%define pre rc1
%define fname %{name}-h3-%{version}-%pre

Summary:	Web Based IMAP Mail Program
Summary(es):	Programa de correo vía Internet basado en IMAP
Summary(pl):	Program do obs³ugi poczty przez WWW korzystaj±cy z IMAP-a
Summary(pt_BR):	Programa de Mail via Web
Name:		%{name}
Version:	%{version}
Release:	0.%{pre}.1
License:	GPL v2
Group:		Applications/Mail
Source0:	ftp://ftp.horde.org/pub/imp/%{fname}.tar.gz
# Source0-md5:	7dd6427b0ca4faf1a4410c4a855f007c
Source1:	%{name}.conf
Source2:	%{name}-pgsql_create.sql
Source3:	%{name}-pgsql_cuser.sh
Source4:	%{name}-menu.txt
Source5:	%{name}-ImpLibVersion.def
Source6:	%{name}-trans.mo
Patch0:		%{name}-path.patch
Patch1:		%{name}-login.patch
URL:		http://www.horde.org/imp/
PreReq:		apache
Requires(post):	grep
Requires:	horde >= 3.0
Requires:	php-imap
Requires:	php-ctype
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{fname}-root-%(id -u -n)

%define		apachedir	/etc/httpd
%define		hordedir	/usr/share/horde
%define		confdir		/etc/horde.org

%description
IMP is the Internet Messaging Program, one of the Horde components. It
provides webmail access to IMAP and POP3 accounts.

The Horde Project writes web applications in PHP and releases them
under the GNU Public License. For more information (including help
with IMP) please visit http://www.horde.org/ .

%description -l es
Programa de correo vía Internet basado en IMAP.

%description -l pl
IMP jest programem do obs³ugi poczty przez WWW, bazowanym na Horde.
Daje dostêp do poczty poprzez IMAP oraz POP3.

Projekt Horde tworzy aplikacje w PHP i dostarcza je na licencji GNU
Public License. Je¿eli chcesz siê dowiedzieæ czego¶ wiêcej (tak¿e help
do IMP-a) zajrzyj na stronê http://www.horde.org/ .

%description -l pt_BR
Programa de Mail via Web baseado no IMAP.

%prep
%setup -q -n %{fname}
%patch0 -p1
%patch1 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{apachedir},/etc/cron.daily,%{confdir}/imp} \
	$RPM_BUILD_ROOT%{hordedir}/imp/{lib,locale,scripts,templates,themes}

cp -pR	*.php			$RPM_BUILD_ROOT%{hordedir}/imp
cp -pR	config/*.dist		$RPM_BUILD_ROOT%{confdir}/imp
cp -pR	config/*.xml		$RPM_BUILD_ROOT%{confdir}/imp
echo "<?php ?>" > 		$RPM_BUILD_ROOT%{confdir}/imp/conf.php
cp -pR	lib/*			$RPM_BUILD_ROOT%{hordedir}/imp/lib
cp -pR	locale/*		$RPM_BUILD_ROOT%{hordedir}/imp/locale
cp -pR	scripts/*.php		$RPM_BUILD_ROOT%{hordedir}/imp/scripts
cp -pR	templates/*		$RPM_BUILD_ROOT%{hordedir}/imp/templates
cp -pR	themes/*		$RPM_BUILD_ROOT%{hordedir}/imp/themes

cp -p	config/.htaccess	$RPM_BUILD_ROOT%{confdir}/imp
cp -p	locale/.htaccess	$RPM_BUILD_ROOT%{hordedir}/imp/locale
cp -p	scripts/.htaccess	$RPM_BUILD_ROOT%{hordedir}/imp/scripts
cp -p	templates/.htaccess	$RPM_BUILD_ROOT%{hordedir}/imp/templates

ln -sf	%{confdir}/%{name} 	$RPM_BUILD_ROOT%{hordedir}/%{name}/config

install %{SOURCE1} 		$RPM_BUILD_ROOT%{apachedir}
install %{SOURCE6} 		$RPM_BUILD_ROOT%{hordedir}/imp/locale/pl_PL/LC_MESSAGES/imp.mo

cd $RPM_BUILD_ROOT%{confdir}/imp
for i in *.dist; do cp $i `basename $i .dist`; done

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*%{name}.conf" /etc/httpd/httpd.conf; then
	echo "Include /etc/httpd/%{name}.conf" >> /etc/httpd/httpd.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
elif [ -d /etc/httpd/httpd.conf ]; then
	ln -sf /etc/httpd/%{name}.conf /etc/httpd/httpd.conf/99_%{name}.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
fi

%preun
if [ "$1" = "0" ]; then
	umask 027
	if [ -d /etc/httpd/httpd.conf ]; then
		rm -f /etc/httpd/httpd.conf/99_%{name}.conf
	else
		grep -v "^Include.*%{name}.conf" /etc/httpd/httpd.conf > \
			/etc/httpd/httpd.conf.tmp
		mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
	fi
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
fi

%triggerpostun -- imp <= 3.2.6-0.1
for i in conf.php filter.txt header.txt html.php menu.php mime_drivers.php motd.php prefs.php servers.php trailer.txt; do
	if [ -f /home/services/httpd/html/horde/imp/config/$i.rpmsave ]; then
		mv -f %{confdir}/%{name}/$i %{confdir}/%{name}/$i.rpmnew
		mv -f /home/services/httpd/html/horde/imp/config/$i.rpmsave %{confdir}/%{name}/$i
	fi
done

%files
%defattr(644,root,root,755)
%doc README docs/* scripts/*.reg
%dir %{hordedir}/%{name}
%attr(640,root,http) %{hordedir}/%{name}/*.php
%attr(750,root,http) %{hordedir}/%{name}/lib
%attr(750,root,http) %{hordedir}/%{name}/locale
%attr(750,root,http) %{hordedir}/%{name}/scripts
%attr(750,root,http) %{hordedir}/%{name}/templates
%attr(750,root,http) %{hordedir}/%{name}/themes

%attr(750,root,http) %dir %{confdir}/%{name}
%{hordedir}/%{name}/config
%attr(640,root,http) %{confdir}/%{name}/*.dist
%attr(640,root,http) %{confdir}/%{name}/*.xml
%attr(640,root,http) %{confdir}/%{name}/.htaccess
%attr(640,root,http) %config(noreplace) %{apachedir}/%{name}.conf
%attr(660,root,http) %config(noreplace) %{confdir}/%{name}/*.php
%attr(640,root,http) %config(noreplace) %{confdir}/%{name}/*.txt
