Summary:	Web Based IMAP Mail Program 
Summary(pl):	Program do obs³ugi poczty przez www korzystaj±cy z IMAP'a
Summary(es):	Programa de correo vía Internet basado en IMAP
Summary(pt_BR): Programa de Mail via Web
Name:		imp
Version:	2.3.6
Release:	1
License:	GPL
Group:		Applications/Mail
Group(de):	Applikationen/Post
Group(pl):	Aplikacje/Poczta
Group(pt):	Aplicações/Correio Eletrônico
Source0:	ftp://ftp.horde.org/pub/imp/tarballs/%{name}-%{version}.tar.gz
Source1:	%{name}-pgsql_create.sql
Source2:	%{name}-pgsql_cuser.sh
Source3:	%{name}-menu.txt
Source4:	%{name}-ImpLibVersion.def
Source5:	%{name}.conf
Patch0:		%{name}-cnc.patch
URL:		http://www.horde.org/imp/
Requires:	horde = 1.2.6 
Requires:	horde-phplib-storage
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
Public License. Je¿eli chcesz siê dowiedzieæ czego¶ wiêcej (tak¿e
help do IMP'a) zajrzyj na stronê http://www.horde.org

%description -l pt_BR
Programa de Mail via Web baseado no IMAP

%description -l es
Programa de correo vía Internet basado en IMAP

%prep
%setup -q -n %{name}-%{version}
#%patch -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d %{buildroot}%{apachedir}/conf

cp -p $RPM_SOURCE_DIR/imp.conf %{buildroot}%{apachedir}/conf
install -d %{buildroot}%{contentdir}/html/horde/imp
cp -pR * %{buildroot}%{contentdir}/html/horde/imp

cat <<_EOF2_ > $RPM_BUILD_DIR/%{name}-%{version}/README.install
IMPORTANT:  If you are installing for the first time, you must now
configure IMP.  The following commands (run as root) will do this:

# cd %{contentdir}/html/horde
# sh install.sh
(visit http://example.com/horde/setup.php3 in a browser)
# sh secure.sh

If you are using a database, you also need to set the database password:

# sh scripts/database/dbpasswd.sh

(See %{_docdir}/%{name}-%{version}/INSTALL for more information.)

_EOF2_

gzip -9nf README README.install

%clean
rm -rf %{buildroot}

%post
grep -i 'Include.*imp.conf$' %{apachedir}/conf/httpd.conf >/dev/null 2>&1
echo "Changing apache configuration"
if [ $? -eq 0 ]; then
	perl -pi -e 's/^#+// if (/Include.*imp.conf$/i);' %{apachedir}/conf/httpd.conf
else
	echo "Include %{apachedir}/conf/imp.conf" >>%{apachedir}/conf/httpd.conf
fi

if [ -f /var/lock/subsys/httpd ]; then
	echo "Restarting httpd daemon"
	/etc/rc.d/init.d/httpd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/httpd start\" to start apache http daemon."
fi


%postun
echo "Changing apache configuration"
perl -pi -e 's/^/#/ if (/^Include.*imp.conf$/i);' %{apachedir}/conf/httpd.conf
if [ -f /var/lock/subsys/httpd ]; then
	echo "Restarting httpd daemon"
	/etc/rc.d/init.d/httpd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/httpd start\" to start apache http daemon."
fi

%files
%defattr(644,root,root,755)

# Apache imp.conf file
%config %{apachedir}/conf/imp.conf

# Include top level with %dir so not all files are sucked in
%dir %{contentdir}/html/horde/imp

# Include top-level files by hand
#%{contentdir}/html/horde/imp/*.css
%{contentdir}/html/horde/imp/*.php

# Include these dirs so that all files _will_ get sucked in
%{contentdir}/html/horde/imp/graphics
%{contentdir}/html/horde/imp/lib
%{contentdir}/html/horde/imp/locale
%{contentdir}/html/horde/imp/scripts
%{contentdir}/html/horde/imp/templates

# Mark documentation files with %doc and %docdir
# docdir not used anymore
%doc *.gz
%doc docs/*
#docdir %{contentdir}/html/horde/imp/docs
#%{contentdir}/html/horde/imp/docs

# Mark configuration files with %config and use secure permissions
# (note that .dist files are considered software; don't mark %config)
%attr(750,root,http) %dir %{contentdir}/html/horde/imp/config
%{contentdir}/html/horde/imp/config/*.dist
%defattr(-,root,root)
%config %{contentdir}/html/horde/imp/config/*.html
%config %{contentdir}/html/horde/imp/config/*.txt
%config %{contentdir}/html/horde/imp/config/*.dt
