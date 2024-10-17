%{?_javapackages_macros:%_javapackages_macros}
Name:          randomizedtesting
Version:       2.1.3
Release:       1%{?dist}
Summary:       Java Testing Framework
License:       ASL 2.0
URL:           https://labs.carrotsearch.com/randomizedtesting.html
Source0:       https://github.com/carrotsearch/randomizedtesting/archive/release/%{version}.tar.gz

BuildRequires: java-devel

BuildRequires: mvn(asm:asm)
BuildRequires: mvn(com.google.code.gson:gson)
BuildRequires: mvn(com.google.guava:guava)
BuildRequires: mvn(commons-io:commons-io)
BuildRequires: mvn(dom4j:dom4j)
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(org.apache.ant:ant)
BuildRequires: mvn(org.apache.ant:ant-junit)
BuildRequires: mvn(org.apache.maven:maven-artifact)
BuildRequires: mvn(org.apache.maven:maven-compat)
BuildRequires: mvn(org.apache.maven:maven-core)
BuildRequires: mvn(org.apache.maven:maven-plugin-api)
BuildRequires: mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires: mvn(org.apache.maven.shared:maven-common-artifact-filters)
BuildRequires: mvn(org.simpleframework:simple-xml)
BuildRequires: mvn(org.sonatype.oss:oss-parent:pom:)
%if 0
# junit4-ant build tools
BuildRequires: mvn(net.sf.proguard:proguard)
BuildRequires: proguard-maven-plugin
# Test deps
BuildRequires: mvn(org.easytesting:fest-assert-core) >= 2.0M6
%endif

BuildRequires: maven-local
BuildRequires: maven-plugin-bundle
BuildRequires: maven-plugin-plugin

Requires:      javapackages-tools
BuildArch:     noarch

%description
Foundation classes and rules for applying the
principles of Randomized Testing.

%package junit4-ant
Summary:       RandomizedTesting JUnit4 ANT Task
Requires:      %{name} = %{version}-%{release}

%description junit4-ant
RandomizedTesting JUnit4 ANT Task.

%package junit4-maven-plugin
Summary:       RandomizedTesting JUnit4 Maven Plugin
Requires:      %{name} = %{version}-%{release}

%description junit4-maven-plugin
RandomizedTesting JUnit4 Maven Plugin.

%package runner
Summary:       RandomizedTesting Randomized Runner
Requires:      %{name} = %{version}-%{release}

%description runner
RandomizedRunner is a JUnit runner, so it is capable of
running @Test-annotated test cases.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-release-%{version}
find . -name "*.class" -delete
find . -name "*.jar" -delete
find . -name "*.dll" -delete
find . -name "*.dylib" -delete
find . -name "*.so" -delete

# Remove bundled JavaScript libraries
find . -name "*.js" -print -delete
sed -i '/jquery/d' \
 junit4-ant/src/main/resources/com/carrotsearch/ant/tasks/junit4/templates/json/index.html \
 junit4-ant/src/main/java/com/carrotsearch/ant/tasks/junit4/listeners/json/JsonReport.java
sed -i '/script.js/d' \
 junit4-ant/src/main/resources/com/carrotsearch/ant/tasks/junit4/templates/json/index.html \
 junit4-ant/src/main/java/com/carrotsearch/ant/tasks/junit4/listeners/json/JsonReport.java

%pom_remove_dep org.easytesting:fest-assert-core randomized-runner

%pom_disable_module examples/maven
%pom_disable_module examples/ant
%pom_disable_module packaging
%pom_disable_module junit4-maven-plugin-tests
# Disable repackaged and shaded deps
%pom_remove_plugin com.pyx4me:proguard-maven-plugin junit4-ant
%pom_remove_plugin org.codehaus.mojo:exec-maven-plugin junit4-ant
%pom_remove_plugin :maven-dependency-plugin junit4-ant
# Fix deps scope
%pom_xpath_remove "pom:scope[text()='provided']" junit4-ant
sed -i 's/\r//' README randomized-runner/README

%build

%mvn_package :%{name}-parent %{name}-runner
# Requires org.easytesting:fest-assert-core >= 2.0M6
%mvn_build -f -s

%install
%mvn_install

#mkdir -p %%{buildroot}%%{_sysconfdir}/ant.d
#echo "ant ant/ant-junit commons-io google-gson guava junit junit4-ant objectweb-asm3/asm %%{name}/randomizedtesting-runner simple-xml" > %%{name}-junit4-ant
#install -p -m 644 %%{name}-junit4-ant %%{buildroot}%%{_sysconfdir}/ant.d/%%{name}-junit4-ant

%files
%dir %{_javadir}/%{name}
%doc LICENSE README

%files junit4-ant -f .mfiles-junit4-ant
#%%config(noreplace) %%{_sysconfdir}/ant.d/%%{name}-junit4-ant

%files junit4-maven-plugin -f .mfiles-junit4-maven-plugin

%files runner -f .mfiles-%{name}-runner
%doc randomized-runner/README

%files javadoc -f .mfiles-javadoc
%doc LICENSE

%changelog
* Fri Jun 20 2014 gil cattaneo <puntogil@libero.it> 2.1.3-1
- update to 2.1.3

* Tue Jun 17 2014 gil cattaneo <puntogil@libero.it> 2.0.15-4
- fix BR list

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Feb 02 2014 gil cattaneo <puntogil@libero.it> 2.0.15-2
- Fix junit4-ant deps scope

* Thu Jan 23 2014 gil cattaneo <puntogil@libero.it> 2.0.15-1
- update to 2.0.15

* Mon Jun 03 2013 gil cattaneo <puntogil@libero.it> 2.0.9-1
- initial rpm