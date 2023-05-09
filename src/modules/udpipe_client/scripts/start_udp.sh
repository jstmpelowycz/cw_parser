start_udp() {
  cd /Users/dmytro-pelovych/University/SE3/cw/udpipe || return

  ~/miniconda/envs/tensorflow/bin/python \
    src/udpipe2_server.py \
    3000 \
    ukr \
    ukrainian-iu-ud-2.10-220711:uk_iu-ud-2.10-220711:uk:ukr \
    udpipe2-ud-2.10-220711/uk_iu-ud-2.10-220711.model uk_iu \
    https://ufal.mff.cuni.cz/udpipe/2/models\#universal_dependencies_210_models

  cd /Users/dmytro-pelovych/University/SE3/cw/project || return
}

start_udp
