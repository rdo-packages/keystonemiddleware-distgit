%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order flake8-docstrings pep8
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

License:        Apache-2.0
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


BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros

%description -n python3-%{sname}
%{common_desc}


%if 0%{?with_doc}
%package -n python-%{sname}-doc
Summary:    Documentation for the Middleware for OpenStack Identity
Group:      Documentation

BuildRequires:  python3-sphinxcontrib-rsvgconverter

%description -n python-%{sname}-doc
Documentation for the Middleware for OpenStack Identity
%endif


%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{sname}-%{upstream_version} -S git

# disable warning-is-error, this project has intersphinx in docs
# so some warnings are generated in network isolated build environment
# as koji
sed -i 's/^warning-is-error.*/warning-is-error = 0/g' setup.cfg

sed -i /.*-c{env:UPPER_CONSTRAINTS_FILE.*/d tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# doc8 is not shipped
sed -i '/[[:space:]]doc8.*/d' tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs};do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%if 0%{?with_doc}
# generate html docs
%tox -e docs
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif


%install
%pyproject_install
# Delete tests
rm -r %{buildroot}%{python3_sitelib}/%{sname}/tests


%files -n python3-%{sname}
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{sname}
%{python3_sitelib}/%{sname}-*.dist-info

%if 0%{?with_doc}
%files -n python-%{sname}-doc
%doc doc/build/html LICENSE
%endif

%changelog
