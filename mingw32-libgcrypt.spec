%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

%define run_tests 0

Name:           mingw32-libgcrypt
Version:        1.4.4
Release:        4%{?dist}.4
Summary:        MinGW Windows gcrypt encryption library


License:        LGPLv2+ and GPLv2+
Group:          Development/Libraries

URL:            ftp://ftp.gnupg.org/gcrypt/libgcrypt/
# The original libgcrypt sources now contain potentially patented ECC
# cipher support. We have to remove it in the tarball we ship with
# the hobble-libgcrypt script.
Source0:        ftp://ftp.gnupg.org/gcrypt/libgcrypt/libgcrypt-%{version}.tar.bz2
Source1:        ftp://ftp.gnupg.org/gcrypt/libgcrypt/libgcrypt-%{version}.tar.bz2.sig
Source2:        wk@g10code.com
Source3:        hobble-libgcrypt

Patch1:         libgcrypt-1.4.4-fips-no-access.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 49
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-libgpg-error
BuildRequires:  mingw32-dlfcn

%if %run_tests
BuildRequires:  wine
%endif


%description
Libgcrypt is a general purpose crypto library based on the code used
in GNU Privacy Guard.

This is a Windows cross-compiled version of the library.


%prep
%setup -q -n libgcrypt-%{version}
%{SOURCE3}
%patch1 -p1 -b .no-access


%build
%{_mingw32_configure} \
  --disable-static \
  --enable-pubkey-ciphers='dsa elgamal rsa'
make %{?_smp_mflags}


%check
%if %run_tests
# Stupid Wine doesn't load DLLs from the PATH any
# more, so libtool scripts don't work.  As a result
# we need to use the following Big Hack.
make -C tests check ||:
pushd src/.libs
for t in $(pwd)/../../tests/*.exe; do
  wine $t
done
popd
%endif


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

# Remove info pages which duplicate what is in Fedora natively.
rm -rf $RPM_BUILD_ROOT%{_mingw32_infodir}

rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libgcrypt.def


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc COPYING COPYING.LIB
%{_mingw32_bindir}/dumpsexp.exe
%{_mingw32_bindir}/hmac256.exe
%{_mingw32_bindir}/libgcrypt-11.dll
%{_mingw32_bindir}/libgcrypt-config
%{_mingw32_libdir}/libgcrypt.dll.a
%{_mingw32_libdir}/libgcrypt.la
%{_mingw32_includedir}/gcrypt-module.h
%{_mingw32_includedir}/gcrypt.h
%{_mingw32_datadir}/aclocal/libgcrypt.m4


%changelog
* Tue Dec 28 2010 Andrew Beekhof <abeekhof@redhat.com> - 1.4.4-4.4
- Rebuild everything with gcc-4.4
  Related: rhbz#658833

* Fri Dec 24 2010 Andrew Beekhof <abeekhof@redhat.com> - 1.4.4-4.3
- The use of ExclusiveArch conflicts with noarch, using an alternate COLLECTION to limit builds
  Related: rhbz#658833

* Wed Dec 22 2010 Andrew Beekhof <abeekhof@redhat.com> - 1.4.4-4.2
- Only build mingw packages on x86_64
  Related: rhbz#658833

* Wed Dec 22 2010 Andrew Beekhof <abeekhof@redhat.com> - 1.4.4-4.1
- Bump the revision to avoid tag collision
  Related: rhbz#658833

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 1.4.4-2
- Rebuild for mingw32-gcc 4.4

* Fri Feb  6 2009 Richard W.M. Jones <rjones@redhat.com> - 1.4.4-1
- Update to Fedora native version 1.4.4:
  . Remove potentially patented ECC support.
  . Do not abort when the fips mode kernel flag is inaccessible
    due to permissions (#470219).
- For review (Michel Alexandre Salim):
  . Remove *.def file.
  . Make description clearer.
  . Distribute the license files.
- The license for binaries is GPLv2+, so update the license field.
- Add check section (disabled by default).
- Why did we set PATH before configure? Removed.
- Added BR mingw32-dlfcn suggested by auto-buildrequires.

* Fri Jan 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.4.3-3
- Use _smp_mflags.
- Disable static libraries.

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 1.4.3-2
- Rename mingw -> mingw32.

* Mon Sep 22 2008 Daniel P. Berrange <berrange@redhat.com> - 1.4.3-1
- Update to 1.4.3 release

* Sun Sep 21 2008 Richard W.M. Jones <rjones@redhat.com> - 1.4.1-6
- Remove info pages.

* Thu Sep 11 2008 Daniel P. Berrange <berrange@redhat.com> - 1.4.1-5
- Set PATH so it finds gpg-error-config

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 1.4.1-4
- Remove static library.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 1.4.1-3
- Use RPM macros from mingw-filesystem.

* Tue Sep  2 2008 Daniel P. Berrange <berrange@redhat.com> - 1.4.1-2
- List files explicitly and use custom CFLAGS

* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 1.4.1-1
- Initial RPM release, largely based on earlier work from several sources.
