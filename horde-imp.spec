%define		_RC	RC2
%define		_rel	1
Summary:	Web Based IMAP Mail Program
Summary(pl):	Program do obs³ugi poczty przez www korzystaj±cy z IMAP'a
Summary(es):	Programa de correo vía Internet basado en IMAP
Summary(pt_BR):	Programa de Mail via Web
Name:		imp
Version:	3.1
Release:	%{_RC}.%{_rel}
License:	GPL v2
Group:		Applications/Mail
Source0:	ftp://ftp.horde.org/pub/imp/tarballs/%{name}-%{version}-%{_RC}.tar.gz
Source1:	%{name}.conf
Source2:	%{name}-pgsql_create.sql
Source3:	%{name}-pgsql_cuser.sh
Source4:	%{name}-menu.txt
Source5:	%{name}-ImpLibVersion.def
URL:		http://www.horde.org/imp/
Requires:	horde >= 2.0
Requires:	php-imap
Prereq:		perl
Prereq:		webserver
BuildArch:	noarch
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		apachedir	/etc/httpd
%define		contentdir	/home/httpd

%description
IMP is the Internet Messaging Program, one of the Horde components. It
provides webmail access to IMAP and POP3 accounts.

The Horde Project writes web applications in PHP and releases them
under the GNU Public License. For more information (including help
with IMP) please visit http://www.horde.org/.

%description -l pl
IMP jest programem do obs³ugi poczty przez www, bazowanym na Horde.
Daje dostêp do poczty poprzez IMAP oraz POP3.

Projekt Horde tworzy aplikacje w PHP i dostarcza je na licencji GNU
Public License. Je¿eli chcesz siê dowiedzieæ czego¶ wiêcej (tak¿e help
do IMP'a) zajrzyj na stronê http://www.horde.org

%description -l pt_BR
Programa de Mail via Web baseado no IMAP

%description -l es
Programa de correo vía Internet basado en IMAP

%prep
%setup -q -n %{name}-%{version}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{apachedir},/etc/cron.daily}
install -d $RPM_BUILD_ROOT%{contentdir}/html/horde/imp/{config,graphics,lib,locale,scripts,templates}

install %{SOURCE1} $RPM_BUILD_ROOT%{apachedir}
cp -pR	*.php			$RPM_BUILD_ROOT%{contentdir}/html/horde/imp
cp -pR	config/*.dist		$RPM_BUILD_ROOT%{contentdir}/html/horde/imp/config
cp -pR	graphics/*		$RPM_BUILD_ROOT%{contentdir}/html/horde/imp/graphics
cp -pR	lib/*			$RPM_BUILD_ROOT%{contentdir}/html/horde/imp/lib
cp -pR	locale/*		$RPM_BUILD_ROOT%{contentdir}/html/horde/imp/locale
cp -pR	scripts/*.php		$RPM_BUILD_ROOT%{contentdir}/html/horde/imp/scripts
cp -pR	templates/*		$RPM_BUILD_ROOT%{contentdir}/html/horde/imp/templates

cp -p	config/.htaccess	$RPM_BUILD_ROOT%{contentdir}/html/horde/imp/config
cp -p	locale/.htaccess	$RPM_BUILD_ROOT%{contentdir}/html/horde/imp/locale
cp -p	scripts/.htaccess	$RPM_BUILD_ROOT%{contentdir}/html/horde/imp/scripts
cp -p	templates/.htaccess	$RPM_BUILD_ROOT%{contentdir}/html/horde/imp/templates

install scripts/imp-cleanup.cron $RPM_BUILD_ROOT/etc/cron.daily/imp-cleanup

ln -sf	%{contentdir}/html/horde/imp/config $RPM_BUILD_ROOT%{apachedir}/imp

cd $RPM_BUILD_ROOT%{contentdir}/html/horde/imp/config/
for i in *.dist; do cp $i `basename $i .dist`; done

%clean
rm -rf $RPM_BUILD_ROOT

%post
grep -i 'Include.*imp.conf$' %{apachedir}/httpd.conf >/dev/null 2>&1
echo "Changing apache configuration"
if [ $? -eq 0 ]; then
	perl -pi -e 's/^#+// if (/Include.*imp.conf$/i);' %{apachedir}/httpd.conf
else
	echo "Include %{apachedir}/imp.conf" >>%{apachedir}/httpd.conf
fi

if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/httpd start\" to start http daemon."
fi


%postun
echo "Changing apache configuration"
perl -pi -e 's/^/#/ if (/^Include.*imp.conf$/i);' %{apachedir}/httpd.conf
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/httpd start\" to start http daemon."
fi

%files
%defattr(644,root,root,755)
%doc README docs/* scripts/*.reg scripts/*.pl

%dir %{contentdir}/html/horde/imp
%attr(640,root,http) %{contentdir}/html/horde/imp/*.php
%attr(750,root,http) %{contentdir}/html/horde/imp/graphics
%attr(750,root,http) %{contentdir}/html/horde/imp/lib
%attr(750,root,http) %{contentdir}/html/horde/imp/locale
%attr(750,root,http) %{contentdir}/html/horde/imp/scripts
%attr(750,root,http) %{contentdir}/html/horde/imp/templates

%attr(750,root,http) %dir %{contentdir}/html/horde/imp/config
%attr(640,root,http) %{contentdir}/html/horde/imp/config/*.dist
%attr(640,root,http) %{contentdir}/html/horde/imp/config/.htaccess
%attr(640,root,http) %config(noreplace) %{apachedir}/imp.conf
%attr(640,root,http) %config(noreplace) %{contentdir}/html/horde/imp/config/*.php
%attr(640,root,http) %config(noreplace) %{contentdir}/html/horde/imp/config/*.txt
%attr(755,root,root) %config(noreplace) /etc/cron.daily/imp-cleanup
%{apachedir}/imp
