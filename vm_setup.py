import requests
import platform
import os
import zipfile

linux_ubuntu_tools = f"pipx python3-pip gdb clang llvm openssl efitools sbsigntool mtools wget autoconf automake libssl-dev zlib1g-dev curl qtcreator qtbase5-dev qt5-qmake cmake git build-essential linux-headers-{platform.uname().release} ruby-rubygems qemu-system qemu-utils libvirt-daemon-system libvirt-clients bridge-utils virt-manager"
jdk_25 = "https://download.oracle.com/java/25/latest/jdk-25_linux-x64_bin.deb"
ghidra = "https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_11.3.1_build/ghidra_11.3.1_PUBLIC_20250219.zip"

windows_tools = ["https://download.microsoft.com/download/f335ca28-1861-4b21-b14b-4bac3ec73d7f/KIT_BUNDLE_WINDOWSSDK_MEDIACREATION/winsdksetup.exe", "https://download.microsoft.com/download/768f5d94-c365-4183-b55a-76d9abcebf52/KIT_BUNDLE_WDK_MEDIACREATION/wdksetup.exe", "https://download.sysinternals.com/files/SysinternalsSuite.zip", "https://downloads.sourceforge.net/winmerge/WinMerge-2.16.52.2-x64-Setup.exe", "https://download.visualstudio.microsoft.com/download/pr/7c09e2e8-2b3e-4213-93ab-5646874f8a2b/0ac797413a56c6b2772f48a567a32cdddd3b739f5b2af649fcf90be4245762ff/vs_Community.exe", "https://github.com/git-for-windows/git/releases/download/v2.51.0.windows.2/Git-2.51.0.2-64-bit.exe", "https://www.nasm.us/pub/nasm/releasebuilds/3.01/win64/nasm-3.01-installer-x64.exe", "https://downloadmirror.intel.com/852052/iasl-win-20250404.zip", "https://slproweb.com/download/Win64OpenSSL_Light-3_6_0.exe", "https://github.com/LongSoft/UEFITool/releases/download/A72/UEFIExtract_NE_A72_win64.zip", "https://github.com/winsiderss/systeminformer/releases/download/v3.2.25011.2103/systeminformer-3.2.25011-release-setup.exe", "https://www.osronline.com/OsrDown.cfm/osrloaderv30.zip", "https://download.oracle.com/java/24/latest/jdk-24_windows-x64_bin.exe", "https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_11.3.1_build/ghidra_11.3.1_PUBLIC_20250219.zip"]

def save_file(url, save_as):
    if os.path.exists(save_as):
        return
    r = requests.get(url, stream=True)
    with open(save_as, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)

def extract_zip(file_path):
    name = file_path.split(".")[0]
    if os.path.exists(name):
        return

    print(f"Extracting {file_path}")
    with zipfile.ZipFile(file_path, "r") as z:
        z.extractall(name)

def setup_windows():
    print("Downloading windbg")
    os.system("winget install Microsoft.WinDbg")
    
    for tool in windows_tools:
        name = tool.split("/")[-1]
        print(f"Downloading {name}")
        save_file(tool, name)
        if "zip" in name:
            extract_zip(name)
            
def setup_linux():
    print("Updating system")
    os.system("sudo apt-get update && sudo apt-get upgrade")

    print("Downloading base tools")
    os.system("sudo apt-get install -y " + linux_ubuntu_tools)
    
    print("Downloading pwndbg")
    os.system("curl -qsL 'https://install.pwndbg.re' | sh -s -- -t pwndbg-gdb")
    
    print("Downloading ghidra")
    save_file(jdk_25, jdk_25.split("/")[-1])
    os.system("sudo dpkg -i " + jdk_25.split("/")[-1])
    save_file(ghidra, ghidra.split("/")[-1])
    extract_zip(ghidra.split("/")[-1])
    
    print("Downloading one gadget")
    os.system("sudo gem install one_gadget")

    print("Downloading libc database")
    os.system("git clone https://github.com/niklasb/libc-database.git")

    print("Downloading python packages")
    os.system("pipx ensurepath")
    os.system("pipx install pwntools ROPgadget xortool")
