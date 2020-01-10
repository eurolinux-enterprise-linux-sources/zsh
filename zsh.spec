# this file is encoded in UTF-8  -*- coding: utf-8 -*-

Summary: A powerful interactive shell
Name: zsh
Version: 4.3.11
Release: 4%{?dist}.2
License: BSD
URL: http://zsh.sunsite.dk/
Group: System Environment/Shells
Source0: ftp://ftp.zsh.org/pub/zsh-%{version}.tar.bz2
Source1: zlogin.rhs
Source2: zlogout.rhs
Source3: zprofile.rhs
Source4: zshrc.rhs
Source5: zshenv.rhs
Source6: dotzshrc
Source7: zshprompt.pl
Patch0: zsh-serial.patch
Patch4: zsh-4.3.6-8bit-prompts.patch
Patch5: zsh-test-C02-dev_fd-mock.patch
Patch6: zsh-4.3.6-hack-a01grammar-test-select-off.patch
# RHEL-6.3
Patch12: BZ-612685-zsh-4.3.10-math-subst.patch
# RHEL-6.6
Patch22: BZ-859859-syntax-check-fail.patch
# RHEL-6.7 and later
Patch23: BZ-978613-malloc-from-signal-handler-workaround.patch

# avoid using uninitialised memory after lexer realloc (#1146119)
Patch24: zsh-4.3.10-lex-realloc.patch

# optimize matching of multiple * in wildcards (#1130418)
Patch25: zsh-5.0.2-wildcard-opt.patch

# use heap rather than stack allocation for variable length arrays (#567215)
Patch26: zsh-5.0.2-disable-alloca.patch

# prevent jobs -Z from destroying environment variables (#878324)
Patch27: zsh-5.0.0-jobs-z-env.patch

# shell emulation doc addition (#1104021)
Patch28: zsh-5.0.2-emul-man-page.patch

# fix defects found by GCC and Coverity Analysis (#1181608)
Patch29: zsh-4.3.11-coverity.patch

# fix malloc() signal leak in lexsave() (#1267903)
Patch30: zsh-4.3.11-malloc-signal.patch

# signal-handling related fixes collected from upstream (#1311166)
Patch32: zsh-4.3.11-signal-handling.patch

# Prereq: fileutils grep /sbin/install-info
Buildroot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: mktemp coreutils sed ncurses-devel libcap-devel
BuildRequires: texinfo tetex texi2html gawk /bin/hostname
Requires(post): /sbin/install-info grep
Requires(preun): /sbin/install-info
Requires(postun): mktemp coreutils grep

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
%patch0 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

# RHEL-6.3
%patch12 -p1

# RHEL-6.6
%patch22 -p1

# RHEL-6.7 and later
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch32 -p1

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
* Tue Mar 01 2016 Kamil Dudka <kdudka@redhat.com> - 4.3.11-5.el6_7.2
- signal-handling related fixes collected from upstream (#1316945)

* Tue Oct 20 2015 Kamil Dudka <kdudka@redhat.com> - 4.3.11-4.el6_7.1
- fix malloc() signal leak in lexsave() (#1267903)

* Mon May 18 2015 Kamil Dudka <kdudka@redhat.com> - 4.3.11-4
- signal safety when updating global state (#978613)

* Mon Feb 23 2015 Kamil Dudka <kdudka@redhat.com> - 4.3.11-3
- signal safety when updating global state in execshfunc() (#978613)

* Tue Jan 13 2015 Kamil Dudka <kdudka@redhat.com> - 4.3.11-2
- fix defects found by GCC and Coverity Analysis (#1181608)

* Thu Nov 20 2014 Kamil Dudka <kdudka@redhat.com> - 4.3.11-1
- rebase to 4.3.11 (#1132710)

* Fri Nov 14 2014 Kamil Dudka <kdudka@redhat.com> - 4.3.10-12
- avoid using uninitialised memory after lexer realloc (#1146119)
- replace an incorrect comment in /etc/zshenv (#1103697)
- optimize matching of multiple * in wildcards (#1131172)
- use heap rather than stack allocation for variable length arrays (#567215)
- prevent jobs -Z from destroying environment variables (#878324)
- shell emulation doc addition (#1104021)

* Thu Nov 13 2014 Kamil Dudka <kdudka@redhat.com> - 4.3.10-11
- signal safety when updating global state in execshfunc() (#978613)

* Tue Sep  7 2014 James Antill <james.antill@redhat.com> - 4.3.10-10
- Workaround zsh calling malloc from signal handler.
- Resolves: rhbz#978613

* Wed Aug 20 2014 James Antill <james.antill@redhat.com> - 4.3.10-8
- Fix syntax check failure with double square brackets.
- Resolves: rhbz#859859

* Mon Aug  5 2013 James Antill <james.antill@redhat.com> - 4.3.10-7
- Change {NAME:OFFSET:LENGTH} substitution feature to ignore KSH_ARRAYS option.
- Fixup tests.
- Resolves: rhbz#820530

* Tue Jun 25 2013 James Antill <james.antill@redhat.com> - 4.3.10-6
- Add {NAME:OFFSET:LENGTH} substitution feature.
- Resolves: rhbz#820530

* Fri Mar  2 2012 James Antill <james.antill@redhat.com> - 4.3.10-5
- Change invocation as "zsh foo" to search the path by default.
- Add new option PATH_SCRIPT for old behaviour.
- Resolves: rhbz#612685
- Solve defect in emulation of ksh with math substituion.
- Resolves: rhbz#657300

* Tue Dec 08 2009 Dennis Gregorovic <dgregor@redhat.com> - 4.3.10-4.1
- Rebuilt for RHEL 6

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

* Fri Dec 20 2008 James Antill <james@fedoraproject.org> - 4.3.9-1
- Import new upstream 4.3.9

* Mon Aug 25 2008 James Antill <james@fedoraproject.org> - 4.3.6-5
- Import new upstream 4.3.6
- Rebase 8bit prompt patch
- Add patch fuzz=2
- Add BuildReq on /bin/hostname directly
- FIXME: These should all be unpatched, at some point.
- Don't test /dev/fd as mock doesn't like it
- Don't test the modload module, as mock doesn't like loading them all
- Don't test the select test in A01grammar, stdin/stderr racy?

* Thu Jan 31 2008 James Antill <james@fedoraproject.org> - 4.3.4-7
- Tweak /etc/zshrc to source /etc/profile.d/*.sh in ksh compat. mode
- Tweak /etc/zprofile to source /etc/profile in ksh compat. mode
- Resolves: rhbz#430665

* Mon Nov  3 2007 James Antill <jantill@redhat.com> - 4.3.4-5
- Fix 8bit chars in prompts.
- Resolves: 375211

* Thu Oct 11 2007 James Antill <jantill@redhat.com> - 4.3.4-4
- Fix login shell detection.
- Resolves: 244684

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 4.3.4-3
- BuildRequire gawk.

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 4.3.4-2
- Rebuild for selinux ppc32 issue.

* Tue Aug 28 2007 James Antill <jantill@redhat.com> - 4.3.4-1
- Rebuild for buildid/ppc32

* Wed Jul 25 2007 James Antill <jantill@redhat.com> - 4.3.4-0
- Move to upstream 4.3.4, the stable non-stable release

* Mon Mar  5 2007 James Antill <james@and.org> - 4.2.6-6
- Move requires to be scriptlet specific
- chmod functions, to shut rpmlint up (false positive warning)
- sed only the requied functions (again, shuts rpmlint up)
- Remove zsh-4.0.6-make-test-fail.patch
- Remove RPM_SOURCE_DIR var, using %%{SOURCEx} and basename
Resolves: rhbz#226813

* Tue Feb 27 2007 James Antill <james@and.org> - 4.2.6-5
- Fix sed typo.
- Fix skel expansion problem.
- Add Requires for mktemp/info/etc.
- Use cp again due to SELinux context
Resolves: rhbz#226813

* Tue Feb 27 2007 James Antill <james@and.org> - 4.2.6-4
- Fix buildroot to new Fedora default.
- Remove /etc/skel from ownership.
- Remove explicit libcap dep.
- Tweak postun script.
- Move checking to generic rpm infrastructure.
Resolves: rhbz#226813

* Tue Jan 16 2007 Miroslav Lichvar <mlichvar@redhat.com> - 4.2.6-3
- Link with ncurses
- Add dist tag
- Make scriptlets safer

* Tue Sep 19 2006 James Antill <jantill@redhat.com> - 4.2.6-2
- Add --enable-maildir-support BZ#186281

* Mon Sep 11 2006 Christopher Aillon <caillon@redhat.com> - 4.2.6-1
- Update to 4.2.6

* Wed Jul 13 2006 Jesse Keating <jkeating@redhat.com> - 4.2.5-2
- rebuild
- add mising br texi2html

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 4.2.5-1.2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 4.2.5
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan  4 2006 Jesse Keating <jkeating@redhat.com> 0 4.2.5-1.2
- rebuilt again

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Mar 14 2005 Colin Walters <walters@redhat.com> - 4.2.5-1
- New upstream version
- Fix Doc html includes; looks like texinfo changed incompatibly

* Mon Mar 14 2005 Colin Walters <walters@redhat.com> - 4.2.1-3
- Rebuild for GCC4

* Sun Jan 16 2005 Colin Walters <walters@redhat.com> - 4.2.1-2
- Install config files using install instead of cp, with mode 644

* Mon Jan 03 2005 Colin Walters <walters@redhat.com> - 4.2.1-1
- New upstream version 4.2.1
- FEATURES, MACHINES, and NEWS moved to toplevel dir
- Update zsh-4.0.6-make-test-fail.patch, but do not apply it for now
- Remove upstreamed zsh-4.2.0-jobtable-125452.patch

* Mon Jul  5 2004 Jens Petersen <petersen@redhat.com> - 4.2.0-3
- source profile in zprofile rather than .zshrc (Péter Kelemen,
  Magnus Gustavsson, 102187,126539)
- add zsh-4.2.0-jobtable-125452.patch to fix job table bug
  (Henrique Martins, 125452)
- buildrequire tetex for texi2html (Maxim Dzumanenko, 124182)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Apr 10 2004 Jens Petersen <petersen@redhat.com> - 4.2.0-1
- update to 4.2.0 stable release
- zsh-4.0.7-bckgrnd-bld-102042.patch no longer needed
- add compinit and various commented config improvements to .zshrc
  (Eric Hattemer,#114887)
- include zshprompt.pl in doc dir (Eric Hattemer)
- drop setenv function from zshrc

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 13 2004 Jens Petersen <petersen@redhat.com> - 4.0.9-1
- update to 4.0.9 release
- zsh-4.0.7-completion-_files-110852.patch no longer needed
- update zsh-4.0.7-bckgrnd-bld-102042.patch to better one with --with-tcsetpgrp
  configure option by Philippe Troin
- configure --with-tcsetpgrp
- buildrequire texinfo for makeinfo
- fix ownership of html manual (Florian La Roche, #112749)

* Tue Dec  9 2003 Jens Petersen <petersen@redhat.com> - 4.0.7-3
- no longer "stty erase" in /etc/zshrc for screen [Lon Hohberger]

* Thu Nov 27 2003 Jens Petersen <petersen@redhat.com> - 4.0.7-2
- quote %% in file glob'ing completion code (#110852)
  [reported with patch by Keith T. Garner]
- add zsh-4.0.7-bckgrnd-bld-102042.patch from Philippe Troin to allow
  configure to run in the background (#102042) [reported by Michael Redinger]
- above patch requires autoconf to be run
- include html manual in separate -html subpackage
- changed url to master site
- skip completion tests on ppc and ppc64 for now, since they hang

* Fri Jun 20 2003 Jens Petersen <petersen@redhat.com> - 4.0.7-1
- update to 4.0.7 bugfix release

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May  1 2003 Jens Petersen <petersen@redhat.com> - 4.0.6-7
- don't set stty erase in a dumb terminal with tput kbs in /etc/zshrc (#89856)
  [reported by Ben Liblit]
- make default prompt more informative, like bash

* Mon Feb 10 2003 Jens Petersen <petersen@redhat.com> - 4.0.6-5
- skip completion tests on s390 and s390x since they hang

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 25 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- fix adding zsh to /etc/shells

* Fri Nov 29 2002 Florian La Roche <Florian.LaRoche@redhat.de> 4.0.6-2
- make sure /bin/zsh is owned by root and not bhcompile
- do not package zsh-%%{version} into binary rpm

* Thu Nov 28 2002 Jens Petersen <petersen@redhat.com> 4.0.6-1
- define _bindir to be /bin and use it
- use _sysconfdir and _libdir

* Mon Nov 25 2002 Jens Petersen <petersen@redhat.com>
- 4.0.6
- add url
- add --without check build option
- don't autoconf
- make "make test" failure not go ignored
- move sourcing of profile from zshenv to new .zshrc file for now (#65509)
- preserve dates when installing rc files

* Fri Nov 15 2002 Jens Petersen <petersen@redhat.com>
- setup backspace better with tput in zshrc to please screen (#77833)
- encode spec file in utf-8

* Fri Jun 28 2002 Trond Eivind Glomsrød <teg@redhat.com> 4.0.4-8
- Make it work with a serial port (#56353)
- Add $HOME/bin to path for login shells (#67110)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Apr  5 2002 Trond Eivind Glomsrød <teg@redhat.com> 4.0.4-5
- Source /etc/profile from /etc/zshenv instead of /etc/zprofile, 
  to run things the same way bash do (#62788)

* Tue Apr  2 2002 Trond Eivind Glomsrød <teg@redhat.com> 4.0.4-4
- Explicitly specify blank LDFLAGS to avoid autoconf thinking it 
  should strip when linking

* Thu Feb 21 2002 Trond Eivind Glomsrød <teg@redhat.com> 4.0.4-3
- Rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Oct 26 2001 Trond Eivind Glomsrød <teg@redhat.com> 4.0.4-1
- 4.0.4
- Don't force emacs keybindings, they're the default (#55102)

* Wed Oct 24 2001 Trond Eivind Glomsrød <teg@redhat.com> 4.0.3-1
- 4.0.3

* Mon Jul 30 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Fix typo in comment in zshrc (#50214)
- Don't set environment variables in  /etc/zshrc (#50308)

* Tue Jun 26 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 4.0.2
- Run the testsuite during build

* Wed Jun 20 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Add libtermcap-devel and libcap-devel to buildrequires

* Fri Jun  1 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 4.0.1

* Thu May 17 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 4.0.1pre4
- zsh is now available in bz2 - use it

* Mon Apr  9 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 4.0.1pre3
- remove the dir file from the info directory

* Wed Mar 21 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Remove contents from /etc/zshenv file - no reason to duplicate things
  from /etc/profile, which is sourced from /etc/zprofile (#32478)

* Thu Mar 15 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 4.0.1pre2
- remove some obsolete code in /etc/zprofile

* Tue Feb 27 2001 Preston Brown <pbrown@redhat.com>
- noreplace config files.

* Thu Feb 15 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Handle RLIMIT_LOCKS in 2.4 (#27834 - patch from H.J. Lu)

* Mon Jan 08 2001 Trond Eivind Glomsrød <teg@redhat.com>
- rebuild to fix #23568  (empty signal list)

* Tue Nov 28 2000 Trond Eivind Glomsrød <teg@redhat.com>
- fix the post script, so we only have only line for zsh
  and can remove the trigger
- get rid of some instances of "/usr/local/bin/zsh"

* Mon Nov 20 2000 Bill Nottingham <notting@redhat.com>
- fix ia64 build

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jul 02 2000 Trond Eivind Glomsrød <teg@redhat.com>
- rebuild

* Tue Jun 06 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 3.0.8
- use %%configure and %%makeinstall
- updated URL
- disable old patches
- add better patch for texi source
- use %%{_mandir} and %%{_infodir}
- use %%{_tmppath}

* Tue May 02 2000 Trond Eivind Glomsrød <teg@redhat.com>
- patched to recognize export in .zshrc (bug #11169)

* Tue Mar  7 2000 Jeff Johnson <jbj@redhat.com>
- rebuild for sparc baud rates > 38400.

* Fri Mar 03 2000 Cristian Gafton <gafton@redhat.com>
- fix postun script so that we don't remove ourselves on every update
  doh...
- add a trigger to fix old versions of the package

* Mon Jan 31 2000 Cristian Gafton <gafton@redhat.com>
- rebuild to fix dependencies

* Thu Jan 13 2000 Jeff Johnson <jbj@redhat.com>
- update to 3.0.7.
- source /etc/profile so that USER gets set correctly (#5655).

* Fri Sep 24 1999 Michael K. Johnson <johnsonm@redhat.com>
- source /etc/profile.d/*.sh in zprofile

* Tue Sep 07 1999 Cristian Gafton <gafton@redhat.com>
- fix zshenv and zprofile scripts - foxed versions from HJLu.

* Thu Jul 29 1999 Bill Nottingham <notting@redhat.com>
- clean up init files some. (#4055)

* Tue May 18 1999 Jeff Johnson <jbj@redhat.com>
- Make sure that env variable TmpFile is evaluated. (#2898)

* Sun May  9 1999 Jeff Johnson <jbj@redhat.com>
- fix select timeval initialization (#2688).

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 10)
- fix the texi source
- patch to detect & link against nsl

* Wed Mar 10 1999 Cristian Gafton <gafton@redhat.com>
- use mktemp to handle temporary files.

* Thu Feb 11 1999 Michael Maher <mike@redhat.com>
- fixed bug #365

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Thu Sep 10 1998 Jeff Johnson <jbj@redhat.com>
- compile for 5.2

* Sat Jun 06 1998 Prospector System <bugs@redhat.com>
- translations modified for de

* Sat Jun  6 1998 Jeff Johnson <jbj@redhat.com>
- Eliminate incorrect info page removal.

* Fri May 08 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sat Apr 11 1998 Cristian Gafton <gafton@redhat.com>
- manhattan build
- moved profile.d handling from zshrc to zprofile

* Wed Oct 21 1997 Cristian Gafton <gafton@redhat.com>
- Upgraded to 3.0.5
- Install-info handling

* Thu Jul 31 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Thu Apr 10 1997 Michael Fulbright <msf@redhat.com>
- Upgraded to 3.0.2
- Added 'reasonable' default startup files in /etc
