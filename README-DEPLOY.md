# 🚀 Telegram Mini App Deployment

## Быстрый деплой на VPS

### 1. Подготовка на сервере
```bash
# Клонируйте проект или скопируйте файлы на VPS
git clone your-repo.git
cd ResearchMiniapp

# Или скопируйте файлы:
# - index.html
# - Dockerfile 
# - docker-compose-miniapp.yml
# - deploy.sh
```

### 2. Запуск
```bash
# Простой запуск
./deploy.sh

# Или вручную:
docker-compose -f docker-compose-miniapp.yml up -d
```

### 3. Получение URL для Telegram Bot
```bash
# Посмотрите логи cloudflared для получения публичного URL
docker-compose -f docker-compose-miniapp.yml logs cloudflared-miniapp

# Найдите строку типа:
# https://random-url.trycloudflare.com
```

### 4. Настройка Telegram Bot
1. Откройте @BotFather в Telegram
2. Найдите ваш бот или создайте новый через `/newbot`
3. Используйте команду `/setmenubutton` 
4. Укажите URL из cloudflared логов
5. Или используйте `/mybots` → выберите бота → Bot Settings → Menu Button

### 5. Структура проекта
```
ResearchMiniapp/
├── index.html                    # Основное приложение
├── Dockerfile                    # Docker конфигурация
├── docker-compose-miniapp.yml    # Docker Compose для Mini App
├── deploy.sh                     # Скрипт деплоя
└── README-DEPLOY.md             # Эта инструкция
```

### 6. Управление
```bash
# Посмотреть статус
docker-compose -f docker-compose-miniapp.yml ps

# Посмотреть логи
docker-compose -f docker-compose-miniapp.yml logs -f

# Остановить
docker-compose -f docker-compose-miniapp.yml down

# Перезапустить после изменений
./deploy.sh
```

### 7. Порты
- **3000** - Mini App (локально)
- **80** - nginx внутри контейнера
- Cloudflare tunnel предоставляет публичный HTTPS URL

### 8. Важные моменты
- n8n должен быть уже запущен отдельно
- Webhook URL в index.html должен совпадать с n8n
- Mini App автоматически получает HTTPS через Cloudflare
- Логи cloudflared покажут публичный URL для Telegram Bot