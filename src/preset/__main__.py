import collections
import os
import sys
import tempfile
import shutil
import subprocess

Preset = collections.namedtuple('Preset', ['collection', 'playbook'])

USERDIR = os.environ['USER_PWD']
PYTHONBIN = os.environ['PYTHONBIN']


def parse_preset():
    args = sys.argv[1:]
    collection = args[0]
    if len(args) == 1:
        return Preset(collection, None)
    elif len(args) == 2:
        return Preset(collection, args[1])
    else:
        raise ValueError('Invalid number of arguments')


def execute(workspace):
    ansible = os.path.join(PYTHONBIN, 'ansible-playbook')
    playbook = os.path.join(workspace, 'playbook.yml')

    rc = subprocess.run(
        f'{ansible} {playbook}',
        cwd=workspace,
        shell=True,
        stdout=sys.stdout,
        stderr=sys.stderr,
        bufsize=1
    ).returncode
    print(f'Ansible return code: {rc}')

    return 0


def process(workspace, preset):
    print(f'Workspace: {workspace}')
    print(f'Processing: {preset}')

    if os.path.isabs(preset.collection):
        collection = preset.collection
    else:
        collection = os.path.join(USERDIR, preset.collection)

    if not (os.path.exists(collection) and os.path.isdir(collection)):
        raise FileNotFoundError(f'Collection not found: {collection}')

    if not os.access(collection, os.R_OK):
        raise PermissionError(f'Collection is not readable: {collection}')

    if os.path.isabs(preset.playbook):
        playbook = preset.playbook
    else:
        playbook = os.path.join(USERDIR, preset.playbook)

    if not (os.path.exists(playbook) and os.path.isfile(playbook)):
        raise FileNotFoundError(f'Playbook not found: {playbook}')

    if not os.access(playbook, os.R_OK):
        raise PermissionError(f'Playbook is not readable: {playbook}')

    print(f'Collection: {collection}\n'
          f'Playbook: {playbook}')

    shutil.copytree(os.path.join(collection, 'roles'), os.path.join(workspace, 'roles'))
    shutil.copy2(playbook, os.path.join(workspace, 'playbook.yml'))

    os.makedirs(os.path.join(workspace, 'host_vars'), exist_ok=True)
    with open(os.path.join(workspace, 'host_vars', 'localhost.yml'), 'w') as f:
        f.write('---\n')
        f.write('ansible_connection: local\n')
        f.write(f'ansible_python_interpreter: {sys.executable}')

    return execute(workspace)


def main():
    preset = parse_preset()
    with tempfile.TemporaryDirectory(prefix='preset-') as workspace:
        process(workspace, preset)

if __name__ == '__main__':
    main()
