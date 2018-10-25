# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global sname keystonemiddleware

%global with_doc 1

%global common_desc \
This package contains middleware modules designed to provide authentication \
and authorization features to web services other than OpenStack Keystone. \
The most prominent module is keystonemiddleware.auth_token. \
This package does not expose any CLI or Python API features.

Name:           python-%{sname}
Version:        XXX
Release:        XXX
Summary:        Middleware for OpenStack Identity

License:        ASL 2.0
URL:            http://launchpad.net/keystonemiddleware
Source0:        https://tarballs.openstack.org/%{sname}/%{sname}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  git
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n python%{pyver}-%{sname}
Summary:        Middleware for OpenStack Identity
%{?python_provide:%python_provide python%{pyver}-%{sname}}

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-pbr
# Required to generate sample config automatically in documentation
BuildRequires:  python%{pyver}-oslo-config
BuildRequires:  python%{pyver}-oslo-log
BuildRequires:  python%{pyver}-keystoneauth1
BuildRequires:  python%{pyver}-keystoneclient
BuildRequires:  python%{pyver}-oslo-cache

Requires: python%{pyver}-keystoneclient >= 1:3.8.0
# for s3 and ec2 token middlewares
Requires: python%{pyver}-keystoneauth1 >= 3.4.0
Requires: python%{pyver}-oslo-config >= 2:5.2.0
Requires: python%{pyver}-oslo-context >= 2.19.2
Requires: python%{pyver}-oslo-i18n >= 3.15.3
Requires: python%{pyver}-oslo-log >= 3.36.0
Requires: python%{pyver}-oslo-serialization >= 2.18.0
Requires: python%{pyver}-oslo-utils >= 3.33.0
Requires: python%{pyver}-pbr >= 2.0.0
Requires: python%{pyver}-pycadf >= 1.1.0
Requires: python%{pyver}-requests >= 2.14.2
Requires: python%{pyver}-six >= 1.10.0
Requires: python%{pyver}-oslo-cache >= 1.26.0
Requires: python%{pyver}-webob >= 1.7.1

%if %{pyver} == 2
BuildRequires:  python-testresources
BuildRequires:  python-requests-mock
BuildRequires:  python-webtest
%else
BuildRequires:  python%{pyver}-testresources
BuildRequires:  python%{pyver}-requests-mock
BuildRequires:  python%{pyver}-webtest
%endif

%description -n python%{pyver}-%{sname}
%{common_desc}


%if 0%{?with_doc}
%package doc
Summary:    Documentation for the Middleware for OpenStack Identity
Group:      Documentation

BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-openstackdocstheme
BuildRequires:  python%{pyver}-oslo-sphinx
BuildRequires:  python%{pyver}-pycadf
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-oslo-messaging
BuildRequires:  python%{pyver}-sphinxcontrib-apidoc
# Handle python2 exception
%if %{pyver} == 2
BuildRequires:  python-testresources
BuildRequires:  python-requests-mock
BuildRequires:  python-webtest
%else
BuildRequires:  python%{pyver}-testresources
BuildRequires:  python%{pyver}-requests-mock
BuildRequires:  python%{pyver}-webtest
%endif

%description doc
Documentation for the Middleware for OpenStack Identity
%endif


%prep
%autosetup -n %{sname}-%{upstream_version} -S git
# Let RPM handle the dependencies
%py_req_cleanup
# Remove bundled egg-info
rm -rf %{sname}.egg-info

# disable warning-is-error, this project has intersphinx in docs
# so some warnings are generated in network isolated build environment
# as koji
sed -i 's/^warning-is-error.*/warning-is-error = 0/g' setup.cfg

%build
%{pyver_build}

%if 0%{?with_doc}
# generate html docs
sphinx-build-%{pyver} -b html doc/source doc/build/html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}
# Delete tests
rm -r %{buildroot}%{pyver_sitelib}/%{sname}/tests


%files -n python%{pyver}-%{sname}
%doc README.rst
%license LICENSE
%{pyver_sitelib}/%{sname}
%{pyver_sitelib}/%{sname}-*.egg-info

%if 0%{?with_doc}
%files doc
%doc doc/build/html LICENSE
%endif

%changelog
