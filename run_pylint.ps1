Get-ChildItem -Path @(".", "./game_files") -Filter *.py | % {$_.FullName} |
ForEach-Object {
    pylint $_
}