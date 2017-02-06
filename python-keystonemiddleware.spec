%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global sname keystonemiddleware

%global with_doc 1

%if 0%{?fedora}
%global with_python3 1
%endif

Name:           python-%{sname}
Version:        XXX
Release:        XXX
Summary:        Middleware for OpenStack Identity

License:        ASL 2.0
URL:            http://launchpad.net/keystonemiddleware
Source0:        https://tarballs.openstack.org/%{sname}/%{sname}-%{version}.tar.gz
BuildArch:      noarch


%description
This package contains middleware modules designed to provide authentication
and authorization features to web services other than OpenStack Keystone.
The most prominent module is keystonemiddleware.auth_token.
This package does not expose any CLI or Python API features.

%package -n python2-%{sname}
Summary:        Middleware for OpenStack Identity

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr
# Required to generate sample config automatically in documentation
BuildRequires:  python-oslo-config
BuildRequires:  python-oslo-log
BuildRequires:  python-keystoneauth1
BuildRequires:  python-keystoneclient

Requires: python-keystoneclient >= 1:3.8.0
# for s3 and ec2 token middlewares
Requires: python-webob >= 1.6.0
Requires: python-keystoneauth1 >= 2.18.0
Requires: python-oslo-config >= 2:3.14.0
Requires: python-oslo-context >= 2.9.0
Requires: python-oslo-i18n >= 2.1.0
Requires: python-oslo-log >= 3.11.0
Requires: python-oslo-serialization >= 1.10.0
Requires: python-oslo-utils >= 3.18.0
Requires: python-pbr >= 1.8
Requires: python-positional >= 1.1.1
Requires: python-pycadf >= 1.1.0
Requires: python-requests >= 2.10.0
Requires: python-six >= 1.9.0

%{?python_provide:%python_provide python2-%{sname}}

%description -n python2-%{sname}
This package contains middleware modules designed to provide authentication
and authorization features to web services other than OpenStack Keystone.
The most prominent module is keystonemiddleware.auth_token.
This package does not expose any CLI or Python API features.


%if 0%{?with_python3}
%package -n python3-%{sname}
Summary:        Middleware for OpenStack Identity

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr
BuildRequires:  python3-oslo-config
BuildRequires:  python3-oslo-log
BuildRequires:  python3-keystoneauth1
BuildRequires:  python3-keystoneclient

Requires: python3-keystoneclient >= 1:3.8.0
# for s3 and ec2 token middlewares
Requires: python3-webob >= 1.6.0
Requires: python3-keystoneauth1 >= 2.18.0
Requires: python3-oslo-config >= 2:3.14.0
Requires: python3-oslo-context >= 2.9.0
Requires: python3-oslo-i18n >= 2.1.0
Requires: python3-oslo-log >= 3.11.0
Requires: python3-oslo-serialization >= 1.10.0
Requires: python3-oslo-utils >= 3.18.0
Requires: python3-pbr >= 1.8
Requires: python3-positional >= 1.1.1
Requires: python3-pycadf >= 1.1.0
Requires: python3-requests >= 2.10.0
Requires: python3-six >= 1.9.0

%{?python_provide:%python_provide python3-%{sname}}

%description -n python3-%{sname}
This package contains middleware modules designed to provide authentication
and authorization features to web services other than OpenStack Keystone.
The most prominent module is keystonemiddleware.auth_token.
This package does not expose any CLI or Python API features.
%endif


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
%setup -q -n %{sname}-%{upstream_version}
# Let RPM handle the dependencies
rm -f requirements.txt
# Remove bundled egg-info
rm -rf %{sname}.egg-info

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%if 0%{?with_doc}
# generate html docs
export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
%endif


%install
%if 0%{?with_python3}
%py3_install
# Delete tests
rm -r %{buildroot}%{python3_sitelib}/%{sname}/tests
%endif

%py2_install
# Delete tests
rm -r %{buildroot}%{python2_sitelib}/%{sname}/tests


%files -n python2-%{sname}
%doc README.rst
%license LICENSE
%{python2_sitelib}/%{sname}
%{python2_sitelib}/%{sname}-*.egg-info

%if 0%{?with_python3}
%files -n python3-%{sname}
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{sname}
%{python3_sitelib}/%{sname}-*.egg-info
%endif


%if 0%{?with_doc}
%files doc
%doc html LICENSE
%endif

%changelog
