#!/bin/bash
# Добавление технического кейса в портфолио

cd ~/senior-automation-suite
mkdir -p docs/cases

# Создание файла кейса
cat << 'EOT' > docs/cases/ai_b2b_manager.md
# Case Study: AI-Powered B2B Order Manager

## 🎯 Project Overview
Automation of order processing for a large hardware store (krepezh.ua). The goal was to eliminate manual matching of client requests with a 10,000+ item catalog.

## 🛠 Technical Solution
- **AI Core**: Integration of LLM (OpenAI/Gemini) for natural language processing of messy customer orders.
- **Matching Engine**: Developed a custom RAG (Retrieval-Augmented Generation) system to match client "slang" names with official catalog nomenclature.
- **Infrastructure**: High-performance AsyncIO backend capable of handling concurrent requests.

## 📈 Business Results
- **Efficiency**: Reduced order processing time from 15 minutes to 30 seconds.
- **Accuracy**: 95%+ matching accuracy for non-standard item descriptions.
- **Scalability**: The system handles 24/7 load without human intervention.

---
*Status: Production-ready | Architecture: Modular AI Agent*
EOT

# Обновляем README, чтобы добавить ссылку на кейс
sed -i '/## 🏗 System Architecture/i ## 📂 Featured Case Studies\n- [AI B2B Order Manager](docs/cases/ai_b2b_manager.md)\n' README.md

# Синхронизация
git add .
git commit -m "feat: add AI B2B Manager case study"
git push origin main

echo "[-] Кейс добавлен и опубликован."
