Summary:	Stereo LADSPA effects rack
Name:		jack-rack
Version:	1.4.7
Release:	15
License:	GPL
Group:		X11/Applications/Sound
Source0:	http://downloads.sourceforge.net/jack-rack/%{name}-%{version}.tar.bz2
# Source0-md5:	a29ef4001ee2916a1b758952c936adca
Patch0:		%{name}-deprecated.patch
Patch1:		%{name}-link.patch
Patch2:		%{name}-build.patch
URL:		http://jack-rack.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gtk+-devel
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	ladspa-devel
BuildRequires:	lash-devel
BuildRequires:	liblrdf-devel
BuildRequires:	libxml2-devel
BuildRequires:	pkg-config
Requires:	jack-patch-bay
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
JACK Rack is a stereo LADSPA effects rack for the JACK audio API.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%{__sed} -i "s|/usr/lib/ladspa|%{_libdir}/ladspa|" src/plugin_mgr.c

%build
%{__gettextize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-gnome	\
	--enable-lash=yes
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cat > $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop <<EOF
[Desktop Entry]
Type=Application
Exec=jack-rack
Icon=jack-rack
Terminal=false
Name=JACK Rack
Comment=LADSPA effects rack for JACK
StartupNotify=true
Categories=GTK;Audio;AudioVideo;Midi;
EOF

mv $RPM_BUILD_ROOT%{_pixmapsdir}/{jack-rack-icon,jack-rack}.png

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS BUGS NEWS README THANKS TODO
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{_desktopdir}/*.desktop
# it seems to be the only package using this dir(?)
%dir %{_datadir}/dtds
%{_datadir}/dtds/*.dtd
%{_pixmapsdir}/*.png

