PROJECT_DIR=/home/pi/Documents

PYTHON_EXE=$PROJECT_DIR/auto_env/bin/python
LOG_DIR=$PROJECT_DIR/auto_logs
SERVER_DIR=$PROJECT_DIR/Auto-Robot/autorobot/server

cd $SERVER_DIR
$PYTHON_EXE server_camera.py --fps 30 &> $LOG_DIR/camera.log
$PYTHON_EXE server_commands.py &> $LOG_DIR/commands.log
