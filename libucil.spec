#
# Conditional build:
%bcond_with	ffmpeg	# avcodec support (needs some unidentified ffmpeg version)

Summary:	Unicap Imaging Library - simple image processing functions
Summary(pl.UTF-8):	Unicap Imaging Library - biblioteka prostych funkcji przetwarzania obrazu
Name:		libucil
Version:	0.9.10
Release:	8
License:	GPL v2+
Group:		Libraries
#Source0Download: http://unicap-imaging.org/download.htm
Source0:	http://unicap-imaging.org/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	986adfd387d64726acd0267565ff9431
Patch0:		%{name}-ac.patch
URL:		http://unicap-imaging.org/
BuildRequires:	alsa-lib-devel >= 0.9
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
%{?with_ffmpeg:BuildRequires:	ffmpeg-devel >= ? < ?}
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.11.0
BuildRequires:	gstreamer-devel >= 0.10
BuildRequires:	gstreamer-plugins-base-devel >= 0.10
BuildRequires:	gtk-doc >= 1.4
BuildRequires:	libpng-devel
BuildRequires:	libtheora-devel
BuildRequires:	libtool
BuildRequires:	libunicap-devel
BuildRequires:	libvorbis-devel
BuildRequires:	pango-devel
BuildRequires:	pkgconfig
Requires:	glib2 >= 1:2.11.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Unicap Imaging Library is a set of simple image processing functions.

%description -l pl.UTF-8
Unicap Imaging Library to biblioteka prostych funkcji przetwarzania
obrazu.

%package devel
Summary:	Header files for ucil library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ucil
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	alsa-lib-devel >= 0.9
%{?with_ffmpeg:Requires:	ffmpeg-devel}
Requires:	glib2-devel >= 1:2.11.0
Requires:	gstreamer-devel >= 0.10
Requires:	gstreamer-plugins-base-devel >= 0.10
Requires:	libpng-devel
Requires:	libtheora-devel
Requires:	libunicap-devel
Requires:	libvorbis-devel
Requires:	pango-devel

%description devel
Header files for ucil library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki ucil.

%package static
Summary:	Static ucil library
Summary(pl.UTF-8):	Statyczna biblioteka ucil
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static ucil library.

%description static -l pl.UTF-8
Statyczna biblioteka ucil.

%package apidocs
Summary:	ucil API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki ucil
Group:		Documentation
Requires:	gtk-doc-common
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for ucil library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki ucil.

%prep
%setup -q
%patch0 -p1

%build
# --enable-gpl allows to use some GPL gstreamer modules
# (doesn't affect libucil license, as it's GPLed anyway)
%{?with_ffmpeg:CPPFLAGS="%{rpmcppflags} -I/usr/include/libavcodec -I/usr/include/libavutil"}
%{__gettextize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-gpl \
	%{?with_ffmpeg:--enable-ucil-avcodec} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_libdir}/libucil.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libucil.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libucil.so
%{_libdir}/libucil.la
%{_includedir}/unicap/ucil*.h
%{_pkgconfigdir}/libucil.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libucil.a

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libucil
