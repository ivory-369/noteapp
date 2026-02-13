from django.db import models

# =========================================
# Categoryモデル（大カテゴリ）
# =========================================
class Category(models.Model):
    # カテゴリ名（必須・ユニーク）
    # 重複を防ぎたいので unique=True
    # 短めの文字列（例：編み物、Python学習）
    name = models.CharField(max_length=80, unique=True)

    # 作成日時（自動）
    # データが作られたときに自動で設定される
    created_at = models.DateTimeField(auto_now_add=True)

    # 管理画面やシェルで表示するときに名前を返す
    def __str__(self):
        return self.name

# =========================================
# Noteモデル（ノート）
# =========================================
class Note(models.Model):
    # ノートのタイトル（必須）
    # 短めの文字列（例：編み物帽子の製図）
    title = models.CharField(max_length=100)

    # 手書き画像（必須）
    # 画像ファイルを保存するフィールド
    # 'notes/' は media フォルダ内の保存先サブフォルダ
    image = models.ImageField(upload_to='notes/', blank=True, null=True)


    # 作成日時（自動）
    # ノートが作られた日時を記録
    created_at = models.DateTimeField(auto_now_add=True)

    # 大カテゴリ（必須）
    # ForeignKeyでCategoryモデルを参照
    # Noteは1つのCategoryに属する
    # Categoryが削除されたら関連するNoteも削除される（CASCADE）
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    # 管理画面やシェルで表示するときにタイトルを返す
    def __str__(self):
        return self.title
