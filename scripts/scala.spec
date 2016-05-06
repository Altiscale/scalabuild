%define altiscale_release_ver ALTISCALE_RELEASE
%define rpm_package_name scala
%define scala_version SCALA_VERSION
%define build_service_name %{rpm_package_name}
%define scala_folder_name %{rpm_package_name}-%{scala_version}
%define install_scala_dest /opt
# %define packager %(echo ${PKGER})
%define build_release BUILD_TIME

Name:           %{rpm_package_name}
Version:        %{scala_version}
Release:        %{altiscale_release_ver}.%{build_release}%{?dist}
License:        BSD and http://www.scala-lang.org/license.html
Summary:        A hybrid functional/object-oriented language for the JVM
BuildArch:      noarch
Group:          Development/Languages
Source:         %{_sourcedir}/%{scala_folder_name}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%{build_service_name}
Provides:       scala
Url:            http://www.scala-lang.org/
# Requires: jre >= 1.7
# Apply all patches to fix CLASSPATH and java lib issues
# Patch1: %{_sourcedir}/patch.scala

%description
This %{scala_folder_name} is a repackaged scala distro to support RPM package for other build process
that requires scala. Scala itself is a general purpose programming language designed to express common
programming patterns in a concise, elegant, and type-safe way. It smoothly
integrates features of object-oriented and functional languages. It is also
fully interoperable with Java.

%prep
# copying files into BUILD/scala/ e.g. BUILD/scala/* 

# %patch1 -p0

%setup -q -n %{scala_folder_name}

%build
echo "ANT_HOME=$ANT_HOME"
echo "JAVA_HOME=$JAVA_HOME"
echo "MAVEN_HOME=$MAVEN_HOME"
echo "MAVEN_OPTS=$MAVEN_OPTS"
echo "M2_HOME=$M2_HOME"

echo "build - scala core in %{_builddir}/%{scala_folder_name}"
ls -al %{_builddir}/%{scala_folder_name}
#pushd `pwd`
#cd %{_builddir}/%{build_service_name}-%{scala_version}/
#popd
#echo "ok - Build scala Completed successfully!"

%install
# manual cleanup for compatibility, and to be safe if the %clean isn't implemented
rm -rf %{buildroot}%{install_scala_dest}/%{scala_folder_name}
# re-create installed dest folders
mkdir -p %{buildroot}%{install_scala_dest}
echo "compiled/built folder is (not the same as buildroot) RPM_BUILD_DIR = %{_builddir}"
echo "test installtion folder (aka buildroot) is RPM_BUILD_ROOT = %{buildroot}"
echo "test install scala dest = %{buildroot}/%{install_scala_dest}"
echo "man page dir = %{_mandir}"
echo "bin dir = %{_bindir}"
echo "java dir = %{_javadir}"
echo "data dir = %{_datadir}"
echo "test install scala label scala_folder_name = %{scala_folder_name}"
# Create dest BUILDROOT/opt/
%{__mkdir} -p %{buildroot}%{install_scala_dest}/
cp -rp %{_builddir}/%{scala_folder_name} %{buildroot}%{install_scala_dest}/

# Install to BUILDROOT/opt/scala-2.11.8/bin/
install -d %{buildroot}%{install_scala_dest}/%{scala_folder_name}/bin
for prog in scaladoc fsc scala scalac scalap; do
        install -p -m 755 bin/$prog %{buildroot}%{install_scala_dest}/%{scala_folder_name}/bin/
done
# Install man page to /usr/share/man/man1/
install -d %{buildroot}%{_mandir}/man1
install -p -m 644 %{_builddir}/%{scala_folder_name}/man/man1/* %{buildroot}%{_mandir}/man1

%clean
echo "ok - cleaning up temporary files, deleting %{buildroot}%{install_scala_dest}/%{scala_folder_name}"
rm -rf %{buildroot}%{install_scala_dest}/%{scala_folder_name}
echo "ok - removing symbolic link %{install_scala_dest}/%{scala_folder_name}"
rm -f %{buildroot}%{install_scala_dest}/%{build_service_name}

%files
%defattr(0755,root,root,0755)
%doc doc/{README,LICENSE.md}
%{install_scala_dest}/%{scala_folder_name}/
%{_mandir}/man1/*

%post
ln -sf %{install_scala_dest}/%{scala_folder_name} /opt/%{build_service_name}
ln -sf %{install_scala_dest}/%{scala_folder_name}/bin/scala %{_bindir}/scala
ln -sf %{install_scala_dest}/%{scala_folder_name}/bin/scaladoc %{_bindir}/scaladoc
ln -sf %{install_scala_dest}/%{scala_folder_name}/bin/fsc %{_bindir}/fsc
ln -sf %{install_scala_dest}/%{scala_folder_name}/bin/scalac %{_bindir}/scalac
ln -sf %{install_scala_dest}/%{scala_folder_name}/bin/scalap %{_bindir}/scalap

%postun
rm -f /opt/%{build_service_name}
rm -f %{_bindir}/scala
rm -f %{_bindir}/scaladoc
rm -f %{_bindir}/fsc
rm -f %{_bindir}/scalac
rm -f %{_bindir}/scalap

%changelog
* Thu May 5 2016 Andrew Lee 20160505
- Added version Scala 2.11.8
* Fri Nov 13 2015 Andrew Lee 20151113
- Added version Scala 2.10.5
* Mon May 19 2014 Andrew Lee 20140519
- Added version Scala 2.10.4
* Thu May 15 2014 Andrew Lee 20140515
- Install bin to /usr/bin, create symbolic llink in %post and %postun 
- Commented out Requires tag for java since the label is not consistent
* Thu May 15 2014 Andrew Lee 20140515
- Added Group tag Development/Tools
* Wed May 14 2014 Andrew Lee 20140514
- Initial Creation of scala spec to build scala 2.10.4 RPM


