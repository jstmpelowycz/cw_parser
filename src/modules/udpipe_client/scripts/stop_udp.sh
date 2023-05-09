stop_udp() {
  cd /Users/dmytro-pelovych/University/SE3/cw/udpipe || exit

  PID=$(lsof -ti :3000)

  echo "$PID"

  if [[ -n "$PID" ]]; then
    echo "Killing PID: $PID"
    kill "$PID"
  else
    echo "Error: Process not found"
  fi

  cd - || exit
}

stop_udp
