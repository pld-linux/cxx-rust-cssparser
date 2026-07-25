#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	6.27
%define		qtver		5.15.2
%define		kfname		kidletime

Summary:	Library for parsing CSS
Summary(pl.UTF-8):	Biblioteka do parsowania CSS
Name:		cxx-rust-cssparser
Version:	1.0.0
Release:	2
License:	LGPL
Group:		Libraries
Source0:	https://download.kde.org/stable/cxx-rust-cssparser/%{name}-%{version}.tar.xz
# Source0-md5:	4302471a1d004501e8e1f5e8473befa0
Source1:	%{name}-vendor-crates-%{version}.tar.xz
# Source1-md5:	667d2488818fc2e04263e8da61936e80
Patch0:		use_corrosion_cxxbridge.patch
Patch1:		no_underscores.patch
URL:		https://www.kde.org/
BuildRequires:	cargo
BuildRequires:	cmake >= 3.22
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 2.004
BuildRequires:	rust
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A C++ library for parsing CSS that uses the Rust cssparser crate
internally.

%description -l pl.UTF-8
Biblioteka C++ do parsowania CSS, która używa wewnętrznie paczki Rust
cssparser.

%package devel
Summary:	Header files for %{name} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{name}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{name}.

%prep
%setup -q -b1
%patch -P0 -p1
%patch -P1 -p1
# Use our offline registry
export CARGO_HOME="$(pwd)/rust/.cargo"

mkdir -p "$CARGO_HOME"
cat >rust/.cargo/config.toml <<EOF
[source.crates-io]
replace-with = 'vendored-sources'

[source.vendored-sources]
directory = '$PWD/rust/vendor'
EOF

%build
export CARGO_HOME="$(pwd)/rust/.cargo"
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DUSE_CORROSION_CXXBRIDGE=OFF \
	-DRust_CARGO_TARGET=%cargo_target

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif

%install
rm -rf $RPM_BUILD_ROOT
export CARGO_HOME="$(pwd)/rust/.cargo"
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/cxx-rust-cssparser-parse
%ghost %{_libdir}/libcxx-rust-cssparser.so.1
%{_libdir}/libcxx-rust-cssparser.so.*.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/cxx-rust-cssparser
%{_libdir}/cmake/cxx-rust-cssparser
%{_libdir}/libcxx-rust-cssparser.so
