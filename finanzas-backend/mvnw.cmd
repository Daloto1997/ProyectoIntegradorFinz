@echo off
setlocal

set BASEDIR=%~dp0
set WRAPPER_JAR=%BASEDIR%.mvn\wrapper\maven-wrapper.jar

java -classpath "%WRAPPER_JAR%" "-Dmaven.multiModuleProjectDirectory=%BASEDIR:~0,-1%" org.apache.maven.wrapper.MavenWrapperMain %*

endlocal
