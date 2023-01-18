url_7za         = r'https://www.7-zip.org/a/7za920.zip'
url_mingw       = r'https://jaist.dl.sourceforge.net/project/mingw-w64/Toolchains%20targetting%20Win64/Personal%20Builds/rubenvb/gcc-4.5-release/x86_64-w64-mingw32-gcc-4.5.4-release-win64_rubenvb.7z'
url_sdl         = r'http://www.libsdl.org/release/SDL-devel-1.2.15-VC.zip'
url_curl        = r'https://curl.se/download/curl-7.64.1.zip'

from tool import *

def main():
    if is_admin() == False:
        print('[*] Error: Please run this script on the root privilege')
        exit(1)

    if is_test_mode() == False:
        print('[*] Error: Please run this script on the test mode')
        exit(1)
    if os.path.exists(path_vbox_dir) == False:
        print(f'[*] Error: Please copy to {path_vbox_dir} the source of VirtualBox to compile')
        exit(1)

    # Download pre-requisites
    print('[+] Set up libraries')
    if create_folder(f'{path_main_dir}/7za'):
        print('[-] Download 7za')
        extract_to(url_7za, f'{path_main_dir}/7za', True)
    if create_folder(f'{path_main_dir}/MinGW'):
        print('[-] Download MinGW')
        extract_to(url_mingw, f'{path_main_dir}/MinGW')
    if create_folder(f'{path_main_dir}/SDL'):
        print('[-] Download SDL')
        extract_to(url_sdl, f'{path_main_dir}/SDL')
        shutil.copytree(f'{path_main_dir}/SDL/SDL-1.2.15/include', f'{path_main_dir}/SDL/include')
        shutil.copytree(f'{path_main_dir}/SDL/SDL-1.2.15/lib/x64', f'{path_main_dir}/SDL/lib')
    if create_folder(f'{path_main_dir}/curl'):
        print('[-] Download cURL')
        extract_to(url_curl, f'{path_main_dir}/curl')
    
    # Run batch scripts
    os.chdir(path_curr_dir)
    execute_batch_x32('build_x32.bat')
    execute_batch_x64('build_x64.bat')
    
    os.chdir(path_curr_dir)
    # Register certification
    flag = True
    if os.path.exists('mytestcert.cer'):
        yesno = input("[Q] The certification for drivers already exists. If you create a new certification, it might lead to some conflictions. Do you want to skip? (y)").lower()
        if yesno == 'y':
            flag = False
    if flag:
        execute_batch_x32('build_driver.bat')

    # Configure VBox build
    execute_batch_x32('build_vbox.bat')

    # Copy local config
    os.chdir(path_vbox_dir)
    shutil.copy(f'{path_curr_dir}/LocalConfig.kmk', path_vbox_dir)

if __name__ == '__main__':
    main()
