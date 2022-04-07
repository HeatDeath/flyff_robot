ps aux|grep python| grep receive | awk '{print $2}'|xargs kill -9

git pull

sleep 3

nohup python3 receive_msg.py > server.log 2>&1 &