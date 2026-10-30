$ErrorActionPreference = 'Stop'
$bridgePath = Join-Path $PSScriptRoot 'start_bridge.py'
$scenePath = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..\art\alchemist_hamlet\Lanternbrook_HD2D.blend'))
$existingBridge = Get-NetTCPConnection -LocalPort 9877 -State Listen -ErrorAction SilentlyContinue
if ($existingBridge) {
    Write-Output 'Blender bridge is already listening on localhost:9877.'
    exit 0
}
Start-Process -FilePath 'D:\Programs\blender\blender.exe' -ArgumentList ('"' + $scenePath + '"'), '--python', ('"' + $bridgePath + '"') -WindowStyle Hidden
Write-Output 'Started Blender with the Lanternbrook scene and local MCP bridge.'
