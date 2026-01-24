[Setup]
                    AppName=RevitAddinApp.TTD
                    AppVersion=7.0.0
                    DefaultDirName="C:\ProgramData\Autodesk\ApplicationPlugins\RevitAddinApp.bundle"
                    DefaultGroupName=RevitAddinApp
                    OutputDir= "C:\Users\C.DES.011\Desktop\Private\Dev\Code Base TTD\RevitCodeBaseApp\output"
                    OutputBaseFilename= RevitAddinApp


                    [Files]
                    Source: "C:\Users\C.DES.011\Desktop\Private\Dev\Code Base TTD\RevitCodeBaseApp\output\RevitAddinApp\*"; DestDir: "C:\ProgramData\Autodesk\ApplicationPlugins\RevitAddinApp.bundle"; Flags: ignoreversion recursesubdirs createallsubdirs; 

                    [Code]
                    function GetProgramData(Param: string): string;
                    begin
                      Result := ExpandConstant('{pf}') + '\..';  // Returns the path for %ProgramData%
                    end;