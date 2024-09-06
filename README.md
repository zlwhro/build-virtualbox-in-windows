# Build VirtualBox in Windows

## Notice  
Based on [this repository](https://github.com/st424204/build-virtualbox-in-windows). Currently works for VirtualBox 7.0.6.  

## Setup Environment

* [Visual Studio 2019 Professional](https://learn.microsoft.com/en-us/visualstudio/releases/2019/release-notes)
* Windows SDK 11 & WDK 11
    * winget install --source winget --exact --id Microsoft.WindowsSDK.10.0.26100
    * winget install --source winget --exact --id Microsoft.WindowsWDK.10.0.26100
    
* [WinSDK 7.1](https://www.microsoft.com/en-us/download/details.aspx?id=8279)
    * Needed for `kmk packing`
    * Install into default path
    * If install failed, check out [this reference](https://notepad.patheticcockroach.com/1666/installing-visual-c-2010-and-windows-sdk-for-windows-7-offline-installer-and-installation-troubleshooting/)

* [Zip for Windows](https://gnuwin32.sourceforge.net/packages/zip.htm)
    * Needed for `kmk packing`
    * Install into default path

* [WIX3](https://github.com/wixtoolset/wix3/releases)
    * Needed for `kmk packing`
    * Download `wix311-binaries.zip`
    * Extract the file into `C:\VBoxBuild\wix311`

* [WinDDK 7.1](https://www.microsoft.com/en-us/download/details.aspx?displaylang=en&id=11800)
* [Yasm](https://yasm.tortall.net/Download.html)
    * Download `Win64.exe`, rename it to `yasm.exe`. Set the PATH env so `yasm.exe` can be found in PATH.
* Qt
    * [Online installer](https://d13lb3tujbc8s0.cloudfront.net/onlineinstallers/qt-unified-windows-x64-4.5.1-online.exe)
    * Use the installer to install Qt. You need to register an account first
    * Install the prebuild version ( `v5.15.2`, `MSVC 2019 64 bit` )
    * When it ask you the install path, set it to `C:\VBoxBuild\Qt`

* MinGW
    * In this repo `setup.py` will install and build mingw for you, but you need to add `C:\VBoxBuild\MinGW\mingw64\bin` in the PATH env.

## How to build

Before building, you'll have to patch the source code in `src\VBox\Runtime\common\ldr\ldrPE.cpp:4812`:  

```C
// Goto line 4812
// Make sure you patch it into the following lines:
    if (   fNewerStructureHack
            && Dir.Size > cbMaxKnown
            && !(fFlags & (RTLDR_O_FOR_DEBUG | RTLDR_O_FOR_VALIDATION)) && 0)
            //&& !ASMMemIsZero(&u.abZeros[cbMaxKnown], Dir.Size - cbMaxKnown))
        {

```
Patch the source code so later it won't ran into error saying `Fail to load VMMR0.r0....`

After that, the building steps are bascially the same as the [original](#2-set-up-privilege) :  
* Turn on test mode, reboot.  
* Make sure the VirtualBox source code is in `C:/VBoxBuild/VirtualBox/`.  
* Open cmd as admin.
* `py script/setup.py`
* `py script/build.py`  
    - This will do `kmk` and `kmk packing`, which will create an installer ( `.msi` file ) in `C:\VBoxBuild\VirtualBox\out\win.amd64\release\obj\Installer\win`.

### Troubleshooting  
* Make sure to delete all the certificates named `MyTestCertificate` before building ( check the [FAQ](#faq) below ).  
* During the first build, it probably will run into error saying something like `No making rule for VBoxGuestAdditions.iso`. All you need to do is:  
    - `mkdir C:/VBoxBuild/VirtualBox/out/win.amd64/release/bin/additions/`  
    - `touch C:/VBoxBuild/VirtualBox/out/win.amd64/release/bin/additions/VBoxGuestAdditions.iso`  
    - Rerun `setup.py` and `build.py` ( don't forget to delete the certificate first )


## Install and run VirtualBox
* **Install the official VirtualBox first.** This will installed the required library and solve some weird issues.
* After making sure the official VirtualBox can run normally, install the self-build version of VirtualBox ( use the `msi` installer ). The installer will replace the one in `C:\Program Files\Oracle\VirtualBox`.
* Copy `libcurl.dll` in `C:\VBoxBuild\curl\x64`, place it under `C:\Program Files\Oracle\VirtualBox` so our VirtualBox can launch.
* Now open VirtualBox. If you're lucky enough you should see it launched successfully.


***
( The following content is the original README.md )
***

## Introduction

[This repository](https://github.com/VirtualBoBs/build-virtualbox-in-windows) provides a set of scripts which will help you compile VirtualBox easily.

You can find the official manual to compile VirtualBox in Windows from [the official site](https://www.virtualbox.org/wiki/Windows%20build%20instructions), but it's too obsolete to follow at this time. So, we wrote python scripts which prepare required libraries for compilation, and compile VirtualBox automatically.

What you need to do is only to install pre-requisites for the compilation, and run the scripts.

## Features

- It downloads or compiles the followings: 7-Zip, MinGW, SDL, SSL, cURL, Qt5
- It creates and registers a credential which is needed to compile drivers in Windows.
- It manages dependencies in the compilation.
- It compiles VirtualBox binaries.

## Requirement

- Windows 10
- Python (≥ 3.8)
- Enough spaces (at least 20GB)

## Building

To build VirtualBox via the scripts, you should follow the steps below.

### 1. Set Up Environment

Before using the scripts, you need to install the followings.

- Visual Studio 2010 (Tested on **Professional**)
- [Visual Studio 2010 SP1](https://kovepg.tistory.com/entry/비주얼-스튜디오-2010-서비스팩1Visual-Studio-2010-SP1-설치파일)
- [WinSDK 7.1](https://www.microsoft.com/en-us/download/details.aspx?id=8279)
- [WinSDK 8.1](https://developer.microsoft.com/ko-kr/windows/downloads/sdk-archive/)
- [WinDDK 7.1](https://www.microsoft.com/en-us/download/details.aspx?displaylang=en&id=11800)
- [SSL 32bit](https://slproweb.com/download/Win32OpenSSL-1_1_1i.exe)
- [SSL 64bit](https://slproweb.com/download/Win64OpenSSL-1_1_1i.exe)

If at least one of them is not installed properly, you could be in trouble with compile errors afterwards. And, we recommend you install them **in their default paths**.

### 2. Set Up Privilege

Before going into any steps, you should satisfy the followings:

- Test Mode
- Root Privilege

You can turn on the test mode with the following:

```cmd
bcdedit /set testsigning on
```

Note that **you MUST reboot your PC** when you turned on the test mode **for the first time**.

And, you should execute any scripts in this repository **with root-privilege(Administrator)**. Unless, you will confront unexpected issues afterwards.

### 3. Download Source of VirtualBox

You should download from [the official site](https://www.virtualbox.org/wiki/Downloads) the sources of VirtualBox, which you want to compile. And copy the sources into `C:/VBoxBuild/VirtualBox`. Scripts will use `C:/VBoxBuild` as a default working directory for compilation.

### 4, Clone This Repository

Clone this repository via:

```cmd
git clone https://github.com/VirtualBoBs/build-virtualbox-in-windows.git
```

### 5. Run Setup Script

Run `script/setup.py`.

It will configure all the requirements for your compilation.

### 6. Run Build Script

Run `script/build.py`.

Please make sure that **the prior setup stage has been accomplished**.

It will build the components of VirtualBox. You can find the compiled binaries in `C:/VBoxBuild/VirtualBox/out/win.amd64/release/bin`.

If you've finished Step 1~5, building the binaries needs **Step 6 only**.

## Usage

### Run VirtualBox

When you run the GUI version of VirtualBox(`VirtualBox.exe`), you need dynamic libraries of both Qt and cURL library. You can run it via:

```cmd
SET PATH=%PATH%;C:\VBoxBuild\Qt\qt5-x64\bin
SET PATH=%PATH%;C:\VBoxBuild\curl\x64

C:\VBoxBuild\VirtualBox\out\win.amd64\release\bin\VirtualBox.exe
```

### Debug VirtualBox

The default setting provides disabled-hardening on the VirtualBox binary, so you can attach any kind of debugger on the running process of compiled VirtualBox.

## FAQ

### Q) I keep getting an error in `SignTool`: `Multiple certificates were found that meet all the given criteria.`

A) Unfortunately, now our script does not handle multiple certificates being generated during the Setup step. You need to run it only once unlike the Build step. And here is the solution:

1. Run `certmgr.msc`
2. Delete **all the certificates** named `MyTestCertificate` in the `Certificates - Personal`
3. Start from the Setup step.


## Bug Reporting

We use Github Issue as its primary upstream bug tracker. Bugs found when running scripts should be reported via:

- [https://github.com/VirtualBoBs/build-virtualbox-in-windows/issues](https://github.com/VirtualBoBs/build-virtualbox-in-windows/issues)

Especially, let us know if you can not download files automatically in the scripts. Old URLs in the scripts might be the causes.

## Contact

You can contact us via:

- Send a mail via a leg of bird
- Use our common telepathy
- Wish to God your genuine belief

Or, well, just e-mail us :p

## License

Copyright (c) 2020 JungHyun Kim & JaeSeung Lee of VirtualBoBs

Released under the [MIT license](https://tldrlegal.com/license/mit-license).
