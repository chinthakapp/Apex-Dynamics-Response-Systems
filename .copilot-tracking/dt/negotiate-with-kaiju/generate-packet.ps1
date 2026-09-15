<#
PowerShell script to convert the execution packet Markdown to PDF using Pandoc.
Requires: pandoc + wkhtmltopdf or a PDF engine supported by pandoc.
#>
param(
    [string]$Input = "method-02-execution-packet.md",
    [string]$Output = "method-02-execution-packet.pdf"
)

if (-not (Get-Command pandoc -ErrorAction SilentlyContinue)) {
    Write-Error "pandoc is not installed or not in PATH. Install pandoc to continue."
    exit 2
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

Write-Host "Converting $Input to $Output using pandoc..."
pandoc $Input -o $Output --pdf-engine=wkhtmltopdf
if ($LASTEXITCODE -ne 0) {
    Write-Error "Pandoc conversion failed. Try installing wkhtmltopdf or use pandoc's default engines."
    exit $LASTEXITCODE
}

Write-Host "PDF generated:" (Resolve-Path $Output)
