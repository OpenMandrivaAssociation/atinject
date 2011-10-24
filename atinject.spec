%global artifactId javax.inject

Name:           atinject
Version:        1
Release:        2.20100611svn86
Summary:        Dependency injection specification for Java (JSR-330)

Group:          Development/Java
License:        ASL 2.0
URL:            http://code.google.com/p/atinject/
# latest release doesn't generate javadocs and there is no source
# tarball with pom.xml or ant build file
#
# svn export -r86 http://atinject.googlecode.com/svn/trunk atinject-1
# tar caf atinject-1.tar.xz atinject-1
Source0:        %{name}-%{version}.tar.xz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:       maven2
BuildRequires:       maven-install-plugin
BuildRequires:       maven-jar-plugin
BuildRequires:       maven-surefire-provider-junit4
BuildRequires:       maven-surefire-plugin
BuildRequires:       maven-javadoc-plugin
BuildRequires:       maven-resources-plugin
BuildRequires:       maven-release-plugin
BuildRequires:       maven-compiler-plugin


Requires:       jpackage-utils
Requires(post):       jpackage-utils
Requires(postun):     jpackage-utils

%description
This package specifies a means for obtaining objects in such a way as
to maximize reusability, testability and maintainability compared to
traditional approaches such as constructors, factories, and service
locators (e.g., JNDI). This process, known as dependency injection, is
beneficial to most nontrivial applications.

%package        javadoc
Summary:        API documentation for %{name}
Group:          Development/Java
Requires:       jpackage-utils

%description    javadoc
%{summary}.


%prep
%setup -q

rm -rf lib/

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL
mvn-jpp \
  -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
  install javadoc:javadoc

%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}%{_javadir}
install -d -m 755 %{buildroot}%{_mavenpomdir}

%add_to_maven_depmap %{artifactId} %{artifactId} %{version} JPP %{name}

# poms
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml \
    %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

# jar files
install -pm 644 target/%{artifactId}-*.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar

# symlinks
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)


# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name} # ghost symlink


%clean
rm -rf %{buildroot}

%post
%update_maven_depmap

%postun
%update_maven_depmap


%files
%defattr(-,root,root,-)
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*
%{_javadir}/*.jar

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}*

