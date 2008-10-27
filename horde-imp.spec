#
# NOTE: When upgrading check if (almost) all languages have translations
#	needed by imp-iportant.patch, and update the patch accordingly
#
%define		hordeapp	imp
#
%include	/usr/lib/rpm/macros.php
Summary:	Web Based IMAP Mail Program
Summary(es.UTF-8):	Programa de correo vía Internet basado en IMAP
Summary(pl.UTF-8):	Program do obsługi poczty przez WWW korzystający z IMAP-a
Summary(pt_BR.UTF-8):	Programa de Mail via Web
Name:		horde-%{hordeapp}
Version:	4.3
Release:	5
License:	GPL v2
Group:		Applications/WWW
Source0:	ftp://ftp.horde.org/pub/imp/%{hordeapp}-h3-%{version}.tar.gz
# Source0-md5:	63e41417c8f31daf1b3b6eaa64a65ac2
Source1:	%{hordeapp}.conf
Patch0:		%{hordeapp}-path.patch
Patch1:		%{hordeapp}-prefs.patch
Patch2:		%{hordeapp}-quota_hook.patch
Patch3:		%{hordeapp}-auth.patch
Patch4:		%{hordeapp}-important.patch
URL:		http://www.horde.org/imp/
BuildRequires:	gettext-devel
BuildRequires:	rpm-php-pearprov >= 4.0.2-98
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	horde >= 3.0
Requires:	php(ctype)
Requires:	php(imap)
Requires:	php(openssl)
Requires:	php(tidy)
Requires:	webapps
Suggests:	php-pear-Auth_SASL
Suggests:	php-pear-HTTP_Request
Suggests:	php-pecl-idn
Obsoletes:	imp
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreq	'pear(/usr/share/horde.*)' 'pear(Horde.*)' 'pear(Text/Flowed.php)'

%define		hordedir	/usr/share/horde
%define		_appdir		%{hordedir}/%{hordeapp}
%define		_webapps	/etc/webapps
%define		_webapp		horde-%{hordeapp}
%define		_sysconfdir	%{_webapps}/%{_webapp}

%description
IMP is the Internet Messaging Program, one of the Horde components. It
provides webmail access to IMAP and POP3 accounts.

The Horde Project writes web applications in PHP and releases them
under the GNU Public License. For more information (including help
with IMP) please visit <http://www.horde.org/>.

%description -l es.UTF-8
Programa de correo vía Internet basado en IMAP.

%description -l pl.UTF-8
IMP jest programem do obsługi poczty przez WWW, bazowanym na Horde.
Daje dostęp do poczty poprzez IMAP oraz POP3.

Projekt Horde tworzy aplikacje WWW w PHP i wydaje je na licencji GNU
General Public License. Więcej informacji (włącznie z pomocą dla
IMP-a) można znaleźć na stronie <http://www.horde.org/>.

%description -l pt_BR.UTF-8
Programa de Mail via Web baseado no IMAP.

%prep
%setup -q -n %{hordeapp}-h3-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

for i in config/*.dist; do
	mv $i config/$(basename $i .dist)
done
# considered harmful (horde/docs/SECURITY)
rm test.php
# remove backup files from patching
find '(' -name '*~' -o -name '*.orig' ')' | xargs -r rm -v

cd po
for file in *.po ; do
	__lang=${file%.po}
	msgfmt $file -o ../locale/$__lang/LC_MESSAGES/imp.mo
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}/docs}

cp -a *.php $RPM_BUILD_ROOT%{_appdir}
cp -a config/* $RPM_BUILD_ROOT%{_sysconfdir}
echo '<?php ?>' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.php
touch $RPM_BUILD_ROOT%{_sysconfdir}/conf.php.bak
cp -a js lib locale templates themes $RPM_BUILD_ROOT%{_appdir}
cp -a docs/CREDITS $RPM_BUILD_ROOT%{_appdir}/docs

ln -s %{_sysconfdir} 	$RPM_BUILD_ROOT%{_appdir}/config
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{_sysconfdir}/conf.php.bak ]; then
	install /dev/null -o root -g http -m660 %{_sysconfdir}/conf.php.bak
fi

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerpostun -- horde-imp < 4.0.4-1.10, imp
for i in conf.php filter.txt header.txt html.php menu.php mime_drivers.php motd.php prefs.php servers.php trailer.txt; do
	if [ -f /home/services/httpd/html/horde/imp/config/$i.rpmsave ]; then
		mv -f %{_sysconfdir}/$i{,.rpmnew}
		mv -f /home/services/httpd/html/horde/imp/config/$i.rpmsave %{_sysconfdir}/$i
	fi
done

if [ -f /etc/httpd/imp.conf.rpmsave ]; then
	mv -f %{_sysconfdir}/apache.conf{,.rpmnew}
	mv -f %{_sysconfdir}/httpd.conf{,.rpmnew}
	cp -f /etc/httpd/imp.conf.rpmsave %{_sysconfdir}/apache.conf
	cp -f /etc/httpd/imp.conf.rpmsave %{_sysconfdir}/httpd.conf
	rm -f /etc/httpd/imp.conf.rpmsave
	httpd_reload=1
fi

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
	rm -f /etc/apache/conf.d/99_horde-imp.conf
	/usr/sbin/webapp register apache %{_webapp}
	%service -q apache reload
fi
if [ -L /etc/httpd/httpd.conf/99_horde-imp.conf ]; then
	rm -f /etc/httpd/httpd.conf/99_horde-imp.conf
	/usr/sbin/webapp register httpd %{_webapp}
	httpd_reload=1
fi

if [ "$httpd_reload" ]; then
	%service -q httpd reload
fi

%files
%defattr(644,root,root,755)
%doc README docs/* scripts
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(660,root,http) %config(noreplace) %{_sysconfdir}/conf.php
%attr(660,root,http) %config(noreplace) %ghost %{_sysconfdir}/conf.php.bak
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/[!c]*.php
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/*.txt
%attr(640,root,http) %{_sysconfdir}/conf.xml

%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/config
%{_appdir}/docs
%{_appdir}/js
%{_appdir}/lib
%{_appdir}/locale
%{_appdir}/templates
%{_appdir}/themes
