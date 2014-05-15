scalabuild
==========

To build Scala 2.10.3 for CentOS 6.5 and for other Foundry app such as Spark.
This RPM is a wrapper around the tar ball version of Scala 2.10.3.
Integrity check is done by the build script, a copy is also checked into github.
NO MODIFICATION ALLOWED to the tar ball according to the license.
http://www.scala-lang.org/license.html

HOW TO
======
Just simply run the build.sh, it will build the SRPM and apply mock to build the final RPMs.
The tar ball is derived from:
http://www.scala-lang.org/files/archive/scala-2.10.3.tgz
