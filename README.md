**<h1> About project: </h1>**
**<h3> Admin bot is a bot, which manage catalog bots (create/on/off) </h3>**
**<h3> Catalog bot that provides list of categories and channels.
Category can be nested within themselves infinity times.
Channel can be related to category </h3>**

**<h3> Client can: </h3>**
- **<h4> Send ```/start``` and get list of channel on which user can join (some may be private) </h4>**
- **<h4> When user join some channel which is register in bot, then he receive welcome messages from this channel (messages managed by admin) </h4>**

**<h3> Admin can: </h3>**
- **<h4> Manage channels in bot: </h4>**
- - **<h4> Auto approve chat join request </h4>**
- - **<h4> Manage welcome messages </h4>**
- - **<h4> Change title </h4>**
- - **<h4> Change invite link </h4>**
- **<h4> Manage categories in bot: </h4>**
- - **<h4> Change title, description, media </h4>**
- - **<h4> Manage another categories and channels, related to this category </h4>**
- **<h4> Send default and periodic newsletter to clients </h4>**
- **<h4> Monitor client statistic </h4>**
- **<h4> Manage admins </h4>**
- **<h4> Manage bot menu (Text and Media) </h4>**

**<h2> You can use this bots in your Django project, just: </h2>**

- **<h3> copy ```catalog_bot``` app and ```admin_bot``` app </h3>**
- **<h3> copy docker files if you need it </h3>**
- **<h3> Specify path to migration module: </h3>**
```python
MIGRATION_MODULES = {
    'catalog_bot': 'catalog_bot.infrastructure.db.migrations',
    'admin_bot': 'admin_bot.db.migrations',
}
```
- **<h3> Do not forget to include bot apps in ```INSTALLED_APPS``` </h3>**
```python
INSTALLED_APPS = [
    'catalog_bot.apps.CatalogBotConfig',
    'admin_bot.apps.AdminBotConfig',
]
```

**<h1> Startup: </h1>**
- **<h4> Create .env file in the root dir, you can find example in .env.example </h4>**
- **<h4> ```docker compose up --build``` </h4>**
- **<h4> Create admin for ```admin_bot``` in the database. You can do this in Django admin panel </h4>**

**<h1> Stack of this project: </h1>**
- **<h3> Python 3.11.4 </h3>**
- **<h3> Aiogram3 + aiogram_dialog + webhook </h3>**
- **<h3> Django </h3>**
- **<h3> Redis </h3>**
- **<h3> Celery, Celery beat </h3>**
- **<h3> Nginx </h3>**
- **<h3> Docker </h3>**
