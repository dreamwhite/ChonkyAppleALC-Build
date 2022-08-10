# ChonkyAppleALC

## AppleALC layout list

The following is an auto-generated list of AppleALC layout IDs available per each codec.

Open the relevant `.md` file inside the vendor folder (e.g. `ALC236` vendor is Realtek)

The following guide will help you light that chonk `AppleALC.kext`
## Requirements

- [XCode](https://developer.apple.com/xcode/)
- [MacKernelSDK](https://github.com/acidanthera/MacKernelSDK)

## How to proceed

After making sure that `AppleALC` stock kext works without any additional edit you can light the kext from ~ 3.7MB to 600KB :)

### Identify your codec

Do I really need to explain how to identify your codec? If you don't know it, use [Hackintool](https://github.com/headkaze/Hackintool) or check your codec dump via OpenCorePkg SysReport feature, like [this](https://github.com/dreamwhite/dell-inspiron-5370-hackintosh/blob/c8e6abd9207414e9073fa9ccc84eca4b8d21d220/Docs/SysReport/SysReport/Audio/Codec0.txt#L4).

![](/.assets/images/hackintool.png)

In my case, my audio codec `ALC295`

### Slim that fat boi AppleALC

1. Clone AppleALC and open the source project
2. Remove `kern_resources.cpp` from `$(source)/AppleALC` as it contains already compiled resources
3. Remove every codec folder in `$(source)/Resources` except:
    - the one which name starts with the previously identified codec name (e.g. in my case `ALC295`)
    - `PinConfigs.kext`
    - `Controllers.plist`
    - `Kexts.plist`
    - `Vendors.plist`

![](/.assets/images/resources.png)

4. Clone MacKernelSDK onto `$(source)` with `git clone https://github.com/acidanthera/MacKernelSDK.git`.
5. Run `wget https://raw.githubusercontent.com/acidanthera/Lilu/master/Lilu/Scripts/bootstrap.sh && bash bootstrap.sh` onto `$(source)`
6. Open XCode and build the project with `Release` configuration using `⇧⌘R` and after it finishes building the project, replace the old `AppleALC.kext` with the newly generated

# How to generate every kext with a single codec

Run `python3 main.py` and see the magic happen.
Created kexts will be in `Kexts` folder

# Issues

If you encounter any issue, please file a bugreport [here](https://github.com/dreamwhite/bugtracker/issues/new?assignees=dreamwhite&labels=bug&template=generic.md&title=)

# Credits

- [Apple](https://apple.com) for [XCode](https://developer.apple.com/xcode/)
- [Acidanthera](https://github.com/acidanthera) for [AppleALC](https://github.com/acidanthera/AppleALC) and [MacKernelSDK](https://github.com/acidanthera/MacKernelSDK)
