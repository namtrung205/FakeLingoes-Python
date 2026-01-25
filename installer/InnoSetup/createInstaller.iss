[Setup]
AppName=Navisworks Cim Tools.TTD
AppVersion=1.0
DefaultDirName="C:\ProgramData\Autodesk\ApplicationPlugins\NavisworksCimToolsApp.TTD.bundle"
DefaultGroupName=Navisworks Cim Tools
OutputDir= "../"
OutputBaseFilename= NavisworksCimToolsInstaller

UninstallDisplayIcon=../Resources/Icons/tt.ico

[Files]
Source: "C:\ProgramData\Autodesk\ApplicationPlugins\NavisworksCimToolsApp.TTD.bundle\*"; 
DestDir: "C:\ProgramData\Autodesk\ApplicationPlugins\NavisworksCimToolsApp.TTD.bundle"; 
Flags: ignoreversion recursesubdirs createallsubdirs; 

[Code]
function GetProgramData(Param: string): string;
begin
  Result := ExpandConstant('{pf}') + '\..';  // Returns the path for %ProgramData%
end;
