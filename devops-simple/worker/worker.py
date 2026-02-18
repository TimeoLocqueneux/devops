import time
import sys
import signal
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

stop = False

def handle_signal(sig, frame):
    global stop
    logger.info("Signal reçu, arrêt propre...")
    stop = True

signal.signal(signal.SIGTERM, handle_signal)
signal.signal(signal.SIGINT, handle_signal)

def run_task(n):
    logger.info(f"Tâche {n} démarrée")
    time.sleep(2)
    logger.info(f"Tâche {n} terminée")

logger.info("Worker démarré")
for i in range(1, 4):
    if stop:
        break
    run_task(i)

logger.info("Worker terminé proprement")
sys.exit(0)
