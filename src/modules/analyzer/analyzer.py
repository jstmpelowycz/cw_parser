import src.modules.file_manager.file_manager as fm
import src.modules.udpipe_client.udpipe_client as uc
from src.modules.file_manager.file_manager import IdentifiablePath
from src.constants.paths import TXT_DATA_DIR_PATH, ANALYSIS_DATA_DIR_PATH


def analyze_all_with_udp_running() -> None:
  paths = fm.get_parsed_paths(TXT_DATA_DIR_PATH, '*.txt')

  uc.start()
  analyze_all(paths)
  uc.stop()


def analyze_all(paths: list[IdentifiablePath]) -> None:
  [analyze(path.path) for path in paths]


def analyze(in_file_path: str) -> None:
  out_file_path = get_dst_file_path(in_file_path)

  uc.process(in_file_path, out_file_path, locally=True)


def get_dst_file_path(src_file_path: str) -> str:
  file_id = fm.get_file_id(src_file_path)

  return f'{ANALYSIS_DATA_DIR_PATH}/{file_id}.json'
