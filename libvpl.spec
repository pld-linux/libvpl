# TODO: OpenCL (-DTOOLS_ENABLE_OPENCL=ON)?
Summary:	Intel Video Processing Library
Summary(pl.UTF-8):	Biblioteka przetwarzania obrazu Intel VPL
Name:		libvpl
Version:	2.10.2
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/intel/libvpl/releases
Source0:	https://github.com/intel/libvpl/archive/v%{version}/libvpl-%{version}.tar.gz
# Source0-md5:	09d6347097590abd3e952619f5ed6316
Patch0:		%{name}-types.patch
URL:		https://www.intel.com/content/www/us/en/developer/tools/vpl/overview.html
BuildRequires:	cmake >= 3.13.0
BuildRequires:	libdrm-devel
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libva-devel >= 1.2
BuildRequires:	libva-drm-devel >= 1.2
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	wayland-devel
BuildRequires:	xorg-lib-libpciaccess-devel
Obsoletes:	oneVPL < 2024
Obsoletes:	python3-oneVPL < 2023
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Intel Video Processing Library (Intel VPL) provides a single video
processing API for encode, decode, and video processing that works
across a wide range of accelerators.

%description -l pl.UTF-8
Biblioteka przetwarzania obrazu Intel Video Processing Library
(Intel VPL) udostępnia jedno API przetwarzania obrazu do kodowania,
dekodowania i przetwarzania działające na wielu różnych
akceleratorach.

%package devel
Summary:	Header files for Intel VPL library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Intel VPL
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel >= 6:4.7
Obsoletes:	oneVPL < 2024

%description devel
Header files for Intel VPL library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Intel VPL.

%package examples
Summary:	Example programs for Intel VPL library
Summary(pl.UTF-8):	Przykładowe programy do biblioteki Intel VPL
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	oneVPL-examples < 2024

%description examples
Example programs for Intel VPL library.

%description examples -l pl.UTF-8
Przykładowe programy do biblioteki Intel VPL.

%prep
%setup -q -n libvpl-%{version}
%patch0 -p1

%build
%cmake -B build

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}
%{__mv} $RPM_BUILD_ROOT%{_datadir}/vpl/examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/vpl/licensing

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md LICENSE README.md SECURITY.md third-party-programs.txt
%attr(755,root,root) %{_bindir}/val-surface-sharing
%attr(755,root,root) %{_bindir}/vpl-import-export
%attr(755,root,root) %{_bindir}/vpl-inspect
%attr(755,root,root) %{_libdir}/libvpl.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libvpl.so.2
%dir %{_libdir}/vpl
%attr(755,root,root) %{_libdir}/vpl/libvpl_wayland.so
%dir %{_sysconfdir}/vpl
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/vpl/vars.sh

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvpl.so
%{_includedir}/vpl
%{_libdir}/cmake/vpl
%{_pkgconfigdir}/vpl.pc

%files examples
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/sample_decode
%attr(755,root,root) %{_bindir}/sample_encode
%attr(755,root,root) %{_bindir}/sample_multi_transcode
%attr(755,root,root) %{_bindir}/sample_vpp
%attr(755,root,root) %{_bindir}/system_analyzer
%{_examplesdir}/%{name}-%{version}
