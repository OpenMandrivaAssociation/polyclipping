# The Clipper C++ crystallographic library already uses the name "clipper".
# The developer is fine with the choosen name.

# API monitoring
# http://upstream-tracker.org/versions/clipper.html

%define major   19
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Name:           polyclipping
Version:        6.2.1
Release:        1
Summary:        Polygon clipping library
Group:          Development/C++
License:        Boost
URL:            https://sourceforge.net/projects/polyclipping
Source0:        http://downloads.sourceforge.net/%{name}/clipper_ver%{version}.zip
BuildRequires:  cmake
BuildRequires:  dos2unix

%description
This library primarily performs the boolean clipping operations -
intersection, union, difference & xor - on 2D polygons. It also performs
polygon offsetting. The library handles complex (self-intersecting) polygons,
polygons with holes and polygons with overlapping co-linear edges.
Input polygons for clipping can use EvenOdd, NonZero, Positive and Negative
filling modes. The clipping code is based on the Vatti clipping algorithm,
and outperforms other clipping libraries.

%package -n     %{libname}
Summary:        %{summary}
Group:          System/Libraries
Provides:       %{name} = %{version}-%{release}


%description -n %{libname}
This library primarily performs the boolean clipping operations -
intersection, union, difference & xor - on 2D polygons. It also performs
polygon offsetting. The library handles complex (self-intersecting) polygons,
polygons with holes and polygons with overlapping co-linear edges.
Input polygons for clipping can use EvenOdd, NonZero, Positive and Negative
filling modes. The clipping code is based on the Vatti clipping algorithm,
and outperforms other clipping libraries.

%package -n     %{devname}
Summary:        Development files for %{name}
Group:          Development/C++
Requires:       %{libname} = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}


%description -n %{devname}
This package contains libraries and header files for developing applications
that use %{name}.


%prep
%setup -qc
%autopatch -p1

# Delete binaries
find . \( -name "*.exe" -o -name "*.dll" \) -delete

# Correct line ends and encodings
find . -type f -exec dos2unix -k {} \;

for filename in perl/perl_readme.txt README; do
  iconv -f iso8859-1 -t utf-8 "${filename}" > "${filename}".conv && \
    touch -r "${filename}" "${filename}".conv && \
    mv "${filename}".conv "${filename}"
done

# Enable use_lines
sed -i 's|^//#define use_lines$|#define use_lines|' cpp/clipper.hpp

%build
pushd cpp
# Use VERSION argument so that it's added to the pkgconfig file
  %cmake -DVERSION=%{version}
  %make
popd


%install
%makeinstall_std -C cpp/build
# from Fedora, but I can't see any need for this
# Install agg header with corrected include statement
# sed -e 's/\.\.\/clipper\.hpp/clipper.hpp/' < cpp/build/cpp_agg/agg_conv_clipper.h > %%{buildroot}%%{_includedir}/%%{name}/agg_conv_clipper.h

mv -f %{buildroot}%{_datadir}/pkgconfig/ %{buildroot}%{_libdir}/

%files -n       %{libname}
%{_libdir}/lib%{name}.so.%{major}*

%files -n       %{devname}
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
