%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a

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
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{sname}/%{sname}-%{version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:  git-core
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n python3-%{sname}
Summary:        Middleware for OpenStack Identity
%{?python_provide:%python_provide python3-%{sname}}


BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr
# Required to generate sample config automatically in documentation
BuildRequires:  python3-oslo-config
BuildRequires:  python3-oslo-log
BuildRequires:  python3-keystoneauth1
BuildRequires:  python3-keystoneclient
BuildRequires:  python3-oslo-cache

Requires: python3-keystoneclient >= 1:3.20.0
# for s3 and ec2 token middlewares
Requires: python3-keystoneauth1 >= 3.12.0
Requires: python3-oslo-config >= 2:5.2.0
Requires: python3-oslo-context >= 2.19.2
Requires: python3-oslo-i18n >= 3.15.3
Requires: python3-oslo-log >= 3.36.0
Requires: python3-oslo-serialization >= 2.18.0
Requires: python3-oslo-utils >= 3.33.0
Requires: python3-pbr >= 2.0.0
Requires: python3-pycadf >= 1.1.0
Requires: python3-requests >= 2.14.2
Requires: python3-six >= 1.10.0
Requires: python3-oslo-cache >= 1.26.0
Requires: python3-webob >= 1.7.1

%description -n python3-%{sname}
%{common_desc}


%if 0%{?with_doc}
%package -n python-%{sname}-doc
Summary:    Documentation for the Middleware for OpenStack Identity
Group:      Documentation

BuildRequires:  python3-sphinx
BuildRequires:  python3-openstackdocstheme
BuildRequires:  python3-pycadf
BuildRequires:  python3-oslotest
BuildRequires:  python3-oslo-messaging
BuildRequires:  python3-sphinxcontrib-apidoc
BuildRequires:  python3-sphinxcontrib-rsvgconverter
BuildRequires:  python3-requests-mock
BuildRequires:  python3-testresources
BuildRequires:  python3-webtest

%description -n python-%{sname}-doc
Documentation for the Middleware for OpenStack Identity
%endif


%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
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
%{py3_build}

%if 0%{?with_doc}
# generate html docs
sphinx-build-3 -b html doc/source doc/build/html
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif


%install
%{py3_install}
# Delete tests
rm -r %{buildroot}%{python3_sitelib}/%{sname}/tests


%files -n python3-%{sname}
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{sname}
%{python3_sitelib}/%{sname}-*.egg-info

%if 0%{?with_doc}
%files -n python-%{sname}-doc
%doc doc/build/html LICENSE
%endif

%changelog
