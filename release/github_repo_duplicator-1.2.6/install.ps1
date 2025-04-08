# PowerShell installation script for GitHub Repo Duplicator

# Function to print colored text
function Write-ColorOutput {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Message,
        [Parameter(Mandatory=$false)]
        [string]$ForegroundColor = "White"
    )
    $originalColor = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    Write-Output $Message
    $host.UI.RawUI.ForegroundColor = $originalColor
}

Write-ColorOutput "==============================================" "Green"
Write-ColorOutput "    GitHub Repo Duplicator Installation       " "Green"
Write-ColorOutput "==============================================" "Green"

# Check for Python
Write-ColorOutput "`nChecking for Python..." "Yellow"
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python 3") {
        Write-ColorOutput "Python 3 found!" "Green"
        $pythonCmd = "python"
    } else {
        Write-ColorOutput "Error: Python 3 is required but $pythonVersion was found." "Red"
        Write-ColorOutput "Please install Python 3 and try again." "Yellow"
        exit 1
    }
} catch {
    try {
        $pythonVersion = py -3 --version 2>&1
        Write-ColorOutput "Python 3 found using py launcher!" "Green"
        $pythonCmd = "py -3"
    } catch {
        Write-ColorOutput "Error: Python 3 is required but not found." "Red"
        Write-ColorOutput "Please install Python 3 from https://www.python.org/downloads/" "Yellow"
        exit 1
    }
}

# Check for Git
Write-ColorOutput "`nChecking for Git..." "Yellow"
try {
    $gitVersion = git --version 2>&1
    Write-ColorOutput "Git found!" "Green"
} catch {
    Write-ColorOutput "Error: Git is required but not found." "Red"
    Write-ColorOutput "Please install Git from https://git-scm.com/download/win" "Yellow"
    exit 1
}

# Check if user is authenticated with GitHub
Write-ColorOutput "`nChecking GitHub authentication..." "Yellow"
try {
    $gitName = git config user.name
    $gitEmail = git config user.email
    if ($gitName -and $gitEmail) {
        Write-ColorOutput "GitHub user configuration found:" "Green"
        Write-ColorOutput "Username: $gitName"
        Write-ColorOutput "Email: $gitEmail"
    } else {
        throw "GitHub user not configured"
    }
} catch {
    Write-ColorOutput "Error: GitHub user configuration not found." "Red"
    Write-ColorOutput "Please configure Git with your GitHub credentials:" "Yellow"
    Write-ColorOutput 'git config --global user.name "Your Name"'
    Write-ColorOutput 'git config --global user.email "your.email@example.com"'
    exit 1
}

# Installation method selection
Write-ColorOutput "`nHow would you like to install GitHub Repo Duplicator?" "Yellow"
Write-ColorOutput "1) Install as a Python package"
Write-ColorOutput "2) Build an executable"
Write-ColorOutput "3) Run directly from source (no installation)"

$installOption = Read-Host "Select an option [1-3]"

switch ($installOption) {
    "1" {
        Write-ColorOutput "`nInstalling as a Python package..." "Yellow"
        Invoke-Expression "$pythonCmd -m pip install -e ."
        
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "`nInstallation successful!" "Green"
            Write-ColorOutput "You can now run the tool with the command: github-repo-duplicator" "Yellow"
        } else {
            Write-ColorOutput "`nInstallation failed." "Red"
            exit 1
        }
    }
    "2" {
        Write-ColorOutput "`nBuilding executable..." "Yellow"
        
        # Check for PyInstaller
        $pyinstallerInstalled = $pythonCmd + " -m pip show pyinstaller"
        try {
            Invoke-Expression $pyinstallerInstalled | Out-Null
        } catch {
            Write-ColorOutput "PyInstaller not found. Installing..." "Yellow"
            Invoke-Expression "$pythonCmd -m pip install pyinstaller"
        }
        
        # Build the executable
        Invoke-Expression "$pythonCmd -m PyInstaller --onefile --name github_repo_duplicator duplicate_repo.py"
        
        if ($LASTEXITCODE -eq 0) {
            $exePath = (Get-Location).Path + "\dist\github_repo_duplicator.exe"
            Write-ColorOutput "`nBuild successful!" "Green"
            Write-ColorOutput "The executable is available at: $exePath" "Yellow"
            
            # Offer to add to PATH
            $addToPath = Read-Host "Do you want to add the executable to your PATH? (y/n)"
            if ($addToPath -eq "y" -or $addToPath -eq "Y") {
                $userPath = [Environment]::GetEnvironmentVariable("Path", "User")
                $distDir = (Get-Location).Path + "\dist"
                
                if (-not $userPath.Contains($distDir)) {
                    [Environment]::SetEnvironmentVariable("Path", $userPath + ";" + $distDir, "User")
                    Write-ColorOutput "Added to PATH. You may need to restart your PowerShell session." "Green"
                } else {
                    Write-ColorOutput "Directory is already in PATH." "Yellow"
                }
            }
        } else {
            Write-ColorOutput "`nBuild failed." "Red"
            exit 1
        }
    }
    "3" {
        Write-ColorOutput "`nRunning from source..." "Yellow"
        Write-ColorOutput "No installation required." "Green"
        Write-ColorOutput "You can run the tool with: $pythonCmd duplicate_repo.py" "Yellow"
        
        # Offer to create a shortcut
        $createShortcut = Read-Host "Do you want to create a desktop shortcut? (y/n)"
        if ($createShortcut -eq "y" -or $createShortcut -eq "Y") {
            $WshShell = New-Object -comObject WScript.Shell
            $Shortcut = $WshShell.CreateShortcut($env:USERPROFILE + "\Desktop\GitHub Repo Duplicator.lnk")
            $Shortcut.TargetPath = $pythonCmd
            $Shortcut.Arguments = """" + (Get-Location).Path + "\duplicate_repo.py" + """"
            $Shortcut.WorkingDirectory = (Get-Location).Path
            $Shortcut.Save()
            
            Write-ColorOutput "Desktop shortcut created!" "Green"
        }
    }
    default {
        Write-ColorOutput "`nInvalid option. Exiting." "Red"
        exit 1
    }
}

Write-ColorOutput "`n==============================================" "Green"
Write-ColorOutput "  GitHub Repo Duplicator Setup Complete!      " "Green"
Write-ColorOutput "==============================================" "Green" 