# Created by pyp2rpm-1.1.0b
%global pypi_name keystonemiddleware

Name:           python-%{pypi_name}
Version:        1.1.1
Release:        1%{?dist}
Summary:        Middleware for OpenStack Identity

License:        ASL 2.0
URL:            http://launchpad.net/keystonemiddleware
Source0:        https://pypi.python.org/packages/source/k/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr

Requires: python-keystoneclient >= 0.10.0
# for s3 and ec2 token middlewares
Requires: python-webob


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
%setup -q -n %{pypi_name}-%{version}
# Let RPM handle the dependencies
rm -f requirements.txt
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# make doc build compatible with python-oslo-sphinx RPM
sed -i 's/oslosphinx/oslo.sphinx/' doc/source/conf.py

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
