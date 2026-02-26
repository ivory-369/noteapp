# notes/urls.py
from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    # ----------------------------------------
    # トップ画面用
    # / にアクセスしたら、ノートがあれば一覧、なければ新規作成にリダイレクト
    # ----------------------------------------
    path("", views.top_redirect, name="top"),

    # ----------------------------------------
    # ノート一覧画面
    # /list/ にアクセスすると、すべてのノートを表示
    # ----------------------------------------
    path("list/", views.note_list, name="list"),

    # ----------------------------------------
    # ノート新規作成画面
    # /create/ にアクセスすると、新しいノートを作成
    # ----------------------------------------
    path("create/", views.note_create, name="create"),

    # ----------------------------------------
    # ノート編集画面
    # /edit/<note_id>/ で特定のノートを編集
    # ----------------------------------------
    path("edit/<int:note_id>/", views.note_edit, name="edit"),

    # ----------------------------------------
    # ノート削除
    # /delete/<note_id>/ で特定のノートを削除
    # ----------------------------------------
    path("delete/<int:note_id>/", views.note_delete, name="delete"),                        # 一覧
    
    # ----------------------------------------
    # お気に入り切替
    # /favorite/<note_id>/ で該当ノートの is_favorite を切り替える
    # Ajax から呼び出す想定
    # ----------------------------------------
    path("favorite/<int:note_id>/", views.toggle_favorite, name="toggle_favorite"),
]