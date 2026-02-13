import os
from pathlib import Path

# --- パス設定 ---
# プロジェクトのルートディレクトリ（manage.pyがある場所）を自動取得します。
BASE_DIR = Path(__file__).resolve().parent.parent

# --- セキュリティ設定 ---

# SECRET_KEY: Djangoの暗号化署名に使われる「鍵」です。
# 本来はGitHubに公開せず環境変数にすべきですが、まずは初期値を保持します。
# SECRET_KEY = 'django-insecure-fj94$4mhse6sity3@yexjjw&96(d@o$ry9)5+w=cuoow1o1w%i'

# 環境変数から取得し、なければ開発用のキー（今のキー）を使う
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-fj94$4mhse6sity3@yexjjw&96(d@o$ry9)5+w=cuoow1o1w%i')

# 環境変数がなければ 'True'（開発環境）、あればその値に従う
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

# ALLOWED_HOSTS: アクセスを許可するドメインを指定します。
# 127.0.0.1 や localhost は自分のPC用、3つ目は PythonAnywhere 用です。
# ※「あなたのユーザー名」は実際のユーザー名に書き換えてください。
ALLOWED_HOSTS = [
    '127.0.0.1', 
    'localhost', 
    'ivory369.pythonanywhere.com'
]

# --- アプリケーション定義 ---

INSTALLED_APPS = [
    'notes', # あなたが作成したアプリ
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'noteapp_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [], # プロジェクト共通のテンプレートフォルダがある場合はここに追加
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'noteapp_project.wsgi.application'


# --- データベース設定 ---
# PythonAnywhereでも最初は SQLite3 を使うのが最もスムーズです。
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --- 言語・時刻設定 ---

# 言語を日本語に、タイムゾーンを日本時間に設定しています。
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True
USE_TZ = True


# --- 静的ファイル (CSS, JavaScript, Images) の設定 ---

# ブラウザからアクセスする際のURLの接頭辞
STATIC_URL = 'static/'

# 【本番用】サーバー上で「python manage.py collectstatic」を実行した際、
# すべての静的ファイルが集約される場所です。
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# 【開発用】各アプリのフォルダ以外に、プロジェクト直下に static フォルダを置く場合の参照先。
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# --- メディアファイル (ユーザーがアップロードする画像など) の設定 ---

# ブラウザから画像にアクセスする際のURL
MEDIA_URL = '/media/'
# 実際に画像ファイルが保存されるサーバー上のパス
MEDIA_ROOT = BASE_DIR / 'media'

# デフォルトのプライマリキー（ID）の型
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'