#!/bin/bash

curr_dir=`dirname $0`
curr_dir=`cd $curr_dir; pwd`

setup_host="$curr_dir/setup_host.sh"
scala_spec="$curr_dir/scala.spec"
mock_cfg="$curr_dir/altiscale-scala-centos-6-x86_64.cfg"
mock_cfg_name=$(basename "$mock_cfg")
mock_cfg_runtime=`echo $mock_cfg_name | sed "s/.cfg/.runtime.cfg/"`
scala_tgz="$curr_dir/scala.tgz"
scala_md5_file="$curr_dir/scala.md5"
scala_md5=""

if [ -f "$curr_dir/setup_env.sh" ]; then
  source "$curr_dir/setup_env.sh"
fi

if [ -f "$scala_md5_file" ]; then
  scala_md5=$(cat "$scala_md5_file" | grep -v "^#")
  echo "ok - scala md5 showing $scala_md5"
else
  echo "warn - $scala_md5_file not found, we will re-download from the source to build scala-${SCALA_VERSION}"
fi

if [ "x${WORKSPACE}" = "x" ] ; then
  WORKSPACE="$curr_dir/../"
fi

if [ ! -f "$curr_dir/setup_host.sh" ]; then
  echo "warn - $setup_host does not exist, we may not need this if all the libs and RPMs are pre-installed"
fi

if [ ! -e "$scala_spec" ] ; then
  echo "fail - missing $scala_spec file, can't continue, exiting"
  exit -9
fi

env | sort

echo "checking if scala is installed on the system"
# this chk can be smarter, however, the build script will re-download the scala libs again during build process
# we can save some build time if we can just re-use the pre-installed scala
chk_scala_rpm=$(rpm -qa *scala*)
if [ "x${chk_scala_rpm}" = "x" -o ! -d "${SCALA_HOME}" ] ; then
  echo "warn - SCALA_HOME may or may not be defined, however, $SCALA_HOME folder doesn't exist, re-validating $scala_tgz file or re-downloading scala and install scala temporarily"
  if [ -f "$scala_tgz" ] ; then
    echo "ok - found existing $scala_tgz, verifying integrity."
    fhash=$(md5sum "$scala_tgz" | cut -d" " -f1)
    if [ "x${fhash}" = "x${scala_md5}" ] ; then
      echo "ok - md5 hash $fhash matched, file is the same, no need to re-download again, use current one on disk"
    else
      echo "warn - previous file hash $fhash <> $scala_md5 , does not match , deleting and re-download again"
      echo "ok - deleting previous stale/corrupted file $scala_tgz"
      stat "$scala_tgz"
      rm -f "$scala_tgz"
      wget --output-document=$scala_tgz "http://www.scala-lang.org/files/archive/scala-${SCALA_VERSION}.tgz"
    fi
  else
    echo "ok - download fresh scala binaries ${SCALA_VERSION}"
    wget --output-document=$scala_tgz "http://www.scala-lang.org/files/archive/scala-${SCALA_VERSION}.tgz"
  fi
  tar xvf $scala_tgz
  if [ -d $WORKSPACE/scala-${SCALA_VERSION} ] ; then
    echo "deleting prev installed scala localtion $WORKSPACE/scala-${SCALA_VERSION}"
    rm -rf $WORKSPACE/scala-${SCALA_VERSION}
  fi
  mv scala-* $WORKSPACE/scala-${SCALA_VERSION}
  export SCALA_HOME=$WORKSPACE/scala-${SCALA_VERSION}
  echo "ok - scala update or re-downloaded completed, and put to $SCALA_HOME"
else
  echo "ok - detected installed scala, SCALA_HOME=$SCALA_HOME"
fi

echo "ok - tar zip source file, preparing for build/compile by rpmbuild"
# Looks like this is not installed on all machines
# rpmdev-setuptree
mkdir -p $WORKSPACE/rpmbuild/{BUILD,BUILDROOT,RPMS,SPECS,SOURCES,SRPMS}/
cp "$scala_spec" $WORKSPACE/rpmbuild/SPECS/scala.spec
cp -r $WORKSPACE/scala-${SCALA_VERSION} $WORKSPACE/rpmbuild/SOURCES/
pushd "$WORKSPACE/rpmbuild/SOURCES/"
tar --exclude .git -czf scala-${SCALA_VERSION}.tar.gz scala-${SCALA_VERSION}
popd

# The patches is no longer needed since we merge the results into a branch on github.
# cp $WORKSPACE/patches/* $WORKSPACE/rpmbuild/SOURCES/

echo "ok - applying version number $SCALA_VERSION and release number $BUILD_TIME, the pattern delimiter is / here"
sed -i "s/SCALA_VERSION/$SCALA_VERSION/g" "$WORKSPACE/rpmbuild/SPECS/scala.spec"
sed -i "s/BUILD_TIME/$BUILD_TIME/g" "$WORKSPACE/rpmbuild/SPECS/scala.spec"
sed -i "s/ALTISCALE_RELEASE/$ALTISCALE_RELEASE/g" "$WORKSPACE/rpmbuild/SPECS/scala.spec"
SCALA_HOME=$SCALA_HOME rpmbuild -vv -bs $WORKSPACE/rpmbuild/SPECS/scala.spec --define "_topdir $WORKSPACE/rpmbuild" --buildroot $WORKSPACE/rpmbuild/BUILDROOT/

if [ $? -ne "0" ] ; then
  echo "fail - RPM build failed"
  exit -98
fi

stat "$WORKSPACE/rpmbuild/SRPMS/scala-${SCALA_VERSION}-${ALTISCALE_RELEASE}.${BUILD_TIME}.el6.src.rpm"
rpm -ivvv "$WORKSPACE/rpmbuild/SRPMS/scala-${SCALA_VERSION}-${ALTISCALE_RELEASE}.${BUILD_TIME}.el6.src.rpm"

echo "ok - applying $WORKSPACE for the new BASEDIR for mock, pattern delimiter here should be :"
# the path includeds /, so we need a diff pattern delimiter

mkdir -p "$WORKSPACE/var/lib/mock"
chmod 2755 "$WORKSPACE/var/lib/mock"
mkdir -p "$WORKSPACE/var/cache/mock"
chmod 2755 "$WORKSPACE/var/cache/mock"
sed "s:BASEDIR:$WORKSPACE:g" "$mock_cfg" > "$mock_cfg_runtime"
echo "ok - applying mock config $mock_cfg_runtime"
cat "$mock_cfg_runtime"
mock -vvv --configdir=$curr_dir -r altiscale-scala-centos-6-x86_64.runtime --resultdir=$WORKSPACE/rpmbuild/RPMS/ --rebuild $WORKSPACE/rpmbuild/SRPMS/scala-${SCALA_VERSION}-${ALTISCALE_RELEASE}.${BUILD_TIME}.el6.src.rpm

if [ $? -ne "0" ] ; then
  echo "fail - mock RPM build failed"
  mock --configdir=$curr_dir -r altiscale-scala-centos-6-x86_64.runtime --clean
  mock --configdir=$curr_dir -r altiscale-scala-centos-6-x86_64.runtime --scrub=all
  exit -99
fi

mock --configdir=$curr_dir -r altiscale-scala-centos-6-x86_64.runtime --clean
mock --configdir=$curr_dir -r altiscale-scala-centos-6-x86_64.runtime --scrub=all

echo "ok - build Completed successfully!"

exit 0












