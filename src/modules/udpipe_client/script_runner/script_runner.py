import subprocess

import src.modules.file_manager.file_manager as fm


def run_script(script_path: str) -> int:
  result = subprocess.run(['/bin/zsh', f'{script_path}'])
  return result.returncode


def run_script_separately(script_path: str) -> None:
  absolute_sp = fm.as_absolute_path(script_path)
  subprocess.run([
    'osascript',
    '-e',
    'tell application "Terminal" to do script '
    f'"/bin/zsh {absolute_sp}"'
  ])
