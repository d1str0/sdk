"""
Build the various language SDK packages for release
"""
import argparse
import glob
import logging
import os
import platform
import shutil
from os.path import join, abspath, dirname, isdir, split
import subprocess
from typing import Dict

try:
    import requests
except:
    os.system('pip install requests')
    import requests


def parse_version_tag():
    raise NotImplementedError


def get_os_arch_path(extract_dir, windows_path):
    copy_from = ''
    libs_dir = join(extract_dir, 'libs')
    os_name = platform.system().lower()
    processor_name = platform.machine().lower()
    if os_name == 'windows':
        copy_from = join(libs_dir, windows_path)
    elif os_name == 'linux':
        if processor_name == 'x86_64':
            copy_from = join(libs_dir, 'linux')
        elif processor_name == 'armv7l':
            copy_from = join(libs_dir, 'linux-armv7')
        elif processor_name == 'aarch64':
            copy_from = join(libs_dir, 'linux-aarch64')
    elif os_name == 'darwin':
        copy_from = join(libs_dir, 'macos')
    return copy_from


def copy_okapi_libs(copy_to: str, windows_path='windows'):
    okapi_dir = abspath(join(dirname(__file__), '..'))
    copy_from = get_os_arch_path(okapi_dir, windows_path)
    logging.info(f"Copying okapi libs from: {copy_from}\nto: {copy_to}")

    for copy_file in glob.glob(join(copy_from, '*.*')):
        shutil.copy2(copy_file, copy_to)
    try:
        shutil.copy2(join(okapi_dir, 'libs', 'C_header', 'okapi.h'), copy_to)
    except FileNotFoundError:
        pass


def clean_dir(language_dir: str) -> None:
    logging.info(f"Cleaning directory={language_dir}")
    try:
        shutil.rmtree(language_dir)
    except FileNotFoundError:
        pass
    os.mkdir(language_dir)



def update_line(file_name: str, replace_lines: Dict[str, str]) -> None:
    with open(file_name, 'r') as fid:
        file_lines = fid.readlines()

    file_lines = list(map(lambda x: replace_line_if_needed(x, replace_lines), file_lines))

    with open(file_name, 'w') as fid2:
        fid2.writelines(file_lines)


def replace_line_if_needed(line: str, replace_lines: Dict[str, str]) -> str:
    for find, replace in replace_lines.items():
        if line.strip().startswith(find.strip()):
            line = replace + '\n'
    return line


def get_language_dir(language_name: str) -> str:
    """
    Get the directory for the given language SDK
    :param language_name: The language directory
    :return: Absolute path to the given language SDK
    """
    return abspath(join(dirname(abspath(__file__)), '..', language_name))


def get_sdk_dir() -> str:
    """Get the full path of the root of the sdk repository"""
    return abspath(join(dirname(abspath(__file__)), '..'))


def build_python(args) -> None:
    # Update version in setup.cfg
    python_dir = get_language_dir('python')
    update_line(join(python_dir, 'setup.cfg'),
                {'version = ': f'version = {get_package_versions(args)}'})
    copy_okapi_libs(abspath(join(python_dir, '..', 'libs')))


def build_java(args) -> None:
    # Update version in setup.cfg
    java_dir = get_language_dir('java')
    update_line(join(java_dir, 'build.gradle'),
                {'def jarVersion': f'def jarVersion = "{get_package_versions(args)}"'})
    copy_okapi_libs(abspath(join(java_dir, '..', 'libs')))


def build_ruby(args) -> None:
    # Update version in setup.cfg
    ruby_dir = get_language_dir('ruby')
    update_line(join(ruby_dir, 'lib', 'version.rb'),
                {'  VERSION =': f"  VERSION = '{get_package_versions(args)}'"})
    copy_okapi_libs(abspath(join(ruby_dir, '..', 'libs')))
    copy_okapi_libs(ruby_dir)  # Ruby FFI loads from current directory first, this enables macos


def build_golang(args) -> None:
    # Update version in setup.cfg
    golang_dir = abspath(join(get_language_dir('go'), 'services'))
    # Copy in the binaries
    copy_okapi_libs(golang_dir, 'windows-gnu')


def get_package_versions(args) -> str:
    return (args.package_version or get_github_version()).lstrip('v')


def get_github_version(github_token: str = None) -> str:
    if not github_token:
        github_token = os.getenv('API_GITHUB_TOKEN')
    github_release_request = requests.get('https://api.github.com/repos/trinsic-id/okapi/releases/latest',
                                          headers={'Authorization': github_token})
    github_json = github_release_request.json()
    version = github_json['tag_name']
    return version


def build_java_docs(args):
    # https://github.com/fchastanet/groovydoc-to-markdown
    # npm install in the root of sdk
    subprocess.Popen(r'node ./node_modules/groovydoc-to-markdown/src/doc2md.js  ./java java ./docs/reference/java', cwd=get_sdk_dir() ).wait()


def build_dotnet_docs(args) -> None:
    # https://github.com/Doraku/DefaultDocumentation
    # dotnet tool install DefaultDocumentation.Console -g
    assembly_file = './dotnet/Trinsic/bin/Debug/net6.0/Trinsic.dll'
    output_doc_folder = './docs/reference/dotnet'
    clean_dir(abspath(join(get_sdk_dir(), output_doc_folder)))
    subprocess.Popen(f"defaultdocumentation --AssemblyFilePath {assembly_file} --OutputDirectoryPath {output_doc_folder} --FileNameMode Name --GeneratedPages Namespaces",
                     cwd=get_sdk_dir()).wait()


def build_go_docs(args):
    # https://github.com/posener/goreadme
    # go get github.com/posener/goreadme/cmd/goreadme
    goreadme_args = r'-recursive -functions -methods -types -variabless'  # Yes, that's a duplicated s, it's on purpose.
    doc_path = abspath(join(get_language_dir('docs'), 'reference', 'go'))

    def write_doc_file(input_path: str, output_file: str):
        logging.info(f"goreadme(input={input_path}, output={output_file})")
        with open(join(doc_path, f'{output_file}.md'), 'w') as output:
            subprocess.Popen(rf'goreadme {goreadme_args}', cwd=input_path, stdout=output).wait()
        # Handle the subdirectories
        for sub_folder in glob.glob(join(input_path, '**')):
            if isdir(sub_folder):
                _, folder_name = split(sub_folder)
                write_doc_file(sub_folder, folder_name)
    
    write_doc_file(get_language_dir('go'), 'index')


def parse_arguments():
    parser = argparse.ArgumentParser(description='Process SDK building')
    parser.add_argument('--package-version', help='Manual override package version')
    parser.add_argument('--language', help='Comma-separated languages to build', default='all')
    return parser.parse_args()


def main():
    # Get command line arguments
    args = parse_arguments()
    langs_to_build = [lang.lower() for lang in (args.language + ',').split(',')]
    build_all = 'all' in langs_to_build
    # Update version information
    if build_all or 'python' in langs_to_build:
        build_python(args)
    if build_all or 'java' in langs_to_build:
        build_java(args)
    if build_all or 'ruby' in langs_to_build:
        build_ruby(args)
    if build_all or 'golang' in langs_to_build:
        build_golang(args)
    if build_all or 'docs' in langs_to_build:
        build_java_docs(args)
        build_dotnet_docs(args)
        build_go_docs(args)


if __name__ == "__main__":
    main()
