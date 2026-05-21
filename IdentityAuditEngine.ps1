<#
.SYNOPSIS
    Automated Identity Management & Permission Audit Engine
    Built for Illovo Bi-Annual IT Security Requirement.
.DESCRIPTION
    Scans specified directories for unsecure 'Everyone' permissions
    and identifies inactive local user accounts.
#>

# --- CONFIGURATION ---
$ScanPath = "C:\Illovo_Lab"
$ReportDestination = "C:\Illovo_Lab\Security_Audit_Report.csv"
$90DaysAgo = (Get-Date).AddDays(-90)

# --- ARRAY HOLDERS ---
$VulnerabilitiesReport = @()

Write-Host "Starting Bi-Annual IT Security Audit..." -ForegroundColor Yellow

# --- STEP 1: PERMISSION AUDIT ---
Write-Host "Scanning file systems for unsafe ACLs..." -ForegroundColor Gray
if (Test-Path $ScanPath) {
    $Directories = Get-ChildItem -Path $ScanPath -Recurse -Directory
    foreach ($Dir in $Directories) {
        $Acl = Get-Acl -Path $Dir.FullName
        foreach ($Access in $Acl.Access) {
            if ($Access.IdentityReference -eq "Everyone" -or $Access.IdentityReference -eq "BUILTIN\Everyone") {
                $VulnerabilitiesReport += [PSCustomObject]@{
                    AuditType      = "File Permission"
                    Target         = $Dir.FullName
                    Issue          = "Exposed to Everyone"
                    RiskLevel      = "HIGH"
                    Remediation    = "Remove 'Everyone' group and assign explicit group access."
                }
            }
        }
    }
}

# --- STEP 2: USER ACCOUNT HYGIENE AUDIT ---
Write-Host "Auditing user accounts for inactivity..." -ForegroundColor Gray
$LocalUsers = Get-LocalUser
foreach ($User in $LocalUsers) {
    if ($User.LastLogon -and ($User.LastLogon -lt $90DaysAgo)) {
        $VulnerabilitiesReport += [PSCustomObject]@{
            AuditType      = "User Account"
            Target         = $User.Name
            Issue          = "Stale Account (No login for 90+ days)"
            RiskLevel      = "MEDIUM"
            Remediation    = "Disable account and verify employment status."
        }
    }
}

# --- STEP 3: EXPORT RESULTS ---
if ($VulnerabilitiesReport.Count -gt 0) {
    $VulnerabilitiesReport | Export-Csv -Path $ReportDestination -NoTypeInformation
    Write-Host "[SUCCESS] Audit complete. $($VulnerabilitiesReport.Count) vulnerabilities flagged." -ForegroundColor Green
    Write-Host "Report saved to: $ReportDestination" -ForegroundColor Green
} else {
    Write-Host "[SUCCESS] No vulnerabilities found. System secure." -ForegroundColor Green
}