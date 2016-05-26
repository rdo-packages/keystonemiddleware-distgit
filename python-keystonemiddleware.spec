# Created by pyp2rpm-1.1.0b
%global pypi_name keystonemiddleware

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-%{pypi_name}
Version:        4.4.1
Release:        1%{?dist}
Summary:        Middleware for OpenStack Identity

License:        ASL 2.0
URL:            http://launchpad.net/keystonemiddleware
Source0:        https://pypi.python.org/packages/source/k/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr

Requires: python-keystoneclient >= 1:1.6.0
# for s3 and ec2 token middlewares
Requires: python-webob >= 1.2.3
Requires: python-keystoneauth1 >= 2.1.0
Requires: python-oslo-config >= 3.4.0
Requires: python-oslo-context >= 0.2.0
Requires: python-oslo-i18n >= 2.1.0
Requires: python-oslo-serialization >= 1.10.0
Requires: python-oslo-utils >= 3.4.0
Requires: python-pbr >= 1.6
Requires: python-positional >= 1.0.1
Requires: python-pycadf >= 1.1.0
Requires: python-requests >= 2.8.1
Requires: python-six >= 1.9.0


%description
This package contains middleware modules designed to provide authentication
and authorization features to web services other than OpenStack Keystone.
The most prominent module is keystonemiddleware.auth_token.
This package does not expose any CLI or Python API features.

%package doc
Summary:    Documentation for the Middleware for OpenStack Identity
Group:      Documentation

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx

%description doc
Documentation for the Middleware for OpenStack Identity


%prep
%setup -q -n %{pypi_name}-%{upstream_version}
# Let RPM handle the dependencies
rm -f requirements.txt
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%{__python2} setup.py build

# generate html docs
export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}


%install
%{__python2} setup.py install --skip-build --root %{buildroot}

# Delete tests
rm -r %{buildroot}%{python2_sitelib}/%{pypi_name}/tests


%files
%doc README.rst LICENSE
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-*.egg-info

%files doc
%doc html LICENSE

%changelog
* Thu May 26 2016 Haikel Guemar <hguemar@fedoraproject.org> 4.4.1-1
- Update to 4.4.1

* Wed Mar 23 2016 Haikel Guemar <hguemar@fedoraproject.org> 4.3.0-
- Update to 4.3.0

* Fri Sep 26 2014 Alan Pevec <alan.pevec@redhat.com> 1.2.0-1
- Update to upstream 1.2.0

* Wed Aug 27 2014 Alan Pevec <apevec@redhat.com> 1.1.1-1
- Update to upstream 1.1.1

* Mon Aug 04 2014 Alan Pevec <apevec@redhat.com> - 1.0.0-4
- move docs to -doc subpackage
- drop tests from the runtime package

* Wed Jul 30 2014 Alan Pevec <apevec@redhat.com> - 1.0.0-2
- add build dep on setuptools
- fix docs build
- clear requires from egginfo to let RPM handle the dependencies

* Sun Jul 27 2014 Alan Pevec <apevec@redhat.com> - 1.0.0-1
- Initial package.
