%include	/usr/lib/rpm/macros.php
Summary:	Web Based IMAP Mail Program
Summary(es):	Programa de correo v�a Internet basado en IMAP
Summary(pl):	Program do obs�ugi poczty przez WWW korzystaj�cy z IMAP-a
Summary(pt_BR):	Programa de Mail via Web
Name:		imp
Version:	3.2.6
Release:	0.5
License:	GPL v2
Group:		Applications/Mail
Source0:	ftp://ftp.horde.org/pub/imp/tarballs/%{name}-%{version}.tar.gz
# Source0-md5:	0a12763bef44a1928f59cc72da7d854d
Source1:	%{name}.conf
Source2:	%{name}-pgsql_create.sql
Source3:	%{name}-pgsql_cuser.sh
Source4:	%{name}-menu.txt
Source5:	%{name}-ImpLibVersion.def
Patch0:		%{name}-path.patch
URL:		http://www.horde.org/imp/
BuildRequires:	rpm-php-pearprov >= 4.0.2-98
PreReq:		apache
Requires(post):	grep
Requires:	crondaemon
Requires:	horde >= 2.0
Requires:	php-imap
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
Programa de correo v�a Internet basado en IMAP.

%description -l pl
IMP jest programem do obs�ugi poczty przez WWW, bazowanym na Horde.
Daje dost�p do poczty poprzez IMAP oraz POP3.

Projekt Horde tworzy aplikacje w PHP i dostarcza je na licencji GNU
Public License. Je�eli chcesz si� dowiedzie� czego� wi�cej (tak�e help
do IMP-a) zajrzyj na stron� http://www.horde.org/ .

%description -l pt_BR
Programa de Mail via Web baseado no IMAP.

%prep
%setup -q
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{apachedir},/etc/cron.daily,%{confdir}/imp} \
	$RPM_BUILD_ROOT%{hordedir}/imp/{config,graphics,lib,locale,scripts,templates}

cp -pR	*.php			$RPM_BUILD_ROOT%{hordedir}/imp
cp -pR	config/*.dist		$RPM_BUILD_ROOT%{confdir}/imp
cp -pR	graphics/*		$RPM_BUILD_ROOT%{hordedir}/imp/graphics
cp -pR	lib/*			$RPM_BUILD_ROOT%{hordedir}/imp/lib
cp -pR	locale/*		$RPM_BUILD_ROOT%{hordedir}/imp/locale
cp -pR	scripts/*.php		$RPM_BUILD_ROOT%{hordedir}/imp/scripts
cp -pR	templates/*		$RPM_BUILD_ROOT%{hordedir}/imp/templates

cp -p	config/.htaccess	$RPM_BUILD_ROOT%{confdir}/imp
cp -p	locale/.htaccess	$RPM_BUILD_ROOT%{hordedir}/imp/locale
cp -p	scripts/.htaccess	$RPM_BUILD_ROOT%{hordedir}/imp/scripts
cp -p	templates/.htaccess	$RPM_BUILD_ROOT%{hordedir}/imp/templates

install scripts/imp-cleanup.cron $RPM_BUILD_ROOT/etc/cron.daily/imp-cleanup
ln -sf	%{confdir}/%{name} $RPM_BUILD_ROOT%{hordedir}/%{name}/config

install %{SOURCE1} $RPM_BUILD_ROOT%{apachedir}

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
%doc README docs/* scripts/*.reg scripts/*.pl
%dir %{hordedir}/%{name}
%attr(640,root,http) %{hordedir}/%{name}/*.php
%attr(750,root,http) %{hordedir}/%{name}/graphics
%attr(750,root,http) %{hordedir}/%{name}/lib
%attr(750,root,http) %{hordedir}/%{name}/locale
%attr(750,root,http) %{hordedir}/%{name}/scripts
%attr(750,root,http) %{hordedir}/%{name}/templates

%attr(750,root,http) %dir %{confdir}/%{name}
%{hordedir}/%{name}/config
%attr(640,root,http) %{confdir}/%{name}/*.dist
%attr(640,root,http) %{confdir}/%{name}/.htaccess
%attr(640,root,http) %config(noreplace) %{apachedir}/%{name}.conf
%attr(640,root,http) %config(noreplace) %{confdir}/%{name}/*.php
%attr(640,root,http) %config(noreplace) %{confdir}/%{name}/*.txt
%attr(755,root,root) %config(noreplace) /etc/cron.daily/%{name}-cleanup
