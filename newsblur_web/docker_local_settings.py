import logging
import os

# ===================
# = Server Settings =
# ===================

ADMINS = (("Samuel Clay", "samuel@newsblur.com"),)

SERVER_EMAIL = "server@newsblur.com"
HELLO_EMAIL = "hello@newsblur.com"
NEWSBLUR_URL = "https://localhost"
PUSH_DOMAIN = "localhost"
SESSION_COOKIE_DOMAIN = "localhost"

# ===================
# = Global Settings =
# ===================

DOCKERBUILD = True
DEBUG = True

# DEBUG_ASSETS controls JS/CSS asset packaging. Turning this off requires you to run
# `./manage.py collectstatic` first (done at image build time here).
DEBUG_ASSETS = False

# DEBUG_QUERIES controls the output of the database query logs.
DEBUG_QUERIES = DEBUG
DEBUG_QUERIES_SUMMARY_ONLY = False

MEDIA_URL = "/media/"
IMAGES_URL = "/imageproxy"
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "")
AUTO_PREMIUM_NEW_USERS = True
AUTO_PREMIUM_ARCHIVE_NEW_USERS = True
AUTO_PREMIUM_PRO_NEW_USERS = True
AUTO_PREMIUM = True
if not AUTO_PREMIUM:
    AUTO_PREMIUM_NEW_USERS = False
    AUTO_PREMIUM_ARCHIVE_NEW_USERS = False
    AUTO_PREMIUM_PRO_NEW_USERS = False
AUTO_ENABLE_NEW_USERS = True
ENFORCE_SIGNUP_CAPTCHA = False
ENABLE_PUSH = False

PRO_MINUTES_BETWEEN_FETCHES = 15

# NOTE: this CACHES dict is unconditionally overwritten later by
# newsblur_web/settings.py (~L1016), which builds the LOCATION from
# REDIS_USER/REDIS_USER_PORT + REDIS_PASSWORD -- kept here only so this file stays a
# faithful/complete settings module on its own.
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://newsblur-redis:6579/6",
    },
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

HOMEPAGE_USERNAME = "popular"
DEV_AUTOLOGIN_USERNAME = "samuel"

# Google Reader OAuth API Keys (unused; no external OAuth configured for this deploy)
OAUTH_KEY = "www.example.com"
OAUTH_SECRET = "SECRET_KEY_FROM_GOOGLE"

S3_ACCESS_KEY = "XXX"
S3_SECRET = "SECRET"
S3_BACKUP_BUCKET = "newsblur-backups"
S3_PAGES_BUCKET_NAME = "pages-XXX.newsblur.com"
S3_ICONS_BUCKET_NAME = "icons-XXX.newsblur.com"
S3_AVATARS_BUCKET_NAME = "avatars-XXX.newsblur.com"

STRIPE_SECRET = "YOUR-SECRET-API-KEY"
STRIPE_PUBLISHABLE = "YOUR-PUBLISHABLE-API-KEY"

# ===============
# = Social APIs =
# ===============

FACEBOOK_APP_ID = "111111111111111"
FACEBOOK_SECRET = "99999999999999999999999999999999"
TWITTER_CONSUMER_KEY = "ooooooooooooooooooooo"
TWITTER_CONSUMER_SECRET = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
YOUTUBE_API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# =============
# = Databases =
# =============

DATABASES = {
    "default": {
        "NAME": os.getenv("POSTGRES_DB", "newsblur"),
        "ENGINE": "django_prometheus.db.backends.postgresql",
        "USER": os.getenv("POSTGRES_USER", "newsblur"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", ""),
        "HOST": "newsblur-postgres",
        "PORT": 5432,
    },
}

# Mongo auth: settings.py's primary connection does
# `MONGODB = connect(MONGO_DB_NAME, **MONGO_DB)` with username/password/
# authentication_source as SEPARATE kwargs -- empirically confirmed (this deploy,
# mongoengine 0.21.0 + pymongo 3.13.0) that combination silently produces an
# UNAUTHENTICATED client (ping succeeds, any real op 'requires authentication',
# no auth attempt even hits the mongod logs). Embedding credentials in the host as
# a mongodb:// URI instead works -- this is the same pattern settings.py's own
# MONGO_ANALYTICS_DB branch already uses when "username" is present, so this just
# brings the primary connection in line with the code path that's proven to work.
MONGO_DB = {
    "name": "newsblur",
    "host": "mongodb://%s:%s@newsblur-mongo:29019/?authSource=admin"
    % (os.getenv("MONGO_USERNAME", "newsblur"), os.getenv("MONGO_PASSWORD", "")),
}
MONGO_ANALYTICS_DB = {
    "name": "nbanalytics",
    "host": "newsblur-mongo:29019",
    "username": os.getenv("MONGO_USERNAME", "newsblur"),
    "password": os.getenv("MONGO_PASSWORD", ""),
}

MONGODB_SLAVE = {"host": "newsblur-mongo"}

# Celery RabbitMQ/Redis Broker
# NOTE: CELERY_BROKER_URL here is unconditionally overwritten by settings.py (~L987)
# using REDIS_PASSWORD -- kept for completeness.
BROKER_URL = "redis://newsblur-redis:6579/0"
CELERY_RESULT_BACKEND = BROKER_URL
CELERY_WORKER_CONCURRENCY = 1

# host/port only reach settings.py's redis.ConnectionPool(...) calls -- REDIS_PASSWORD
# (settings.py, from the REDIS_PASSWORD env var) is what actually authenticates them.
REDIS_USER = {"host": "newsblur-redis", "port": 6579}
REDIS_PUBSUB = {"host": "newsblur-redis", "port": 6579}
REDIS_STORY = {"host": "newsblur-redis", "port": 6579}
REDIS_SESSIONS = {"host": "newsblur-redis", "port": 6579}

CELERY_REDIS_DB_NUM = 4
SESSION_REDIS_DB = 5

ELASTICSEARCH_FEED_HOSTS = ["newsblur-elasticsearch:9200"]
ELASTICSEARCH_STORY_HOSTS = ["newsblur-elasticsearch:9200"]
ELASTICSEARCH_DISCOVER_HOSTS = ["newsblur-elasticsearch:9200"]

ELASTICSEARCH_FEED_HOST = "http://newsblur-elasticsearch:9200"
ELASTICSEARCH_STORY_HOST = "http://newsblur-elasticsearch:9200"
ELASTICSEARCH_DISCOVER_HOST = "http://newsblur-elasticsearch:9200"
BACKED_BY_AWS = {
    "pages_on_node": False,
    "pages_on_s3": False,
    "icons_on_s3": False,
}

# AI Provider API Keys -- optional, not configured for this deploy.
OPENAI_API_KEY = "sk-svcacct-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
ANTHROPIC_API_KEY = "sk-ant-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
GOOGLE_GEMINI_API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
XAI_GROK_API_KEY = "xai-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
ASK_AI_MODEL = "anthropic"
BRIEFING_MODEL = "openai"
WEBFEED_MODEL = "openai"

# ===========
# = Logging =
# ===========

LOG_TO_STREAM = True

if len(logging._handlerList) < 1:
    LOG_FILE = "~/newsblur/logs/development.log"
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)-12s: %(message)s",
        datefmt="%b %d %H:%M:%S",
        handler=logging.StreamHandler,
    )

MAILGUN_ACCESS_KEY = "key-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
MAILGUN_SERVER_NAME = "newsblur.com"

DO_TOKEN_LOG = "0000000000000000000000000000000000000000000000000000000000000000"
DO_TOKEN_FABRIC = "0000000000000000000000000000000000000000000000000000000000000000"

SERVER_NAME = "nblocalhost"
NEWSBLUR_URL = os.getenv("NEWSBLUR_URL", "https://localhost")

if NEWSBLUR_URL == "https://localhost":
    SESSION_COOKIE_DOMAIN = "localhost"

SESSION_ENGINE = "redis_sessions.session"

RECAPTCHA_SECRET_KEY = "0000000000000000000000000000000000000000"
IMAGES_SECRET_KEY = "0000000000000000000000000000000"

# APNS settings for token-based authentication -- unused.
APNS_TEAM_ID = "XXXXXXXXXX"
APNS_KEY_ID = "XXXXXXXXXX"
