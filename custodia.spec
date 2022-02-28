Name:           custodia
Version:        0.6.0
Release:        7
Summary:        A tool for managing secrets other processes
License:        GPLv3+
URL:            https://github.com/latchset/%{name}
Source0:        https://github.com/latchset/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz
Source2:        custodia.conf
Source3:        custodia@.service
Source4:        custodia@.socket
Source5:        custodia.tmpfiles.conf
BuildArch:      noarch

Patch0:		0001-fix-build-for-pytest.patch

BuildRequires:      systemd python3-devel python3-jwcrypto >= 0.4.2
BuildRequires:      python3-requests python3-setuptools > 18 python3-coverage
BuildRequires:      python3-pytest python3-docutils python3-systemd python3-virtualenv

Requires:           python3-custodia = %{version}-%{release}
Requires(preun):    systemd-units
Requires(postun):   systemd-units
Requires(post):     systemd-units

%description
A tool for managing secrets other processes

Custodia is a project that aims to define an API for modern cloud applications
that allows to easily store and share password,tokens,certificates and any
other secret in a way that keeps data secure, manageable and auditable.

Custodia is modular, the configuration file controls how authentication,
authorization, storage and API plugins are combined and exposed.

%package -n python3-custodia
Summary:    Sub-package with python3 custodia modules
%{?python_provide:%python_provide python3-%{name}}
Requires:   python3-jwcrypto >= 0.4.2 python3-requests python3-setuptools python3-systemd
Conflicts:  python3-custodia-extra < %{version}

%description -n python3-custodia
Sub-package with python custodia modules

Custodia is a project that aims to define an API for modern cloud applications
that allows to easily store and share password,tokens,certificates and any
other secret in a way that keeps data secure, manageable and auditable.

Custodia is modular, the configuration file controls how authentication,
authorization, storage and API plugins are combined and exposed.

%prep
%autosetup -n %{name}-%{version} -p1

%build
%py3_build

%check
export PIP_INDEX_URL=http://host.invalid./
export PIP_NO_DEPS=yes
export PIP_IGNORE_INSTALLED=yes


virtualenv --python=%{__python3} --system-site-packages testenv
source testenv/bin/activate
testenv/bin/pip install .
testenv/bin/python -m pytest --capture=no --strict --skip-servertests
deactivate 


%install
install -d %{buildroot}/%{_sbindir}
install -d  %{buildroot}/%{_mandir}/man7
install -d %{buildroot}/%{_defaultdocdir}/custodia
install -d %{buildroot}/%{_defaultdocdir}/custodia/examples
install -d %{buildroot}/%{_sysconfdir}/custodia
install -d %{buildroot}/%{_unitdir}
install -d %{buildroot}/%{_tmpfilesdir}
install -d %{buildroot}/%{_localstatedir}/lib/custodia
install -d %{buildroot}/%{_localstatedir}/log/custodia
install -d %{buildroot}/%{_localstatedir}/run/custodia

%py3_install
mv %{buildroot}/%{_bindir}/custodia %{buildroot}/%{_sbindir}/custodia
cp %{buildroot}/%{_sbindir}/custodia %{buildroot}/%{_sbindir}/custodia-3
cp %{buildroot}/%{_bindir}/custodia-cli %{buildroot}/%{_bindir}/custodia-cli-3

install -m 644 -t "%{buildroot}/%{_mandir}/man7" man/custodia.7
install -m 644 -t "%{buildroot}/%{_defaultdocdir}/custodia" README API.md
install -m 644 -t "%{buildroot}/%{_defaultdocdir}/custodia/examples" custodia.conf
install -m 600 %{SOURCE2} %{buildroot}%{_sysconfdir}/custodia
install -m 644 %{SOURCE3} %{SOURCE4} %{buildroot}%{_unitdir}
install -m 644 %{SOURCE5} %{buildroot}%{_tmpfilesdir}/custodia.conf

%pre
getent group custodia >/dev/null || groupadd -r custodia
getent passwd custodia >/dev/null || \
    useradd -r -g custodia -d / -s /sbin/nologin \
    -c "User for custodia" custodia
exit 0

%post
%systemd_post custodia@\*.socket
%systemd_post custodia@\*.service

%preun
%systemd_preun custodia@\*.socket
%systemd_preun custodia@\*.service

%postun
%systemd_postun custodia@\*.socket
%systemd_postun custodia@\*.service

%files
%doc README API.md LICENSE
%doc %{_defaultdocdir}/custodia/examples/custodia.conf
%{_mandir}/man7/custodia*
%{_sbindir}/custodia
%{_bindir}/custodia-cli
%dir %attr(0700,custodia,custodia) %{_sysconfdir}/custodia
%dir %attr(0700,custodia,custodia) %{_localstatedir}/lib/custodia
%dir %attr(0700,custodia,custodia) %{_localstatedir}/log/custodia
%dir %attr(0755,custodia,custodia) %{_localstatedir}/run/custodia
%config(noreplace) %attr(600,custodia,custodia) %{_sysconfdir}/custodia/custodia.conf
%attr(644,root,root)  %{_unitdir}/custodia@.socket
%attr(644,root,root)  %{_unitdir}/custodia@.service
%{_tmpfilesdir}/custodia.conf

%files -n python3-custodia
%doc LICENSE
%{_sbindir}/custodia-3
%{_bindir}/custodia-cli-3
%{python3_sitelib}/%{name}
%{python3_sitelib}/%{name}-%{version}-py%{python3_version}.egg-info
%{python3_sitelib}/%{name}-%{version}-py%{python3_version}-nspkg.pth

%changelog
* Mon Feb 28 2022 Jingwiw <ixoote@gmail.com> 0.6.0-7
- missing python-venv and replaced with python-virtualenv 
  only riscv64 tested

* Fri Jan 8 2021 baizhonggui <baizhonggui> 0.6.0-6
- Fix building for pytest 

* Fri May 15 2020 Captain Wei <captain.a.wei@gmail.com> 0.6.0-5
- Package init
