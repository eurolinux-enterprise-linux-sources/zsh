# this file is encoded in UTF-8  -*- coding: utf-8 -*-

Summary: Powerful interactive shell
Name: zsh
Version: 5.0.2
Release: 31%{?dist}
License: MIT
URL: http://zsh.sourceforge.net/
Group: System Environment/Shells
Source0: http://download.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Source1: zlogin.rhs
Source2: zlogout.rhs
Source3: zprofile.rhs
Source4: zshrc.rhs
Source5: zshenv.rhs
Source6: dotzshrc
Source7: zshprompt.pl
Source8: http://cgit.freedesktop.org/systemd/systemd/plain/shell-completion/systemd-zsh-completion.zsh
Patch0: zsh-serial.patch

# make the wait built-in work for already exited processes (#1150554)
Patch2: zsh-5.0.2-wait-for-exited.patch

Patch4: zsh-4.3.6-8bit-prompts.patch
Patch5: zsh-test-C02-dev_fd-mock.patch

# signal safety when updating global state (#1163823)
Patch6: zsh-5.0.2-signal-safety.patch

# fix NOEXEC option in execsimple() optimisation (#1146512)
Patch7: zsh-5.0.2-noexec.patch

# optimize matching of multiple * in wildcards (#1130418)
Patch8: zsh-5.0.2-wildcard-opt.patch

# use heap rather than stack allocation for variable length arrays (#1130418)
Patch9: zsh-5.0.2-disable-alloca.patch

# shell emulation doc addition (#1147545)
Patch10: zsh-5.0.2-emul-man-page.patch

# Tmp.
Patch11: zsh-5.0.2.texi-itemx.patch
Patch12: http://ausil.fedorapeople.org/aarch64/zsh/zsh-aarch64.patch

# suppress a warning about closing an already closed file descriptor (#1131191)
Patch13: zsh-5.0.2-close-fd.patch

# fix SIGSEGV of the syntax check in ksh emulation mode (#1222867)
Patch14: zsh-5.0.2-ksh-syntax-check.patch

# fix command substitutions to parse contents as they are read in (#1241023)
Patch15: zsh-5.0.2-cmd-subst.patch

# fix malloc() signal leak in lexsave() (#1267912)
Patch16: zsh-5.0.2-malloc-signal.patch

# queue signals while processing a job exit (#1291782)
Patch17: zsh-5.0.2-sigchld-deadlock.patch

# prevent zsh from crashing when printing the "out of memory" message (#1302229)
Patch18: zsh-5.0.2-oom-fatal-error.patch

# signal-handling related fixes collected from upstream (#1198671)
Patch19: zsh-5.0.2-signal-handling.patch

# improve options handling in the _arguments completion utility (#1334312)
Patch20: zsh-5.0.2-comp-args.patch

# fix off-by-one error in completion utility cache code (#1344599)
Patch21: zsh-5.0.2-comp-cache.patch

# fix parsing of parameter subscript expression with NOEXEC (#1398740)
Patch22: zsh-5.0.2-noexec-subscript.patch

# zero new space allocated in prompt buffer (#1408619)
Patch23: zsh-5.0.2-initialize-prompt-buffer.patch

# fix crash while inputting long multi-line strings (#1492595)
Patch24: zsh-5.0.2-freeheap-crash.patch

# fix buffer overflow for very long fds in >& fd syntax (CVE-2014-10071)
Patch33: zsh-5.0.2-CVE-2014-10071.patch

# fix buffer overflow when scanning very long path for symlinks (CVE-2014-10072)
Patch34: zsh-5.0.2-CVE-2014-10072.patch

# fix NULL dereference in cd (CVE-2017-18205)
Patch35: zsh-5.0.2-CVE-2017-18205.patch

# fix buffer overrun in xsymlinks (CVE-2017-18206)
Patch36: zsh-5.0.2-CVE-2017-18206.patch

# avoid crash when copying empty hash table (CVE-2018-7549)
Patch37: zsh-5.0.2-CVE-2018-7549.patch

# fix stack-based buffer overflow in exec.c:hashcmd() (CVE-2018-1071)
Patch38: zsh-5.0.2-CVE-2018-1071.patch

# fix stack-based buffer overflow in gen_matches_files() (CVE-2018-1083)
Patch39: zsh-5.0.2-CVE-2018-1083.patch

# fix stack-based buffer overflow in utils.c:checkmailpath() (CVE-2018-1100)
Patch40: zsh-5.0.2-CVE-2018-1100.patch

BuildRequires: coreutils sed ncurses-devel libcap-devel
BuildRequires: texinfo texi2html gawk hostname
Requires(post): /sbin/install-info grep
Requires(preun): /sbin/install-info
Requires(postun): coreutils grep

%description
The zsh shell is a command interpreter usable as an interactive login
shell and as a shell script command processor.  Zsh resembles the ksh
shell (the Korn shell), but includes many enhancements.  Zsh supports
command line editing, built-in spelling correction, programmable
command completion, shell functions (with autoloading), a history
mechanism, and more.

%package html
Summary: Zsh shell manual in html format
Group: System Environment/Shells

%description html
The zsh shell is a command interpreter usable as an interactive login
shell and as a shell script command processor.  Zsh resembles the ksh
shell (the Korn shell), but includes many enhancements.  Zsh supports
command line editing, built-in spelling correction, programmable
command completion, shell functions (with autoloading), a history
mechanism, and more.

This package contains the Zsh manual in html format.

%prep

%setup -q
%patch0 -p1 -b .serial
%patch2 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1
%patch40 -p1

cp -p %SOURCE7 .

%build
%define _bindir /bin
# Avoid stripping...
export LDFLAGS=""
%configure --enable-etcdir=%{_sysconfdir} --with-tcsetpgrp  --enable-maildir-support

make all html

%check
# Run the testsuite
# the completion tests hang on s390 and s390x
  ( cd Test
    mkdir skipped
%ifarch s390 s390x ppc ppc64
    mv Y*.ztst skipped
%endif
%ifarch s390 s390x ppc64
    # FIXME: This is a real failure, Debian apparently just don't test.
    # RHBZ: 460043
    mv D02glob.ztst skipped
%endif
    # FIXME: This hangs in mock
    # Running test: Test loading of all compiled modules
    mv V01zmodload.ztst skipped
    true )
  ZTST_verbose=1 make test

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall install.info \
  fndir=$RPM_BUILD_ROOT%{_datadir}/zsh/%{version}/functions \
  sitefndir=$RPM_BUILD_ROOT%{_datadir}/zsh/site-functions \
  scriptdir=$RPM_BUILD_ROOT%{_datadir}/zsh/%{version}/scripts \
  sitescriptdir=$RPM_BUILD_ROOT%{_datadir}/zsh/scripts

install -p %SOURCE8 $RPM_BUILD_ROOT%{_datadir}/zsh/%{version}/functions/_systemd

rm -f ${RPM_BUILD_ROOT}%{_bindir}/zsh-%{version}
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}
for i in %{SOURCE4} %{SOURCE1} %{SOURCE2} %{SOURCE5} %{SOURCE3}; do
    install -m 644 $i ${RPM_BUILD_ROOT}%{_sysconfdir}/"$(basename $i .rhs)"
done

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/skel
install -m 644 %{SOURCE6} ${RPM_BUILD_ROOT}%{_sysconfdir}/skel/.zshrc

# This is just here to shut up rpmlint, and is very annoying.
# Note that we can't chmod everything as then rpmlint will complain about
# those without a she-bang line.
for i in checkmail harden run-help zcalc zkbd; do
    sed -i -e 's!/usr/local/bin/zsh!%{_bindir}/zsh!' \
      ${RPM_BUILD_ROOT}%{_datadir}/zsh/*/functions/$i
    chmod +x ${RPM_BUILD_ROOT}%{_datadir}/zsh/*/functions/$i
done


%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{_sysconfdir}/shells ] ; then
    echo "%{_bindir}/zsh" > %{_sysconfdir}/shells
else
    grep -q "^%{_bindir}/zsh$" %{_sysconfdir}/shells || echo "%{_bindir}/zsh" >> %{_sysconfdir}/shells
fi

if [ -f %{_infodir}/zsh.info.gz ]; then
# This is needed so that --excludedocs works.
/sbin/install-info %{_infodir}/zsh.info.gz %{_infodir}/dir \
  --entry="* zsh: (zsh).			An enhanced bourne shell."
fi

:

%preun
if [ "$1" = 0 ] ; then
    if [ -f %{_infodir}/zsh.info.gz ]; then
    # This is needed so that --excludedocs works.
    /sbin/install-info --delete %{_infodir}/zsh.info.gz %{_infodir}/dir \
      --entry="* zsh: (zsh).			An enhanced bourne shell."
    fi
fi
:

%postun
if [ "$1" = 0 ] ; then
    if [ -f %{_sysconfdir}/shells ] ; then
        TmpFile=`%{_bindir}/mktemp /tmp/.zshrpmXXXXXX`
        grep -v '^%{_bindir}/zsh$' %{_sysconfdir}/shells > $TmpFile
        cp -f $TmpFile %{_sysconfdir}/shells
        rm -f $TmpFile
    fi
fi

%files
%defattr(-,root,root)
%doc README LICENCE Etc/BUGS Etc/CONTRIBUTORS Etc/FAQ FEATURES MACHINES
%doc NEWS Etc/zsh-development-guide Etc/completion-style-guide zshprompt.pl
%attr(755,root,root) %{_bindir}/zsh
%{_mandir}/*/*
%{_infodir}/*
%{_datadir}/zsh
%{_libdir}/zsh
%config(noreplace) %{_sysconfdir}/skel/.z*
%config(noreplace) %{_sysconfdir}/z*

%files html
%defattr(-,root,root)
%doc Doc/*.html

%changelog
* Fri May 04 2018 Kamil Dudka <kdudka@redhat.com> - 5.0.2-31
- fix defects detected by Coverity related to CVE-2017-18206 and CVE-2018-1083

* Thu May 03 2018 Kamil Dudka <kdudka@redhat.com> - 5.0.2-30
- fix stack-based buffer overflow in utils.c:checkmailpath() (CVE-2018-1100)
- fix stack-based buffer overflow in gen_matches_files() (CVE-2018-1083)
- fix stack-based buffer overflow in exec.c:hashcmd() (CVE-2018-1071)
- avoid crash when copying empty hash table (CVE-2018-7549)
- fix buffer overrun in xsymlinks (CVE-2017-18206)
- fix NULL dereference in cd (CVE-2017-18205)
- fix buffer overflow when scanning very long path for symlinks (CVE-2014-10072)
- fix buffer overflow for very long fds in >& fd syntax (CVE-2014-10071)

* Tue Sep 19 2017 Kamil Dudka <kdudka@redhat.com> - 5.0.2-29
- fix crash while inputting long multi-line strings (#1492595)

* Thu Feb 16 2017 Kamil Dudka <kdudka@redhat.com> - 5.0.2-28
- zero new space allocated in prompt buffer (#1408619)

* Mon Nov 28 2016 Kamil Dudka <kdudka@redhat.com> - 5.0.2-27
- fix parsing of parameter subscript expression with NOEXEC (#1398740)

* Mon Oct 17 2016 Kamil Dudka <kdudka@redhat.com> - 5.0.2-26
- fix crash while parsing the here-document syntax (#1374752)

* Thu Jul 14 2016 Kamil Dudka <kdudka@redhat.com> - 5.0.2-25
- improve use of new command substitution in completion (#1356388)

* Fri Jun 10 2016 Kamil Dudka <kdudka@redhat.com> - 5.0.2-24
- fix off-by-one error in completion utility cache code (#1344599)

* Mon May 23 2016 Kamil Dudka <kdudka@redhat.com> - 5.0.2-23
- fix parse error on a script with unescaped exclamation mark (#1338689)

* Tue May 17 2016 Kamil Dudka <kdudka@redhat.com> - 5.0.2-22
- fix alias expansion in history for command substitution (#1321303)

* Mon May 09 2016 Kamil Dudka <kdudka@redhat.com> - 5.0.2-21
- improve options handling in the _arguments completion utility (#1334312)

* Tue Mar 29 2016 Kamil Dudka <kdudka@redhat.com> - 5.0.2-20
- turn off history word marking in command substitution (#1321303)

* Tue Mar 01 2016 Kamil Dudka <kdudka@redhat.com> - 5.0.2-19
- signal-handling related fixes collected from upstream (#1198671)

* Wed Feb 17 2016 Kamil Dudka <kdudka@redhat.com> - 5.0.2-18
- prevent zsh from crashing when printing the "out of memory" message (#1302229)

* Wed Feb 17 2016 Kamil Dudka <kdudka@redhat.com> - 5.0.2-17
- queue signals while processing a job exit (#1291782)

* Mon Nov 02 2015 Kamil Dudka <kdudka@redhat.com> - 5.0.2-16
- fix malloc() signal leak in lexsave() (#1267912)

* Thu Oct 08 2015 Kamil Dudka <kdudka@redhat.com> - 5.0.2-15
- fix crash in ksh mode with -n and $HOME (#1267251)

* Fri Aug 14 2015 Kamil Dudka <kdudka@redhat.com> - 5.0.2-14
- fix alias handling in command substitution (#1253555)

* Thu Jul 30 2015 Kamil Dudka <kdudka@redhat.com> - 5.0.2-13
- fix parser regression introduced by the fix for bug #1241023

* Wed Jul 08 2015 Kamil Dudka <kdudka@redhat.com> - 5.0.2-12
- fix command substitutions to parse contents as they are read in (#1241023)

* Fri May 22 2015 Kamil Dudka <kdudka@redhat.com> - 5.0.2-11
- fix SIGSEGV of the syntax check in ksh emulation mode (#1222867)

* Mon May 18 2015 Kamil Dudka <kdudka@redhat.com> - 5.0.2-10
- signal safety when updating global state (#1163823)

* Tue May 05 2015 Kamil Dudka <kdudka@redhat.com> - 5.0.2-9
- signal safety when updating global state in execshfunc() (#1163823)
- make the wait built-in work for already exited processes (#1162198)
- replace an incorrect comment in /etc/zshenv (#1164312)
- optimize matching of multiple * in wildcards (#1130418)
- use heap rather than stack allocation for variable length arrays (#1165118)
- shell emulation doc addition (#1147545)
- suppress a warning about closing an already closed file descriptor (#1131191)

* Thu Mar 19 2015 Kamil Dudka <kdudka@redhat.com> - 5.0.2-8
- fix NOEXEC option in execsimple() optimisation (#1146512)

* Tue Jan 28 2014 James Antill <james@fedoraproject.org> - 5.0.2-7
- Remove unneeded build require on tetex.
- Resolves: rhbz#1037828
- Depend on hostname package instead of /bin/hostname.

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 5.0.2-6
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 5.0.2-5
- Mass rebuild 2013-12-27

* Tue Jun 25 2013 Dominic Hopf <dmaphy@fedoraproject.org> - 5.0.2-4
- up-to-date systemd completion (#949003)
- apply patch for building for aarch64 (#926864)

* Mon Apr 15 2013 James Antill <james@fedoraproject.org> - 5.0.2-3
- Fix the changelog dates.
- Fix the texi itemx bug.
- Resolves: bug#927863

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 08 2013 Dominic Hopf <dmaphy@fedoraproject.org> - 5.0.2-1
- Update to new upstream version: Zsh 5.0.2

* Wed Nov 21 2012 Dominic Hopf <dmaphy@fedoraproject.org> - 5.0.0-1
- Update to new upstream version: Zsh 5.0.0

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Mar 04 2012 Dominic Hopf <dmaphy@fedoraproject.org> - 4.3.17-1
- Update to new upstream version: Zsh 4.3.17

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 24 2011 Dominic Hopf <dmaphy@fedoraproject.org> - 4.3.15-1
- Update to new upstream version: Zsh 4.3.15

* Sat Dec 17 2011 Dominic Hopf <dmaphy@fedoraproject.org> - 4.3.14-2
- change the License field to MIT (RHBZ#768548)

* Sat Dec 10 2011 Dominic Hopf <dmaphy@fedoraproject.org> - 4.3.14-1
- Update to new upstream version: Zsh 4.3.14

* Sat Dec 03 2011 Dominic Hopf <dmaphy@fedoraproject.org> - 4.3.13-1
- Update to new upstream version: Zsh 4.3.13

* Sat Aug 13 2011 Dominic Hopf <dmaphy@fedoraproject.org> - 4.3.12-1
- Update to new upstream version: Zsh 4.3.12

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 20 2011 Christopher Ailon <caillon@redhat.com> - 4.3.11-1
- Rebase to upstream version 4.3.11

* Tue Dec 7 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 4.3.10-6
- Rebuild for FTBFS https://bugzilla.redhat.com/show_bug.cgi?id=631197
- Remove deprecated PreReq, the packages aren't needed at runtime and they're
  already in Requires(post,preun,etc): lines.

* Mon Mar 22 2010 James Antill <james@fedoraproject.org> - 4.3.10-5
- Add pathmunge to our /etc/zshrc, for profile.d compat.
- Resolves: bug#548960

* Fri Aug  7 2009 James Antill <james@fedoraproject.org> - 4.3.10-4
- Allow --excludedocs command to work!
- Resolves: bug#515986

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 James Antill <james@fedoraproject.org> - 4.3.10-1
- Import new upstream 4.3.10

* Wed Jun 10 2009 Karsten Hopp <karsten@redhat.com> 4.3.9-4.1
- skip D02glob test on s390, too

* Mon Mar  2 2009 James Antill <james@fedoraproject.org> - 4.3.9-4
- Remove D02glob testcase on ppc/ppc64, and hope noone cares

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild
