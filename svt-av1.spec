%global __cmake_in_source_build 1
%global real_name SVT-AV1

Name:           svt-av1
Version:        0.9.0
Release:        1%{?dist}
Summary:        Scalable Video Technology for AV1 Encoder / Decoder
License:        Alliance for Open Media Patent License 1.0
URL:            https://gitlab.com/AOMediaCodec/%{real_name}

Source0:        %{url}/-/archive/v%{version}/%{real_name}-v%{version}.tar.bz2
# Build GStreamer plugin from tree directly
Patch0:         %{name}-gst.patch

BuildRequires:  cmake3
BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  pkgconfig(gstreamer-1.0) >= 1.13.1
BuildRequires:  pkgconfig(gstreamer-base-1.0) >= 1.13.1
BuildRequires:  pkgconfig(gstreamer-video-1.0) >= 1.13.1
BuildRequires:  yasm

ExclusiveArch:  x86_64

%description
The Scalable Video Technology for AV1 (SVT-AV1 Encoder and Decoder) is an AV1
compliant encoder/decoder library core. The SVT-AV1 encoder development is a
work-in-progress targeting performance levels applicable to both VOD and Live
encoding / transcoding video applications. The SVT-AV1 decoder implementation is
targeting future codec research activities.

%package        libs
Summary:        %{name} libraries

%description    libs
Scalable Video Technology for AV1 (SVT-AV1 Encoder and Decoder) libraries.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.

%package -n     gstreamer1-%{name}
Summary:        GStreamer 1.0 %{real_name} plug-in
Requires:       gstreamer1-plugins-base%{?_isa} >= 1.8

%description -n gstreamer1-%{name}
This package provides an %{real_name} based GStreamer plug-in.

%prep
%autosetup -p1 -n %{real_name}-v%{version}

%build
export LDFLAGS="%build_ldflags -Wl,-znoexecstack"

# Do not use 'Release' build or it hardcodes compiler settings:
%cmake3 -G Ninja -DCMAKE_BUILD_TYPE='Fedora'
%ninja_build

pushd gstreamer-plugin
export LIBRARY_PATH="$PWD/../Bin/Fedora:$LIBRARY_PATH"
%meson
%meson_build
popd

%install
%ninja_install
pushd gstreamer-plugin
%meson_install
popd

%files
%{_bindir}/SvtAv1DecApp
%{_bindir}/SvtAv1EncApp

%files libs
%license LICENSE.md
%doc README.md Docs
%{_libdir}/libSvtAv1Dec.so.0.8.7
%{_libdir}/libSvtAv1Dec.so.0
%{_libdir}/libSvtAv1Enc.so.%{version}
%{_libdir}/libSvtAv1Enc.so.0

%files devel
%{_includedir}/svt-av1
%{_libdir}/libSvtAv1Dec.so
%{_libdir}/libSvtAv1Enc.so
%{_libdir}/pkgconfig/SvtAv1Dec.pc
%{_libdir}/pkgconfig/SvtAv1Enc.pc

%files -n gstreamer1-%{name}
%{_libdir}/gstreamer-1.0/libgstsvtav1enc.so

%changelog
* Tue Jan 25 2022 Simone Caronni <negativo17@gmail.com> - 0.9.0-1
- Update to 0.9.0.

* Sat Jul 24 2021 Simone Caronni <negativo17@gmail.com> - 0.8.7-1
- Update to 0.8.7.

* Fri Apr 30 2021 Simone Caronni <negativo17@gmail.com> - 0.8.6-6
- Switch sources to Gitlab.

* Mon Mar 01 2021 Simone Caronni <negativo17@gmail.com> - 0.8.6-5
- Backport fixes from Fedora.
- Bump release to be newer than the official Fedora packages.

* Mon Dec 21 2020 Simone Caronni <negativo17@gmail.com> - 0.8.6-1
- Update to 0.8.6.

* Thu Nov 26 2020 Simone Caronni <negativo17@gmail.com> - 0.8.5-1
- First build, make it build also on CentOS/RHEL 7 with rebased GStreamer.
