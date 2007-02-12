#
# Conditional build:
%bcond_without	javascript	# don't use javascript interpreter
%bcond_without	graphics	# don't use graphics
%bcond_without	svga		# compile without svgalib graphics driver
%bcond_without	directfb	# compile without DirectFB support
%bcond_without	x		# compile without X Window System graphics driver
%bcond_without	fb		# compile without Linux Framebuffer graphics driver
%bcond_without	pmshell		# compile without PMShell graphics driver
%bcond_without	atheos		# compile without Atheos graphics driver
#
Summary:	Lynx-like WWW browser
Summary(es.UTF-8):   El links es un browser para modo texto, similar a lynx
Summary(pl.UTF-8):   Podobna do Lynksa przeglądarka WWW
Summary(pt_BR.UTF-8):   O links é um browser para modo texto, similar ao lynx
Summary(ru.UTF-8):   Текстовый WWW броузер типа Lynx
Summary(uk.UTF-8):   Текстовий WWW броузер типу Lynx
Name:		links-hacked
Version:	031220
Release:	6
License:	GPL v2
Group:		Applications/Networking
Source0:	http://xray.sai.msu.ru/~karpov/links-hacked/downloads/%{name}-%{version}.tgz
# Source0-md5:	402d9490638b0e158d6122bd5bb830f2
Source1:	http://xray.sai.msu.ru/~karpov/links-hacked/downloads/links-fonts-new.tgz
# Source1-md5:	1176ee9132c9df8c1ec955e28bff6f5b
Source2:	%{name}.desktop
Source3:	linksh.png
Patch0:		%{name}-js-Date-getTime.patch
Patch1:		%{name}-js-submit-nodefer.patch
Patch2:		%{name}-etc_dir.patch
Patch3:		%{name}-ac25x.patch
Patch4:		%{name}-suffix.patch
Patch5:		%{name}-gcc34.patch
Patch6:		%{name}-en-fix.patch
Patch7:		%{name}-pl-update.patch
URL:		http://xray.sai.msu.ru/~karpov/links-hacked/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	gpm-devel
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	zlib-devel
%if %{with graphics}
%{?with_directfb:BuildRequires:	DirectFB-devel}
%{?with_x:BuildRequires:	XFree86-devel}
%{?with_javascript:BuildRequires:	bison}
%{?with_javascript:BuildRequires:	flex}
BuildRequires:	freetype-devel
BuildRequires:	libpng-devel >= 2:1.2.7-2
BuildRequires:	libjpeg-devel
BuildRequires:	libtiff-devel
%{?with_svga:BuildRequires:	svgalib-devel}
Requires:	libpng >= 2:1.2.7-2
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

%{?with_graphics:This version can work in graphical mode.}
%{?with_javascript:This version has support for JavaScript.}

Links-hacked is based on links2 and elinks.

%description -l es.UTF-8
Links es un browser WWW modo texto, similar al Lynx. El links muestra
tablas, hace baja archivos en segundo plano, y usa conexiones HTTP/1.1
keepalive.

%description -l pl.UTF-8
Links jest przeglądarką WWW, na pierwszy rzut oka podobną do Lynksa,
ale mimo wszystko inną:

- renderuje tabelki i ramki,
- wyświetla kolory zgodnie z definicjami w oglądanej stronie HTML,
- używa opuszczanego menu (jak w Midnight Commanderze),
- może ściągać pliki w tle.

%{?with_graphics:Ta wersja może pracować w trybie graficznym.}
%{?with_javascript:Ta wersja obsługuje JavaScript.}

Links-hacked jest oparty na kodzie links2 i elinksa.

%description -l pt_BR.UTF-8
Links é um browser WWW modo texto, similar ao Lynx. O Links exibe
tabelas, faz baixa arquivos em segundo plano, e usa as conexões
HTTP/1.1 keepalive.

%description -l ru.UTF-8
Links - это текстовый WWW броузер, на первый взгляд похожий на Lynx,
но несколько отличающийся:

- отображает таблицы и (скоро) фреймы,
- показывает цвета как указано в HTML странице,
- использует выпадающие меню (как в Midnight Commander),
- может загружать файлы в фоне.

%description -l uk.UTF-8
Links - це текстовий WWW броузер, на перший погляд схожий на Lynx, але
трохи відмінний від нього:

- відображає таблиці та (незабаром) фрейми,
- показує кольори як вказано в HTML сторінці,
- використовує випадаючі меню (як в Midnight Commander),
- може завантажувати файли в фоні.

%prep
%setup -q -n %{name} -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

rm -rf autom4te.cache

cd intl
./gen-intl

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--program-suffix=h \
	%{?with_graphics:--enable-graphics} \
	%{?with_javascript:--enable-javascript} \
	%{!?with_svga:--without-svgalib} \
	%{!?with_x:--without-x} \
	%{!?with_fb:--without-fb} \
	%{!?with_pmshell:--without-pmshell} \
	%{!?with_atheos:--without-atheos} \
	%{!?with_directfb:--without-directfb}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE3} $RPM_BUILD_ROOT%{_pixmapsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog README SITES TODO docs/*
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*
