import json
import re
import sys

isystem_armclang_include = ['-isystem /opt/arm/developmentstudio-2023.0/sw/ARMCompiler6.20/lib/clang/17/include']

def extract_info_from_compile_commands(filePath):
    with open(filePath, 'r') as f:
        data = json.load(f)

    # Write to a makefile
    makeFile = open('Makefile', 'w')
    makeFile.write('all:\n')


    for item in data:
        file = item.get('file', '')
        command = item.get('command', '')

        # get defines starting with -D till next space
        defines = re.findall(r'-D[^ ]+', command)
        include_dirs = re.findall(r'-I[^ ]+', command)
        imacros = re.findall(r'-imacros [^ ]+', command)
        macro_prefix_maps = re.findall(r'-fmacro-prefix-map=[^ ]+', command)
        sysroot = re.findall(r'--sysroot=[^ ]+', command)
        isystem = re.findall(r'-isystem [^ ]+', command)
        cpu_info = re.findall(r'-mcpu=[^ ]+', command)
        thumb = re.findall(r'-mthumb', command)

        # # Add '--target=arm-arm-none-eabi -save-temps' to defines
        defines.append('--target=arm-arm-none-eabi -S -save-temps -Wno-error=implicit-function-declaration')

        # print(f'File: {file}')
        # print(f'Defines: {defines}')
        # print(f'Include Directories: {include_dirs}')
        # print(f'iMacros: {imacros}')
        # print(f'Macro Prefix Maps: {macro_prefix_maps}\n')
    
        # run armclang on each file to get bitcode
        armclang_command = ['armclang', file] + defines + include_dirs + imacros + macro_prefix_maps + sysroot + isystem + cpu_info + thumb + isystem_armclang_include
        # make as a string
        armclang_command = ' '.join(armclang_command)
        # print(armclang_command)

        makeFile.write(f'\t{armclang_command}\n')

    # make clean
    makeFile.write('clean:\n')
    makeFile.write('\trm -rf *.i *.s *.o *.bc *.ll *.d\n')

    
if __name__ == "__main__":
    # take compile_commands.json as input from command line
    filePath =  sys.argv[1]
    extract_info_from_compile_commands(filePath)