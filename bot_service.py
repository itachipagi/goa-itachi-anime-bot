import os
import sys
import time
import subprocess
import logging
import servicemanager
import win32event
import win32service
import win32serviceutil

# Set up logging
logging.basicConfig(
    filename='bot_service.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BotService(win32serviceutil.ServiceFramework):
    _svc_name_ = "TelegramBotService"
    _svc_display_name_ = "Telegram Bot Service"
    _svc_description_ = "Runs the Telegram bot in the background 24/7"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.bot_process = None
        self.is_running = False

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_running = False
        
        # Kill the bot process if it's running
        if self.bot_process:
            logger.info("Stopping bot process...")
            try:
                self.bot_process.terminate()
                self.bot_process = None
            except Exception as e:
                logger.error(f"Error terminating bot process: {e}")

    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        self.is_running = True
        self.main()

    def main(self):
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        bot_script = os.path.join(script_dir, 'bot.py')
        
        logger.info(f"Starting bot from: {bot_script}")
        
        # Keep restarting the bot if it crashes
        while self.is_running:
            try:
                # Start the bot process
                python_exec = sys.executable
                self.bot_process = subprocess.Popen(
                    [python_exec, bot_script],
                    cwd=script_dir,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                
                logger.info(f"Bot process started with PID: {self.bot_process.pid}")
                
                # Check if the service is being stopped
                while self.is_running:
                    rc = win32event.WaitForSingleObject(self.hWaitStop, 5000)
                    if rc == win32event.WAIT_OBJECT_0:
                        # Service is being stopped
                        self.is_running = False
                        break
                    
                    # Check if the bot process is still running
                    if self.bot_process.poll() is not None:
                        logger.warning("Bot process has stopped unexpectedly, restarting...")
                        break
                
                # Clean up the process if it's still running
                if self.bot_process and self.bot_process.poll() is None:
                    self.bot_process.terminate()
                    self.bot_process = None
                    
                # If we're stopping the service, exit the loop
                if not self.is_running:
                    logger.info("Service is stopping, exiting main loop")
                    break
                    
                # Wait before restarting
                time.sleep(10)
                logger.info("Restarting bot...")
                
            except Exception as e:
                logger.error(f"Error in main service loop: {e}")
                time.sleep(60)  # Wait a bit longer if there's an error


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(BotService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(BotService) 
