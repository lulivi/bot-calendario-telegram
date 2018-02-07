#!/usr/bin/env bash

function clean_exit {
    echo "Killing processes... :("
    kill -9 -$$
}

current_dir=${PWD##*/}

if [[ $current_dir = "scripts" ]]; then
    cd ../ || exit;
fi

cd bot_calendario_telegram || exit;

# Run Rest Api
python reminder_rest_api.py &

# Check the status of the rest api process
rest_pid=$!
status=$?
if [ $status != 0 ]; then
  echo "Failed to start the rest api: $status"
  exit $status
else
  echo "Rest Api started correctly with pid: "$rest_pid
fi


# Run the bot
python bot.py &

# Check the status of the rest api process
bot_pid=$!
status=$?
if [ $status != 0 ]; then
  echo "Failed to start the bot: $status"
  exit $status
else
  echo "Bot started correctly with pid: "$bot_pid
fi


# Wait a sec and idle
sleep 2
trap '{ clean_exit; }' INT
read -p "To exit press enter or Ctrl-c..." answer
case ${answer:0:1} in
    * ) clean_exit;;
esac
