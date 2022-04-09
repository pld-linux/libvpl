#
# Conditional build:
%bcond_without	python3		# Python binding
#
Summary:	oneAPI Video Processing Library
Summary(pl.UTF-8):	Biblioteka przetwarzania obrazu oneAPI VPL
Name:		oneVPL
Version:	2022.0.0
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/oneapi-src/onevpl/releases
Source0:	https://github.com/oneapi-src/oneVPL/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	f812597060cfca4462071dc10fa37aa2
URL:		https://www.intel.com/content/www/us/en/developer/tools/oneapi/onevpl.html
BuildRequires:	cmake >= 3.10.2
BuildRequires:	libdrm-devel
BuildRequires:	libstdc++-devel >= 6:4.7
%{?with_python3:BuildRequires:	libstdc++-devel >= 6:7}
BuildRequires:	libva-devel >= 1.2
BuildRequires:	libva-drm-devel >= 1.2
BuildRequires:	pkgconfig
%{?with_python3:BuildRequires:	python3-devel >= 1:3.2}
%{?with_python3:BuildRequires:	python3-pybind11}
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	wayland-devel
BuildRequires:	xorg-lib-libpciaccess-devel
ExclusiveArch:	%{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The oneAPI Video Processing Library (oneVPL) provides a single video
processing API for encode, decode, and video processing that works
across a wide range of accelerators.

%description -l pl.UTF-8
Biblioteka przetwarzania obrazu oneAPI Video Processing Library
(oneVPL) udostępnia jedno API przetwarzania obrazu do kodowania,
dekodowania i przetwarzania działające na wielu różnych
akceleratorach.

%package devel
Summary:	Header files for oneVPL library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki oneVPL
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel >= 6:4.7

%description devel
Header files for oneVPL library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki oneVPL.

%package examples
Summary:	Example programs for oneVPL library
Summary(pl.UTF-8):	Przykładowe programy do biblioteki oneVPL
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description examples
Example programs for oneVPL library.

%description examples -l pl.UTF-8
Przykładowe programy do biblioteki oneVPL.

%package -n python3-oneVPL
Summary:	Python binding for oneVPL library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki oneVPL
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	libva >= 1.2
Requires:	libva-drm >= 1.2

%description -n python3-oneVPL
Python binding for oneVPL library.

%description -n python3-oneVPL -l pl.UTF-8
Wiązania Pythona do biblioteki oneVPL.

%prep
%setup -q

%build
install -d build
cd build
%cmake .. \
	%{?with_python3:-DBUILD_PYTHON_BINDING:BOOL=ON} \
	-DPYTHON_INSTALL_DIR:STRING=%{py3_sitedir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_docdir}/*.txt

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md third-party-programs.txt
%attr(755,root,root) %{_bindir}/decvpp_tool
%attr(755,root,root) %{_bindir}/vpl-inspect
%attr(755,root,root) %{_libdir}/libvpl.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libvpl.so.2
%dir %{_libdir}/oneVPL
%attr(755,root,root) %{_libdir}/oneVPL/libvpl_wayland.so
%dir %{_datadir}/oneVPL
%{_datadir}/oneVPL/env
%{_datadir}/oneVPL/modulefiles

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvpl.so
%{_includedir}/vpl
%{_libdir}/cmake/vpl
%{_pkgconfigdir}/vpl.pc

%files examples
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/hello-decode
%attr(755,root,root) %{_bindir}/hello-encode
%attr(755,root,root) %{_bindir}/hello-vpp
%attr(755,root,root) %{_bindir}/sample_decode
%attr(755,root,root) %{_bindir}/sample_encode
%attr(755,root,root) %{_bindir}/sample_multi_transcode
%attr(755,root,root) %{_bindir}/sample_vpp
%{_datadir}/oneVPL/examples

%if %{with python3}
%files -n python3-oneVPL
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/pyvpl.cpython-*.so
%endif
