%define apachedir /etc/httpd
%define apacheuser nobody
%define apachegroup nobody
%define contentdir /home/httpd

Name: imp
Version: 2.2.3
Release: 2cl
Summary: Web Based IMAP Mail Program 
Summary(pt_BR): Programa de Mail via Web
Summary(es): Programa de correo vía Internet basado en IMAP
BuildArchitectures: noarch
Group: Mail
Group(pt_BR): Correio Eletrônico
Group(es): Correo Eletrónico
License: GPL
Source0: ftp://ftp.horde.org/imp/imp-%{version}.tar.gz
Source1: pgsql_create.sql
Source2: pgsql_cuser.sh
Source3: menu.txt  
Source4: ImpLibVersion.def  
Source5: imp.conf
Patch: imp-2.2.3-cnc.patch
Buildroot: %{_tmppath}/%{name}-%{version}-root
Url: http://www.horde.org/imp
Requires: horde = 1.2.3 horde-phplib-storage mod_php3-imap >= 3.0.16
Prereq: perl webserver
BuildArchitectures: noarch

%description
IMP is the Internet Messaging Program, one of the Horde components.
It provides webmail access to IMAP and POP3 accounts.

The Horde Project writes web applications in PHP and releases them under
the GNU Public License.  For more information (including help with IMP)
please visit http://www.horde.org/.

%description -l pt_BR
Programa de Mail via Web baseado no IMAP

%description -l es
Programa de correo vía Internet basado en IMAP

%prep
%setup -q -n %{name}-%{version}
%patch -p1

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{apachedir}/conf
cp -p $RPM_SOURCE_DIR/imp.conf %{buildroot}%{apachedir}/conf
mkdir -p %{buildroot}%{contentdir}/html/horde/imp
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


%clean
rm -rf %{buildroot}

%post
grep -i 'Include.*imp.conf$' %{apachedir}/conf/httpd.conf >/dev/null 2>&1
if [ $? -eq 0 ]; then
	perl -pi -e 's/^#+// if (/Include.*imp.conf$/i);' %{apachedir}/conf/httpd.conf
else
	echo "Include %{apachedir}/conf/imp.conf" >>%{apachedir}/conf/httpd.conf
fi
#/sbin/service httpd restart
killall -HUP httpd > /dev/null 2>&1 || :
sleep 1  # settling time vs. installing multiple RPMs at a time


%postun
perl -pi -e 's/^/#/ if (/^Include.*imp.conf$/i);' %{apachedir}/conf/httpd.conf
#/sbin/service httpd restart
killall -HUP httpd > /dev/null 2>&1 || :
sleep 1  # settling time vs. installing multiple RPMs at a time


%files
%defattr(-,root,root)

# Apache imp.conf file
%config %{apachedir}/conf/imp.conf

# Include top level with %dir so not all files are sucked in
%dir %{contentdir}/html/horde/imp

# Include top-level files by hand
%{contentdir}/html/horde/imp/*.css
%{contentdir}/html/horde/imp/*.php3

# Include these dirs so that all files _will_ get sucked in
%{contentdir}/html/horde/imp/graphics
%{contentdir}/html/horde/imp/lib
%{contentdir}/html/horde/imp/locale
%{contentdir}/html/horde/imp/scripts
%{contentdir}/html/horde/imp/templates

# Mark documentation files with %doc and %docdir
# docdir not used anymore
%doc COPYING
%doc README 
%doc README.install
%doc docs/*
#docdir %{contentdir}/html/horde/imp/docs
#%{contentdir}/html/horde/imp/docs

# Mark configuration files with %config and use secure permissions
# (note that .dist files are considered software; don't mark %config)
%attr(750,root,%{apachegroup}) %dir %{contentdir}/html/horde/imp/config
%{contentdir}/html/horde/imp/config/*.dist
%defattr(-,root,root)
%config %{contentdir}/html/horde/imp/config/*.html
%config %{contentdir}/html/horde/imp/config/*.php3
%config %{contentdir}/html/horde/imp/config/*.txt


%changelog
* Fri Oct 13 2000 Andreas Hasenack <andreas@conectiva.com>
- added cnc patch for pt_BR, en and es ispell support in
  our distro. Thanks, Moises!

* Tue Oct 10 2000 Andreas Hasenack <andreas@conectiva.com>
- updated to 2.2.3

* Tue Sep 19 2000 Andreas Hasenack <andreas@conectiva.com>
- updated to 2.2.2, fixing a new security problem

* Tue Sep 12 2000 Andreas Hasenack <andreas@conectiva.com>
- major update. Spec file almost entirely taken from
  Brent J. Nordquist <bjn@horde.org>
- instead of httpd restart, using killall -HUP httpd
- new doc file placement
- created README.install file from info that was previously
  echoed to the screen during package installation

* Tue Aug 29 2000 Rodrigo Barbosa <rodrigob@conectiva.com>
- Adopted rpm macros

* Mon Aug 07 2000 Rudá Moura <ruda@conectiva.com>
- recompiled against rpm-3.0.5-5cl

* Sun Jun 18 2000 Rodrigo Parra Novo <rodarvus@conectiva.com>
- Do not try to use FQDN, when querying hostname
- Use /etc/httpd/conf/httpd.conf for $srm
- Use prereq for mod_php3, horde-core and webserver

* Tue Sep 14 1999 Guilherme Manika <gwm@conectiva.com>
- Converted pre to a bash script, and simplified it (I'm not sure it's still needed, but I'm being conservative)
- post and preun vastly simplified (doesn't touch php config, situations absent in Conectiva Linux are no longer checked)
- No longer uses databases by default, the user should Read The Fine Manual
- Doesn't restart any daemons
- Doesn't output anything to the screen

* Mon Sep 13 1999 Rodrigo Parra Novo <rodarvus@conectiva.com>
- Adopted by Conectiva Linux
- Removed most perl print messages (useless in an install)

* Tue Sep  7 1999  Pablo Costa <pablo@ib.usp.br>
- Upgrade to version 2.0.11

* Fri Jun 11 1999  Pablo Costa <pablo@ib.usp.br>
- Upgrade to version 2.0.6

* Fri Jun 10 1999  Pablo Costa <pablo@ib.usp.br>
- Upgrade to version 2.0.5
- Fix errors in portuguese locales
- Put doc in /usr/doc/imp because is required by impconfig 
- "$scripts = '/usr/doc/imp/examples/scripts';" 
- Build with rpm-3.0.1-12.6.0

* Thu Jun  3 1999  Henri Gomez <gomez@slib.fr>
- noarch added since perl and php code 
  nb:  use rpm -bb xxx.spec since rpm 3.0-6.0 core with -ba if BuildArch: none
- cleanup RPM

* Thu Jun  3 1999  Pablo Costa <pablo@shark.ib.usp.br>
- Initial RPM release
