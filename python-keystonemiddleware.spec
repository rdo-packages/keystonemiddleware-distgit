# Created by pyp2rpm-1.1.0b
%global pypi_name keystonemiddleware

%bcond_without doc

Name:           python-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        Middleware for OpenStack Identity

License:        ASL 2.0
URL:            http://launchpad.net/keystonemiddleware
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr
# Required to generate sample config automatically in documentation
BuildRequires:  python-oslo-config
BuildRequires:  python-keystoneauth1
BuildRequires:  python-keystoneclient

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

%if 0%{?with_doc}
%package doc
Summary:    Documentation for the Middleware for OpenStack Identity
Group:      Documentation

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx

%description doc
Documentation for the Middleware for OpenStack Identity
%endif


%prep
%setup -q -n %{pypi_name}-%{upstream_version}
# Let RPM handle the dependencies
rm -f requirements.txt
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%{__python2} setup.py build

%if 0%{?with_doc}
# generate html docs
export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
%endif


%install
%{__python2} setup.py install --skip-build --root %{buildroot}

# Delete tests
rm -r %{buildroot}%{python2_sitelib}/%{pypi_name}/tests


%files
%doc README.rst
%license LICENSE
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-*.egg-info

%if 0%{?with_doc}
%files doc
%doc html LICENSE
%endif

%changelog
