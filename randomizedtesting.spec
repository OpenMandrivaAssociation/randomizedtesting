Name:		randomizedtesting
Version:	2.9.2
Release:	1
Summary:	Randomized JUnit 4 runner
Group:		Development/Java
License:	ASL 2.0
URL:		https://github.com/carrotsearch/randomizedtesting
Source0:	https://github.com/carrotsearch/randomizedtesting/archive/refs/tags/release/%{version}.tar.gz#/randomizedtesting-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	python
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildRequires:	mvn(junit:junit)
# AssumptionViolatedException's signature references org.hamcrest.Matcher.
BuildRequires:	mvn(org.hamcrest:hamcrest-core)
BuildSystem:	maven
BuildOption(install):	--file-name randomizedtesting-runner

Obsoletes:	%{name}-runner < %{version}-%{release}
Obsoletes:	%{name}-junit4-ant < %{version}-%{release}
Obsoletes:	%{name}-junit4-maven-plugin < %{version}-%{release}
Obsoletes:	%{name}-javadoc < %{version}-%{release}

%description
RandomizedTesting adds randomization, reproducible seeds, and
lifecycle rules on top of JUnit 4. 2.9.2 is the current release.
Since 2.1.3 it ignores CompletableFuture delay threads, can format
test names with square brackets for Gradle and IntelliJ, and runs on
current Java releases. This package ships the runner. The Ant task
and the Maven plugin are left out: the Ant task vendors native crash
libraries and simple-xml-safe. The compiler release is 8. Tests are
skipped.

%prep
%autosetup -n randomizedtesting-release-%{version}
rm -rf junit4-ant junit4-maven-plugin junit4-maven-plugin-tests examples
find . -name '*.jar' -delete
find . \( -name '*.so' -o -name '*.dll' -o -name '*.dylib' -o -name '*.class' \) -delete
python - <<'PY'
from pathlib import Path

for rel in ("junit4-ant", "junit4-maven-plugin", "junit4-maven-plugin-tests", "examples"):
    if Path(rel).exists():
        raise SystemExit(rel + " remains")
java_files = list(Path("randomized-runner/src/main/java").rglob("*.java"))
if len(java_files) != 92:
    raise SystemExit("java files " + str(len(java_files)))
if list(Path(".").rglob("*.jar")) or list(Path(".").rglob("*.so")) or list(Path(".").rglob("*.dll")):
    raise SystemExit("prebuilt binary remains")
for pom in Path(".").rglob("pom.xml"):
    pom.unlink()

Path("pom.xml").write_text("""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.carrotsearch.randomizedtesting</groupId>
  <artifactId>randomizedtesting-runner</artifactId>
  <version>%{version}</version>
  <packaging>jar</packaging>
  <name>RandomizedTesting runner</name>
  <description>JUnit 4 runner with reproducible randomization.</description>
  <url>https://github.com/carrotsearch/randomizedtesting</url>
  <licenses>
    <license>
      <name>Apache License, Version 2.0</name>
      <url>https://www.apache.org/licenses/LICENSE-2.0.txt</url>
    </license>
  </licenses>
  <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <maven.compiler.release>8</maven.compiler.release>
  </properties>
  <dependencies>
    <dependency>
      <groupId>junit</groupId>
      <artifactId>junit</artifactId>
      <version>4.13.2</version>
    </dependency>
    <dependency>
      <groupId>org.hamcrest</groupId>
      <artifactId>hamcrest-core</artifactId>
      <version>3.0</version>
    </dependency>
  </dependencies>
  <build>
    <sourceDirectory>randomized-runner/src/main/java</sourceDirectory>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.12.1</version>
        <configuration>
          <release>8</release>
        </configuration>
      </plugin>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-jar-plugin</artifactId>
        <version>3.3.0</version>
      </plugin>
    </plugins>
  </build>
</project>
""", encoding="utf-8")
pom = Path("pom.xml").read_text(encoding="utf-8")
poms = sorted(str(path) for path in Path(".").rglob("pom.xml"))
if poms != ["pom.xml"]:
    raise SystemExit("poms " + str(poms))
for needle in (
    "<artifactId>randomizedtesting-runner</artifactId>",
    "<artifactId>junit</artifactId>",
    "<artifactId>hamcrest-core</artifactId>",
    "<version>4.13.2</version>",
    "<version>3.0</version>",
    "<version>%{version}</version>",
    "<release>8</release>",
    "<sourceDirectory>randomized-runner/src/main/java</sourceDirectory>",
):
    if needle not in pom:
        raise SystemExit("pom missing " + needle)
for needle in ("assertj", "guava", "simple-xml", "proguard", "SNAPSHOT", "<source>", "<target>", "<parent>", "ant"):
    if needle in pom:
        raise SystemExit("pom still contains " + needle)
PY

%build -a
java --module-path target/randomizedtesting-runner-%{version}.jar --describe-module randomizedtesting.runner > module-describe.txt
# A versioned jar prints "name@version ... automatic", not "name automatic".
grep -q '^randomizedtesting.runner' module-describe.txt || { cat module-describe.txt; exit 1; }
grep -q ' automatic$' module-describe.txt || { cat module-describe.txt; exit 1; }

%files -f .mfiles
%doc LICENSE.txt README.txt CHANGES.txt
