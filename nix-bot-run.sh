#! /usr/bin/env nix-shell
#! nix-shell -i bash -p bash python313Packages.wikipedia python313Packages.requests python313Packages.cython
#

# Directory of the virtual environment
#VENV="./FaustBotVEnv"
export PYTHONDONTWRITEBYTECODE=1

venv() {
  :
}

help() {
  echo "Simple script to manage a single faust-bot instance."
  echo "  -h  displays this help message"
  echo "  -s  starts the bot, if it is not running yet"
  echo "  -e  exits/stops the bot"
  echo "  -r  restarts the bot"
  echo "  -u  updates the bots code"
  echo "  -d  activates tailing of out.txt for quick debugging"
}

start() {
  venv
  echo "[=== checking if bot is already running "
  if [ -f ".pid" ]; then
    echo "[=== bot is already running "
    echo "[=== aborting start "
  else
    echo "[=== bot is not running "
    echo "[=== check if out.txt exists "
    if [ -f "out.txt" ]; then
      echo "[=== removing existing out.txt "
      rm out.txt
    else
      echo "[=== no out.txt found "
    fi
    echo "[=== checking if database already exists "
    if [ -f "faust_bot.db" ]; then
      echo "[=== database already exists "
    else
      echo "[=== no database "
      echo "[=== preparing database "
      python ReadInternationalization.py
    fi
    echo "[=== checking if config.txt exits"
    if [ -f "config.txt" ]; then
      echo "[=== config.txt exists"
    else
      echo "[=== no config.txt"
      echo "[== aborting start"
      exit
    fi
    echo "[=== checking if badquotes.txt exists"
    if [ -f "FaustBot/Modules/txtfiles/badquotes.txt" ]; then
      echo "[=== badquotes.txt exists, continuing"
    else
      touch "FaustBot/Modules/txtfiles/badquotes.txt"
      echo "[=== badquotes.txt created"
    fi
    echo "[=== starting faust-bot "
    echo "[=== redirecting output to nohup.out "
    nohup python -u Main.py --config config.txt >out.txt &
    echo "[=== pid of bot process can be found in .pid "
    echo $! >.pid
  fi
}

stop() {
  echo "[=== checking if bot is running "
  if [ ! -f ".pid" ]; then
    echo "[=== bot is not running "
  else
    echo "[=== bot is running "
    echo "[=== killing bot process "
    kill "$(cat .pid)"
    echo "[=== removing .pid file "
    rm .pid
  fi
}

update() {
  echo "[=== stopping the bot to update it "
  stop
  echo "[=== stashing local changes "
  git stash --all
  echo "[=== update the code "
  git pull origin main
  echo "[=== reapply done local changes "
  git stash pop
  echo "[=== restarting bot instance "
  start
}

clean() {
  echo "[=== cleaning files "
  echo "[=== stopping the bot "
  stop
  echo "[=== removing output file "
  rm out.txt
  echo "[=== removing venv "
  rm -rf $VENV
}

debug() {
  echo "[== debug sesh activated"
  stop
  start
  tail -f out.txt
}

OPTIND=1

while getopts "hserucd" opt; do
  case $opt in
  h)
    help
    exit
    ;;
  s)
    start
    ;;
  e)
    stop
    ;;
  r)
    stop
    start
    ;;
  u)
    update
    ;;
  c)
    clean
    ;;
  d)
    debug
    ;;
  \?)
    echo "Invalid option: -$OPTARG" >&2
    help
    ;;
  esac
done
