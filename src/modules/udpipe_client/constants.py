AWAITING_START_DURATION = 5

NEWPAR_MARKER = '# newpar'
SENT_ID_MARKER = '# sent_id = '
SENT_TEXT_MARKER = '# text = '
SUB_DELIMITER_MARKER = ''

SENT_ID_INDEX = 0
SENT_TEXT_INDEX = 1
NON_SENT_INFO_START_INDEX = 2
NON_EXTRA_COMMENT_START_INDEX = 5
REQUIRED_INFO_INDICES = [0, 1, 2, 3, 5, 6, 7]

UDP_PORT = 3000
UDP_MODEL_NAME = 'ukrainian-iu-ud-2.10-220711'

UDP_PROCESS_ENDPOINTS = {
  'local': f'http://localhost:{UDP_PORT}/process',
  'remote': 'http://lindat.mff.cuni.cz/services/udpipe/api/process'
}

UDP_EXEC_CODES = {
  'PROCESS_REQUEST_SUCCESS': 0,
  'RUNNING_SUCCESS': 0,
}

UDP_CLIENT_SHS_PATH = 'modules/udpipe_client/scripts'
START_UDP_SH_PATH = f'{UDP_CLIENT_SHS_PATH}/start_udp.sh'
STOP_UDP_SH_PATH = f'{UDP_CLIENT_SHS_PATH}/stop_udp.sh'
IS_UDP_RUNNING_SH_PATH = f'{UDP_CLIENT_SHS_PATH}/is_udp_running.sh'
