"""
Django settings for adminset project.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType, PosixGroupType
import configparser as cp  # 直接使用Python 3的configparser模块



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = cp.ConfigParser()
config.read(os.path.join(BASE_DIR, 'adminset.conf'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = 'n@s)3&f$tu#-^^%k-dj__th2)7m!m*(ag!fs=6ezyzb7l%@i@9'
# if redis_password:
#     CELERY_BROKER_URL = 'redis://:{0}@{1}:{2}/{3}'.format(redis_password, redis_host, redis_port, redis_db)
# else:
#     CELERY_BROKER_URL = 'redis://{0}:{1}/{2}'.format(redis_host, redis_port, redis_db)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TASK_SERIALIZER = 'json'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_SAMESITE = 'Lax'  # 添加SameSite cookie设置
CSRF_COOKIE_SAMESITE = 'Lax'  # 添加SameSite cookie设置
X_FRAME_OPTIONS = 'SAMEORIGIN'  # 添加X-Frame-Options设置

# Application definition

INSTALLED_APPS = [
    'setup',
    'navi',
    'cmdb',
    'config',
    'accounts',
    'monitor',
    'appconf',
    'delivery',
    'django_celery_results',
    'django_celery_beat',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'branches',
]

MIDDLEWARE = [  # 更新中间件设置
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ... existing code ...

# CSRF设置
CSRF_TRUSTED_ORIGINS = [
    'https://192.168.110.100',
    'http://192.168.110.100',
]
# CSRF失败时的友好提示（可选）
CSRF_FAILURE_VIEW = 'django.views.csrf.csrf_failure' 
# ... existing code ...

ROOT_URLCONF = 'adminset.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'adminset.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


DATABASES = {}
if config.get('db', 'engine') == 'mysql':
    DB_HOST = config.get('db', 'host')
    DB_PORT = config.getint('db', 'port')
    DB_USER = config.get('db', 'user')
    DB_PASSWORD = config.get('db', 'password')
    DB_DATABASE = config.get('db', 'database')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': DB_DATABASE,
            'USER': DB_USER,
            'PASSWORD': DB_PASSWORD,
            'HOST': DB_HOST,
            'PORT': DB_PORT,
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES', innodb_strict_mode=1",
            },
        }
    }
elif config.get('db', 'engine') == 'sqlite':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': config.get('db', 'database'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# 设置默认的主键字段类型
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
# sys.path.append(os.path.join(BASE_DIR, 'vendor').replace('\\', '/'))
#STATIC_ROOT = os.path.join(APP_PATH,'static').replace('\\','/')
STATIC_URL = '/static/'
STATIC_ROOT = '/var/opt/adminset/main/static/'
# 移除STATICFILES_DIRS以避免冲突
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}

#ldap configurations
ldap_enable = config.get('ldap', 'ldap_enable')
if ldap_enable == "True":
    ldap_port = config.get('ldap', 'ldap_port')
    if ldap_port:
        ldap_server = config.get('ldap', 'ldap_server') + ":" + ldap_port
    else:
        ldap_server = config.get('ldap', 'ldap_server')
    base_dn = config.get('ldap', 'base_dn')
    ldap_manager = config.get('ldap', 'ldap_manager')
    ldap_password = config.get('ldap', 'ldap_password')
    ldap_filter = config.get('ldap', 'ldap_filter')
    if ldap_filter == "OpenLDAP":
        ldap_filter = '(uid=%(user)s)'
    else:
        ldap_filter = '(sAMAccountName=%(user)s)'

    AUTH_LDAP_SERVER_URI = ldap_server

    AUTH_LDAP_BIND_DN = ldap_manager
    AUTH_LDAP_BIND_PASSWORD = ldap_password
    AUTH_LDAP_USER_SEARCH = LDAPSearch(
        base_dn,
        ldap.SCOPE_SUBTREE,
        ldap_filter,
    )
    # Or:
    # AUTH_LDAP_USER_DN_TEMPLATE = 'uid=%(user)s,ou=users,dc=example,dc=com'

    # Set up the basic group parameters.
    AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
        base_dn,
        ldap.SCOPE_SUBTREE,
        #'(objectClass=posixGroup)',
        '(objectClass=*)',
    )
    AUTH_LDAP_GROUP_TYPE = PosixGroupType(name_attr='cn')
    #
    # # Simple group restrictions
    require_group = config.get('ldap', 'require_group')
    nickname = config.get('ldap', 'nickname')
    is_active = config.get('ldap', 'is_active')
    is_superuser = config.get('ldap', 'is_superuser')
    if require_group:
        #AUTH_LDAP_REQUIRE_GROUP = 'cn=enable,ou=scimall,dc=gldap,dc=com'
        AUTH_LDAP_REQUIRE_GROUP = require_group
    # AUTH_LDAP_DENY_GROUP = 'cn=disabled,ou=django,ou=groups,dc=example,dc=com'

    # Populate the Django user from the LDAP directory.
    if not nickname:
        nickname = 'cn'
    AUTH_LDAP_USER_ATTR_MAP = {
        # 'first_name': 'givenName',
        # 'last_name': 'sn',
        'nickname': nickname,
        'email': 'mail',
        'ldap_name': 'cn',
    }

    if is_active and not is_superuser:
        AUTH_LDAP_USER_FLAGS_BY_GROUP = {
            'is_active': is_active,
        }
    elif is_superuser and not is_active:
        AUTH_LDAP_USER_FLAGS_BY_GROUP = {
            'is_superuser': is_superuser,
        }
    elif is_active and is_superuser:
        AUTH_LDAP_USER_FLAGS_BY_GROUP = {
            'is_active': is_active,
            'is_superuser': is_superuser,
        }

    # This is the default, but I like to be explicit.
    AUTH_LDAP_ALWAYS_UPDATE_USER = True

    # Use LDAP group membership to calculate group permissions.
    # AUTH_LDAP_FIND_GROUP_PERMS = True

    # Cache distinguised names and group memberships for an hour to minimize
    # LDAP traffic.

    AUTH_LDAP_CACHE_TIMEOUT = 60
    # Keep ModelBackend around for per-user permissions and maybe a local
    # superuser.
    AUTHENTICATION_BACKENDS = (
        'django_auth_ldap.backend.LDAPBackend',
        'django.contrib.auth.backends.ModelBackend',
    )

AUTH_USER_MODEL = 'accounts.UserInfo'
# MEDIA_ROOT = os.path.join(BASE_DIR,'mfile/media')
MEDIA_ROOT = os.path.join('/var/opt/adminset/data')
MEDIA_URL = '/media/'

# 使用标准文件系统存储
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# SFTP存储配置部分已删除