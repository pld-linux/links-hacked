#
# Conditional build:
%bcond_without  javascript	# don't use javascript interpreter
%bcond_without	graphics	# don't use graphics
%bcond_without	svga		# compile without svgalib graphics driver
%bcond_without	directfb	# compile without DirectFB support
%bcond_without	x		# compile without X Window System graphics driver
%bcond_without	fb		# compile without Linux Framebuffer graphics driver
%bcond_without	pmshell		# compile without PMShell graphics driver
%bcond_without	atheos		# compile without Atheos graphics driver
#
%ifnarch %{ix86} alpha
%undefine 	with_svga
%endif
Summary:	Lynx-like WWW browser
Summary(es):	El links es un browser para modo texto, similar a lynx
Summary(pl):	Podobna do Lynksa przegl╠darka WWW
Summary(pt_BR):	O links И um browser para modo texto, similar ao lynx
Summary(ru):	Текстовый WWW броузер типа Lynx
Summary(uk):	Текстовий WWW броузер типу Lynx
Name:		links-hacked
Version:	031220
Release:	1
License:	GPL v2
Group:		Applications/Networking
Source0:	http://xray.sai.msu.ru/~karpov/%{name}/downloads/%{name}-%{version}.tgz
# Source0-md5:	402d9490638b0e158d6122bd5bb830f2
Source1:	http://xray.sai.msu.ru/~karpov/%{name}/downloads/links-fonts-new.tgz
# Source1-md5:	1176ee9132c9df8c1ec955e28bff6f5b
Source2:	%{name}.desktop
Source3:	linksh.png
Patch0:		%{name}-js-Date-getTime.patch
Patch1:		%{name}-js-submit-nodefer.patch
Patch2:		%{name}-etc_dir.patch
Patch3:		%{name}-ac25x.patch
Patch4:		%{name}-suffix.patch
URL:		http://xray.sai.msu.ru/~karpov/links-hacked/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gpm-devel
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	zlib-devel
%if %{with graphics}
%{?with_directfb:BuildRequires:	DirectFB-devel}
BuildRequires:	freetype-devel
BuildRequires:	libpng-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libtiff-devel
%{?with_javascript:BuildRequires:	flex}
%{?with_javascript:BuildRequires:	bison}
%{?with_svga:BuildRequires:	svgalib-devel}
%{?with_x:BuildRequires:	XFree86-devel}
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

%description -l es
Links es un browser WWW modo texto, similar al Lynx. El links muestra
tablas, hace baja archivos en segundo plano, y usa conexiones HTTP/1.1
keepalive.

%description -l pl
Links jest przegl╠dark╠ WWW, na pierwszy rzut oka podobn╠ do Lynksa,
ale mimo wszystko inn╠:

- renderuje tabelki i ramki,
- wy╤wietla kolory zgodnie z definicjami w ogl╠danej stronie HTML,
- u©ywa opuszczanego menu (jak w Midnight Commanderze),
- mo©e ╤ci╠gaФ pliki w tle.

%{?with_graphics:Ta wersja mo©e pracowaФ w trybie graficznym.}
%{?with_javascript:Ta wersja obsЁuguje JavaScript.}

Links-hacked jest oparty na kodzie links2 i elinksa.

%description -l pt_BR
Links И um browser WWW modo texto, similar ao Lynx. O Links exibe
tabelas, faz baixa arquivos em segundo plano, e usa as conexУes
HTTP/1.1 keepalive.

%description -l ru
Links - это текстовый WWW броузер, на первый взгляд похожий на Lynx,
но несколько отличающийся:

- отображает таблицы и (скоро) фреймы,
- показывает цвета как указано в HTML странице,
- использует выпадающие меню (как в Midnight Commander),
- может загружать файлы в фоне.

%description -l uk
Links - це текстовий WWW броузер, на перший погляд схожий на Lynx, але
трохи в╕дм╕нний в╕д нього:

- в╕добража╓ таблиц╕ та (незабаром) фрейми,
- показу╓ кольори як вказано в HTML стор╕нц╕,
- використову╓ випадаюч╕ меню (як в Midnight Commander),
- може завантажувати файли в фон╕.

%prep
%setup -q -n %{name} -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
rm -rf autom4te.cache

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
