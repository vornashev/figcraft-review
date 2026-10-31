; FigCraft Review's Windows installer (Inno Setup 6). scripts/package.py windows-app compiles it with
; /DVersion=X.Y.Z /DSource=<the staged app: python\, app\, bin\> /DOutput=<dist>.
; Per user, no admin rights. An update (agent/update.py) runs it with /SILENT and starts the app itself afterwards.

#ifndef Version
  #error Pass /DVersion=X.Y.Z
#endif

[Setup]
AppId={{8B5E2C1A-6F3D-4E7B-9A21-F1C0D4E5B6A7}
AppName=FigCraft Review
AppVersion={#Version}
AppVerName=FigCraft Review {#Version}
AppPublisher=vornashev
AppPublisherURL=https://github.com/vornashev/figcraft-review
AppUpdatesURL=https://github.com/vornashev/figcraft-review/releases
DefaultDirName={localappdata}\Programs\FigCraft Review
DisableProgramGroupPage=yes
DisableDirPage=yes
PrivilegesRequired=lowest
OutputDir={#Output}
OutputBaseFilename=FigCraftReview-Setup-v{#Version}
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\icon.ico
UninstallDisplayName=FigCraft Review
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
ChangesEnvironment=yes
CloseApplications=force
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "ru"; MessagesFile: "compiler:Languages\Russian.isl"
Name: "en"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "startup"; Description: "Запускать при входе в систему"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[InstallDelete]
; an update replaces the code and the runtime whole, so removed files don't linger; chats and settings live elsewhere
Type: filesandordirs; Name: "{app}\app"
Type: filesandordirs; Name: "{app}\python"

[UninstallDelete]
; bytecode Python wrote while the app ran (Inno removes only the files it installed)
Type: filesandordirs; Name: "{app}\app"
Type: filesandordirs; Name: "{app}\python"

[Files]
Source: "{#Source}\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\FigCraft Review"; Filename: "{app}\python\pythonw.exe"; Parameters: """{app}\app\sidecar\app.py"""; WorkingDir: "{app}"; IconFilename: "{app}\icon.ico"
Name: "{autodesktop}\FigCraft Review"; Filename: "{app}\python\pythonw.exe"; Parameters: """{app}\app\sidecar\app.py"""; WorkingDir: "{app}"; IconFilename: "{app}\icon.ico"; Tasks: desktopicon
Name: "{userstartup}\FigCraft Review"; Filename: "{app}\python\pythonw.exe"; Parameters: """{app}\app\sidecar\app.py"""; WorkingDir: "{app}"; IconFilename: "{app}\icon.ico"; Tasks: startup

[Registry]
; figcraft-review / figcraft-agent for hotkeys and agents outside the chat
Root: HKCU; Subkey: "Environment"; ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}\bin"; Check: NeedsAddPath(ExpandConstant('{app}\bin'))

[Run]
Filename: "{app}\python\pythonw.exe"; Parameters: """{app}\app\sidecar\app.py"""; WorkingDir: "{app}"; Description: "Запустить FigCraft Review"; Flags: postinstall nowait skipifsilent

[UninstallRun]
Filename: "{app}\python\python.exe"; Parameters: """{app}\app\sidecar\app.py"" --quit"; Flags: runhidden waituntilterminated; RunOnceId: "StopApp"

[Code]
function NeedsAddPath(Dir: string): Boolean;
var
  Path: string;
begin
  if not RegQueryStringValue(HKCU, 'Environment', 'Path', Path) then
    Path := '';
  Result := Pos(';' + Uppercase(Dir) + ';', ';' + Uppercase(Path) + ';') = 0;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  Path, Dir: string;
  P: Integer;
begin
  if CurUninstallStep <> usPostUninstall then
    exit;
  Dir := ExpandConstant('{app}\bin');
  if RegQueryStringValue(HKCU, 'Environment', 'Path', Path) then
  begin
    P := Pos(';' + Uppercase(Dir), Uppercase(Path));
    if P > 0 then
    begin
      Delete(Path, P, Length(Dir) + 1);
      RegWriteExpandStringValue(HKCU, 'Environment', 'Path', Path);
    end;
  end;
end;
