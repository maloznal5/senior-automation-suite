import logging
import subprocess
import os
from flask import Flask, render_template, request
from config import Config

# ЛОГИРОВАНИЕ
if not os.path.exists('logs'): os.makedirs('logs')
logging.basicConfig(level=logging.INFO, filename=Config.LOG_FILE, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.config.from_object(Config)

def get_tree():
    try:
        return subprocess.check_output(["tree", Config.SUITE_DIR, "-L", "3"]).decode('utf-8')
    except:
        return subprocess.check_output(["ls", "-R", Config.SUITE_DIR]).decode('utf-8')

def get_bids():
    if os.path.exists(Config.BIDS_FILE):
        with open(Config.BIDS_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    return "Шаблоны не найдены. Создайте ai_strategy/bidding_templates.txt"

@app.route('/')
def index():
    logging.info(f"Панель открыта с IP: {request.remote_addr}")
    return render_template('index.html', tree=get_tree(), bids=get_bids())

@app.route('/open_folder')
def open_folder():
    logging.info("Запрошено открытие папки")
    # В Termux графические папки не открываются, эмулируем ответ
    return f"Рабочая директория: {Config.SUITE_DIR}. Проверьте логи."

if __name__ == '__main__':
    logging.info("Web Panel запущен")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
