#
# Conditional build:
# _without_javascript - don't use javascript interpreter
# _without_graphics - don't use graphics
# _without_svgalib - compile without svgalib graphics driver
# _without_directfb - compile without DirectFB support
# _without_x - compile without X Window System graphics driver
# _without_fb - compile without Linux Framebuffer graphics driver
# _without_pmshell - compile without PMShell graphics driver
# _without_atheos - compile without Atheos graphics driver

%ifnarch %{ix86} alpha
%define _without_svgalib 1
%endif
Summary:	Lynx-like WWW browser
Summary(es):	El links es un browser para modo texto, similar a lynx
Summary(pl):	Podobna do Lynksa przegl�darka WWW
Summary(pt_BR):	O links � um browser para modo texto, similar ao lynx
Summary(ru):	��������� WWW ������� ���� Lynx
Summary(uk):	��������� WWW ������� ���� Lynx
Name:		links-hacked
Version:	030316
Release:	1
License:	GPL v2
Group:		Applications/Networking
Source0:	http://xray.sai.msu.ru/~karpov/%{name}/downloads/%{name}-%{version}.tgz
Source1:	http://xray.sai.msu.ru/~karpov/%{name}/downloads/links-fonts-new.tgz
Source2:	%{name}.desktop
Source3:	linksh.png
Patch0:		%{name}-js-Date-getTime.patch
Patch1:		%{name}-js-submit-nodefer.patch
Patch2:		%{name}-etc_dir.patch
Patch3:		%{name}-ac25x.patch
Patch4:		%{name}-suffix.patch
URL:		http://xray.sai.msu.ru/~karpov/%{name}/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gpm-devel
BuildRequires:	openssl-devel >= 0.9.7
BuildRequires:	zlib-devel
%if%{!?_without_graphics:1}%{?_without_graphics:0}
%{!?_without_directfb:BuildRequires:	DirectFB-devel}
BuildRequires:	freetype-devel
BuildRequires:	libpng-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libtiff-devel
%{!?_without_javascript:BuildRequires:	flex}
%{!?_without_javascript:BuildRequires:	bison}
%{!?_without_svgalib:BuildRequires:	svgalib-devel}
%{!?_without_x:BuildRequires:	XFree86-devel}
%endif
Provides:	webclient
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Links is a WWW browser, at first look similiar to Lynx, but somehow
different:

- renders tables and frames,
- displays colors as specified in current HTML page,
- uses drop-down menu (like in Midnight Commander),
- can download files in background.

%{!?_without_graphics:This version can work in graphical mode.}
%{!?_without_javascript:This version has support for JavaScript.}

Links-hacked is based on links2 and elinks.

%description -l es
Links es un browser WWW modo texto, similar al Lynx. El links muestra
tablas, hace baja archivos en segundo plano, y usa conexiones HTTP/1.1
keepalive.

%description -l pl
Links jest przegl�dark� WWW, na pierwszy rzut oka podobn� do Lynksa,
ale mimo wszystko inn�:

- renderuje tabelki i ramki,
- wy�wietla kolory zgodnie z definicjami w ogl�danej stronie HTML,
- u�ywa opuszczanego menu (jak w Midnight Commanderze),
- mo�e �ci�ga� pliki w tle.

%{!?_without_graphics:Ta wersja mo�e pracowa� w trybie graficznym.}
%{!?_without_javascript:Ta wersja obs�uguje JavaScript.}

Links-hacked jest oparty na kodzie links2 i elinksa.

%description -l pt_BR
Links � um browser WWW modo texto, similar ao Lynx. O Links exibe
tabelas, faz baixa arquivos em segundo plano, e usa as conex�es
HTTP/1.1 keepalive.

%description -l ru
Links - ��� ��������� WWW �������, �� ������ ������ ������� �� Lynx,
�� ��������� ������������:

- ���������� ������� � (�����) ������,
- ���������� ����� ��� ������� � HTML ��������,
- ���������� ���������� ���� (��� � Midnight Commander),
- ����� ��������� ����� � ����.

%description -l uk
Links - �� ��������� WWW �������, �� ������ ������ ������ �� Lynx, ���
����� צ�ͦ���� צ� �����:

- צ�������� �����æ �� (���������) ������,
- �����դ ������� �� ������� � HTML ���Ҧ�æ,
- ����������դ �������ަ ���� (�� � Midnight Commander),
- ���� ������������� ����� � ��Φ.

%prep
%setup -q -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
rm -f missing
%{__aclocal}
%{__automake}
%{__autoheader}
%{__autoconf}
%configure \
	--program-suffix=h \
	%{!?_without_graphics:--enable-graphics} \
	%{!?_without_javascript:--enable-javascript} \
	%{?_without_svgalib:--without-svgalib} \
	%{?_without_x:--without-x} \
	%{?_without_fb:--without-fb} \
	%{?_without_pmshell:--without-pmshell} \
	%{?_without_atheos:--without-atheos} \
	%{?_without_directfb:--without-directfb}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_applnkdir}/Network/WWW,%{_pixmapsdir}}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE2} $RPM_BUILD_ROOT%{_applnkdir}/Network/WWW

#install %{SOURCE2} $RPM_BUILD_ROOT%{_mandir}/pl/man1/links2.1
install %{SOURCE3} $RPM_BUILD_ROOT%{_pixmapsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog README SITES TODO docs/*
%attr(755,root,root) %{_bindir}/*
%{_applnkdir}/Network/WWW/*
%{_mandir}/man*/*
#%lang(pl) %{_mandir}/pl/man*/*
%{_pixmapsdir}/*
