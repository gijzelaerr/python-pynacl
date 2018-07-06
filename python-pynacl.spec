%{?python_enable_dependency_generator}
%bcond_without check

%global modname pynacl

Name:           python-%{modname}
Version:        1.2.1
Release:        2%{?dist}
Summary:        Python binding to the Networking and Cryptography (NaCl) library

License:        ASL 2.0
URL:            https://github.com/pyca/pynacl
Source0:        %{url}/archive/%{version}/%{modname}-%{version}.tar.gz

BuildRequires:  libsodium-devel

%global _description \
PyNaCl is a Python binding to the Networking and Cryptography library,\
a crypto library with the stated goal of improving usability, security\
and speed.

%description %{_description}

%package -n python2-%{modname}
Summary:        %{summary}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python-cffi >= 1.4.1
%if %{with check}
BuildRequires:  python2-six
BuildRequires:  python2-pytest
BuildRequires:  python2-hypothesis
%endif

%description -n python2-%{modname} %{_description}

Python 2 version.

%prep
%autosetup -n %{modname}-%{version}
# Remove bundled libsodium, to be sure
rm -vrf src/libsodium/

# ARM and s390x is too slow for upstream tests
# See https://bugzilla.redhat.com/show_bug.cgi?id=1594901
# And https://github.com/pyca/pynacl/issues/370
%ifarch s390x %{arm}
sed -i 's/@settings(deadline=1500, max_examples=5)/@settings(deadline=4000, max_examples=5)/' tests/test_pwhash.py
%endif

%build
export SODIUM_INSTALL=system
%py2_build

%install
%py2_install

%if %{with check}
%check
PYTHONPATH=%{buildroot}%{python2_sitearch} py.test -v
%endif

%files -n python2-%{modname}
%license LICENSE
%doc README.rst
%{python2_sitearch}/PyNaCl-*.egg-info/
%{python2_sitearch}/nacl/

%changelog
* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.2.1-2
- Rebuilt for Python 3.7
- Prolong the deadline for tests on s390x
- Don't ignore the test results on arm, do the same as on s390x

* Tue Mar 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 02 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0

* Mon Oct 02 2017 Remi Collet <remi@fedoraproject.org> - 1.1.2-4
- rebuild for libsodium

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Apr 01 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.1.2-1
- Update to 1.1.2

* Thu Mar 16 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.1.1-1
- Update to 1.1.1

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 22 2016 Miro Hrončok <mhroncok@redhat.com> - 1.0.1-2
- Rebuild for Python 3.6

* Mon Dec 19 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.0.1-1
- Initial package
