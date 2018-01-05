%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global sname keystonemiddleware

%global with_doc 1

%if 0%{?fedora}
%global with_python3 1
%endif

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


%description
%{common_desc}

%package -n python2-%{sname}
Summary:        Middleware for OpenStack Identity

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr
BuildRequires:  git
# Required to generate sample config automatically in documentation
BuildRequires:  python-oslo-config
BuildRequires:  python-oslo-log
BuildRequires:  python-keystoneauth1
BuildRequires:  python-keystoneclient

Requires: python-keystoneclient >= 1:3.8.0
# for s3 and ec2 token middlewares
Requires: python-webob >= 1.7.1
Requires: python-keystoneauth1 >= 3.3.0
Requires: python-oslo-cache >= 1.26.0
Requires: python-oslo-config >= 2:5.1.0
Requires: python-oslo-context >= 2.19.2
Requires: python-oslo-i18n >= 3.15.3
Requires: python-oslo-log >= 3.30.0
Requires: python-oslo-serialization >= 2.18.0
Requires: python-oslo-utils >= 3.20.0
Requires: python-pbr >= 2.0.0
Requires: python-positional >= 1.1.1
Requires: python-pycadf >= 1.1.0
Requires: python-requests >= 2.14.2
Requires: python-six >= 1.10.0

%{?python_provide:%python_provide python2-%{sname}}

%description -n python2-%{sname}
%{common_desc}


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
Requires: python3-webob >= 1.7.1
Requires: python3-keystoneauth1 >= 3.3.0
Requires: python3-oslo-cache >= 1.26.0
Requires: python3-oslo-config >= 2:5.1.0
Requires: python3-oslo-context >= 2.19.2
Requires: python3-oslo-i18n >= 3.15.3
Requires: python3-oslo-log >= 3.30.0
Requires: python3-oslo-serialization >= 2.18.0
Requires: python3-oslo-utils >= 3.20.0
Requires: python3-pbr >= 2.0.0
Requires: python3-positional >= 1.1.1
Requires: python3-pycadf >= 1.1.0
Requires: python3-requests >= 2.14.2
Requires: python3-six >= 1.10.0

%{?python_provide:%python_provide python3-%{sname}}

%description -n python3-%{sname}
%{common_desc}
%endif


%if 0%{?with_doc}
%package doc
Summary:    Documentation for the Middleware for OpenStack Identity
Group:      Documentation

BuildRequires:  python-sphinx
BuildRequires:  python-openstackdocstheme
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-pycadf
BuildRequires:  python-oslotest
BuildRequires:  python-testresources
BuildRequires:  python-oslo-cache
BuildRequires:  python-oslo-messaging
BuildRequires:  python-requests-mock
BuildRequires:  python-webtest
BuildRequires:  openstack-macros

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
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%if 0%{?with_doc}
# generate html docs
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
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
%doc doc/build/html LICENSE
%endif

%changelog
