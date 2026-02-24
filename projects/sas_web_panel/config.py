import os
class Config:
    SECRET_KEY = os.urandom(24)
    DEBUG = False
    PORT = 5000
    HOST = '0.0.0.0'
    LOG_FILE = 'logs/app.log'
    SUITE_DIR = os.path.expanduser('~/senior-automation-suite')
    BIDS_FILE = os.path.join(SUITE_DIR, 'ai_strategy/bidding_templates.txt')
