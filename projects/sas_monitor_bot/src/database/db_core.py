import aiosqlite
import os
import csv
from utils.logger import setup_logger

logger = setup_logger()
DB_PATH = "database/analytics.db"

async def init_db():
    os.makedirs("database", exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS user_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.commit()
    logger.info("Database initialized.")

async def log_action(user_id: int, action: str):
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute('INSERT INTO user_actions (user_id, action) VALUES (?, ?)', (user_id, action))
            await db.commit()
    except Exception as e:
        logger.error(f"DB Log Error: {e}")

async def export_csv(filepath: str = "database/report.csv"):
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.execute('SELECT * FROM user_actions ORDER BY timestamp DESC') as cursor:
                rows = await cursor.fetchall()
                with open(filepath, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Log_ID", "User_ID", "Action", "Timestamp"])
                    writer.writerows(rows)
        return filepath
    except Exception as e:
        logger.error(f"CSV Export Error: {e}")
        return None
