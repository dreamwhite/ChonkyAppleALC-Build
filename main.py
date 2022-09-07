import argparse
import os
import subprocess
import sys

from shutil import which

# Checks if platform is macOS, if not raises an error
if sys.platform != 'darwin':
    print('ERROR: The following script runs only on macOS')
    sys.exit(1)

parser = argparse.ArgumentParser(description='AppleALC de-chonker')
parser.add_argument('-v', '--verbose', action='store_true',help='Enable verbose')
args = parser.parse_args()

# Checks if the necessary tools are installed
if not os.path.exists('/Applications/Xcode.app/Contents/Developer') or not os.path.exists('/Library/Developer/CommandLineTools'):
    print('ERROR: Xcode does not appear to be installed. Please install it from App Store')
    sys.exit(1)

# If CLI tools are installed, git should be already installed. Probably gonna remove this if
if which('git') == None:
    print('ERROR: git does not appear to be installed. Please install it')
    sys.exit(1)

if not os.path.exists('AppleALC'):
    subprocess.run(['git', 'clone', 'https://github.com/acidanthera/AppleALC'], capture_output=not args.verbose)

os.chdir('AppleALC')
if os.path.exists('AppleALC/kern_resources.cpp'):
    print('Detected kern_resources.cpp. Removing it as it may contain old compressed codecs...\n')
    subprocess.run(['rm','AppleALC/kern_resources.cpp'], capture_output=not args.verbose)

if not os.path.exists('../Kexts'):
    print('Creating Kexts output folder...')
    subprocess.run(['mkdir', '../Kexts'], capture_output=not args.verbose)
else:
    print('Detected Kexts output folder. Removing it as it may contain old built kexts...\n')
    subprocess.run(['rm', '-r', '../Kexts'], capture_output=not args.verbose)

if not os.path.exists('MacKernelSDK'):
    print('WARNING: MacKernelSDK doesn\'t appear to be cloned. Cloning...\n')
    subprocess.run(['git', 'clone', 'https://github.com/acidanthera/MacKernelSDK.git'], capture_output=not args.verbose)

if not os.path.exists('Lilu.kext'):
    print('WARNING: Lilu debug doesn\'t appear to be there. Building...\n')
    subprocess.run(['wget', 'https://raw.githubusercontent.com/acidanthera/Lilu/master/Lilu/Scripts/bootstrap.sh'])
    subprocess.run(['bash', 'bootstrap.sh'])


excluded_dir_files = [
    'Controllers.plist',
    'Kexts.plist.md5',
    'PinConfigs.kext',
    'Controllers.plist',
    'Kexts.plist',
    'Vendors.plist',
    'Vendors.plist.md5'
]

print(os.listdir('Resources'))

codecs = [codec for codec in os.listdir('Resources') if codec not in excluded_dir_files]

for codec in codecs:
    if os.path.exists('AppleALC/kern_resources.cpp'):
        print('Detected kern_resources.cpp. Removing it as it may contain old compressed codecs...\n')
        subprocess.run(['rm','AppleALC/kern_resources.cpp'], capture_output=not args.verbose)
    print(f'Building AppleALC for {codec}...\n')
    command = f'find Resources -type d -not -name {codec} -not -name PinConfigs.kext -not -path Resources/PinConfigs.kext/Contents -not -name Resources | xargs rm -rf {{}};'
    subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    subprocess.run(['xcodebuild', '-project', 'AppleALC.xcodeproj', '-scheme', 'AppleALC', '-configuration', 'Release', '-sdk', 'macosx', '-derivedDataPath', 'out'], capture_output=not args.verbose)
    subprocess.run(['mv', 'out/Build/Products/Release/AppleALC-1.7.4-RELEASE.zip', f'../Kexts/{codec}.zip'], capture_output=not args.verbose)
    subprocess.run(['git', 'reset', '--hard', 'HEAD'], capture_output=not args.verbose)
    #subprocess.run(['rm', '-rf', 'out'], capture_output=not args.verbose)
    subprocess.run(['tree', 'out'])
    sys.exit()