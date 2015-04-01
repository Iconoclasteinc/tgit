#define MyAppName "TGiT"
#define MyAppVersion "1.2.3"
#define MyAppPublisher "Iconoclaste Musique, Inc."
#define MyAppURL "http://www.tagyourmusic.com/"
#define MyAppExeName "tgit.exe"
#define SourcePath "C:\Users\Jonathan\Documents\Code\tgit"

[Setup]
AppId={{B880DBE7-A29E-4869-A0F9-DE07ED1348B3}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=build
OutputBaseFilename="{#MyAppName}-{#MyAppVersion}"
Compression=lzma
SolidCompression=yes
SetupIconFile={#SourcePath}\tgit.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"; LicenseFile: "license.txt"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"; LicenseFile: "license-fr.txt"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 0,6.1

[Files]
Source: "{#SourcePath}\build\exe.win-amd64-3.4\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
