# Created by pyp2rpm-1.1.0b
%global pypi_name keystonemiddleware

Name:           python-%{pypi_name}
Version:        1.0.0
Release:        3%{?dist}
Summary:        Middleware for OpenStack Identity

License:        ASL 2.0
URL:            http://launchpad.net/keystonemiddleware
Source0:        https://pypi.python.org/packages/source/k/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr

Requires: python-keystoneclient >= 0.9.0


%description
This package contains middleware modules designed to provide authentication
and authorization features to web services other than OpenStack Keystone.
The most prominent module is keystonemiddleware.auth_token.
This package does not expose any CLI or Python API features.

%package doc
Summary:    Documentation for the Middleware for OpenStack Identity
Group:      Documentation

BuildRequires:  python-sphinx

%description doc
Documentation for the Middleware for OpenStack Identity


%prep
%setup -q -n %{pypi_name}-%{version}
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
rm -r %{buildroot}%{python_sitelib}/%{pypi_name}/tests


%files
%doc README.rst LICENSE
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%files doc
%doc html LICENSE

%changelog
* Mon Aug 04 2014 Alan Pevec <apevec@redhat.com> - 1.0.0-3
- move docs to -doc subpackage
- drop tests from the runtime package

* Wed Jul 30 2014 Alan Pevec <apevec@redhat.com> - 1.0.0-2
- add build dep on setuptools
- fix docs build
- clear requires from egginfo to let RPM handle the dependencies

* Sun Jul 27 2014 Alan Pevec <apevec@redhat.com> - 1.0.0-1
- Initial package.
