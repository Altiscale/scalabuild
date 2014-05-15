%define altiscale_release_ver ALTISCALE_RELEASE
%define rpm_package_name scala
%define scala_version SCALA_VERSION
%define build_service_name scala
%define scala_folder_name %{rpm_package_name}-%{scala_version}
%define install_scala_dest /opt/%{scala_folder_name}
# %define packager %(echo ${PKGER})
%define build_release BUILD_TIME

Name: %{rpm_package_name}
Summary: %{scala_folder_name} RPM wrapper.
Version: %{scala_version}
Release: %{altiscale_release_ver}.%{build_release}%{?dist}
License: http://www.scala-lang.org/license.html
# Packager: %{packager}
Group: Development/Tools
Source: %{_sourcedir}/%{build_service_name}-%{scala_version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%{build_service_name}
Provides: scala
%if 0%{?rhel}
Requires: jre7
%else
Requires: jre >= 1.7
%endif
# Apply all patches to fix CLASSPATH and java lib issues
# Patch1: %{_sourcedir}/patch.scala

Url: http://www.scala-lang.org/

%description
%{scala_folder_name} is a repackaged scala distro to support RPM package for other build process
that requires scala.

%prep
# copying files into BUILD/scala/ e.g. BUILD/scala/* 

# %patch1 -p0

%setup -q -n %{build_service_name}-%{scala_version}

%build
echo "ANT_HOME=$ANT_HOME"
echo "JAVA_HOME=$JAVA_HOME"
echo "MAVEN_HOME=$MAVEN_HOME"
echo "MAVEN_OPTS=$MAVEN_OPTS"
echo "M2_HOME=$M2_HOME"

echo "build - scala core in %{_builddir}/%{build_service_name}-%{scala_version}"
ls -al %{_builddir}/%{build_service_name}-%{scala_version}
#pushd `pwd`
#cd %{_builddir}/%{build_service_name}-%{scala_version}/
#popd
#echo "ok - Build scala Completed successfully!"

%install
# manual cleanup for compatibility, and to be safe if the %clean isn't implemented
rm -rf %{buildroot}%{install_scala_dest}
# re-create installed dest folders
mkdir -p %{buildroot}%{install_scala_dest}
echo "compiled/built folder is (not the same as buildroot) RPM_BUILD_DIR = %{_builddir}"
echo "test installtion folder (aka buildroot) is RPM_BUILD_ROOT = %{buildroot}"
echo "test install scala dest = %{buildroot}/%{install_scala_dest}"
echo "test install scala label scala_folder_name = %{scala_folder_name}"
%{__mkdir} -p %{buildroot}%{install_scala_dest}
cp -rp %{_builddir}/%{build_service_name}-%{scala_version} %{buildroot}%{install_scala_dest}

%clean
echo "ok - cleaning up temporary files, deleting %{buildroot}%{install_scala_dest}"
rm -rf %{buildroot}%{install_scala_dest}
rm -f %{buildroot}%{build_service_name}

%files
%defattr(0755,root,root,0755)
%{install_scala_dest}

%post
ln -sf %{install_scala_dest} /opt/%{build_service_name}

%postun
rm /opt/%{build_service_name}

%changelog
* Thu May 15 2014 Andrew Lee 20140515
- Added Group tag Development/Tools
* Wed May 14 2014 Andrew Lee 20140514
- Initial Creation of scala spec to build scala 2.10.3 RPM


