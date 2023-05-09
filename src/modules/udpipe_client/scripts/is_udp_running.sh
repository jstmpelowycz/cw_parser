is_udp_running() {
  if lsof -i :3000 | grep -q "python"; then
    exit 0
  else
    exit 1
  fi
}

is_udp_running