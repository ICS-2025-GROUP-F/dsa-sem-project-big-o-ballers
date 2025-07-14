import logging

class AppLogger:
    def __init__(self, log_file="app.log", gui_log_widget=None):
        self.gui_log_widget = gui_log_widget

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)s: %(message)s",
            handlers=[
                logging.FileHandler(log_file, encoding="utf-8"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("TaskManagerLogger")

    def log_event(self, message, level="info"):
        # Log to file/console
        if level == "info":
            self.logger.info(message)
        elif level == "warning":
            self.logger.warning(message)
        elif level == "error":
            self.logger.error(message)
        else:
            self.logger.debug(message)

        if self.gui_log_widget:
            self.gui_log_widget.insert("end", message + "\n")
            self.gui_log_widget.see("end")