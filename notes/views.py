from django.shortcuts import render, redirect, get_object_or_404
from .models import Note, Category
from django.core.files.base import ContentFile
import base64
from django.http import JsonResponse

# -----------------------------
# 共通：カテゴリ取得
# -----------------------------
def get_categories_with_default():
    """
    カテゴリが0件なら「未分類」を自動生成する
    """
    if Category.objects.count() == 0:
        Category.objects.create(name="未分類")

    return Category.objects.all()


# -----------------------------
# 新規作成
# -----------------------------
def note_create(request):
    categories = get_categories_with_default()

    # ★ 追加：ノートが1件以上あるか判定
    notes_exist = Note.objects.exists()

    context = {
        "note": None,                 # 新規作成なので None
        "title": "",
        "categories": categories,
        "selected_category": None,
        "error": "",
        "notes_exist": notes_exist,   # ★ ここ追加
    }

    if request.method == "POST":
        title = request.POST.get("title", "")
        category_id = request.POST.get("category")
        image_data = request.POST.get("image_data")

        # カテゴリ決定（未選択なら最初のカテゴリ）
        if category_id:
            category = Category.objects.filter(id=category_id).first()
        else:
            category = categories.first()

        # 画像必須チェック
        if not image_data:
            context["error"] = "画像が送信されていません"
            context["title"] = title
            context["selected_category"] = category_id
            return render(request, "notes/note_form.html", context)

        # base64 → 画像ファイル化
        format, imgstr = image_data.split(";base64,")
        ext = format.split("/")[-1]
        data = base64.b64decode(imgstr)
        image_file = ContentFile(data, name=f"note.{ext}")

        # 保存
        Note.objects.create(
            title=title or "無題",
            image=image_file,
            category=category
        )

        return redirect("notes:list")

    return render(request, "notes/note_form.html", context)

# -----------------------------
# 編集
# -----------------------------
def note_edit(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    categories = get_categories_with_default()

    # ノートが1件以上あるか判定
    notes_exist = Note.objects.exists()

    context = {
        "note": note,
        "title": note.title,
        "categories": categories,
        "selected_category": note.category.id if note.category else None,
        "notes_exist": notes_exist,   # ★ これだけ追加
    }

    if request.method == "POST":
        title = request.POST.get("title", "")
        category_id = request.POST.get("category")
        delete_flag = request.POST.get("delete_image")
        image_data = request.POST.get("image_data")

        # カテゴリ更新
        if category_id:
            note.category = Category.objects.filter(id=category_id).first()

        note.title = title or "無題"

        # 画像削除 → 新規描画
        if delete_flag == "on":
            note.image.delete(save=False)
            note.image = None

        # 新しい画像があれば保存
        if image_data:
            format, imgstr = image_data.split(";base64,")
            ext = format.split("/")[-1]
            data = base64.b64decode(imgstr)
            note.image.save(f"note.{ext}", ContentFile(data))

        note.save()
        return redirect("notes:list")

    return render(request, "notes/note_form.html", context)

# -----------------------------
# 削除
# -----------------------------
def note_delete(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    note.delete()
    return redirect('notes:list')  # 削除後は一覧へ

# -----------------------------
# 一覧
# -----------------------------
def note_list(request):
    # GETパラメータでカテゴリID取得
    category_id = request.GET.get("category")     # カテゴリ
    favorite_only = request.GET.get("favorite")   # ★フィルター

    # ベースクエリ
    notes = Note.objects.all()

    # カテゴリフィルター
    if category_id:
        notes = notes.filter(category_id=category_id)
        
    # お気に入りフィルター
    if favorite_only == "1":
        notes = notes.filter(is_favorite=True)

    # 並び順
    notes = notes.order_by("-created_at")

    # プルダウン用カテゴリ
    categories = Category.objects.all()

    context = {
        "notes": notes,
        "categories": categories,
        "selected_category": category_id,  # 選択状態保持
        "favorite_only": favorite_only,    # ★状態保持
    }

    return render(request, "notes/note_list.html", context)
# -----------------------------
# トップのルーティング
# ノートがあれば一覧、なければ新規作成画面へ
# -----------------------------
def top_redirect(request):
    # ノートが1件でもあるか確認
    if Note.objects.exists():
        # ノート一覧へ
        return redirect('notes:list')
    else:
        # 新規作成画面へ
        return redirect('notes:create')

# ========================================
# お気に入り切替ビュー
# ========================================
def toggle_favorite(request, note_id):
    """
    ノートのお気に入り状態を切り替える
    Ajaxリクエストで呼び出されることを想定
    戻り値は JSON で現在の状態を返す
    """
    # --- note_id で対象ノートを取得 ---
    # 存在しない場合は 404 を返す
    note = get_object_or_404(Note, id=note_id)

    # --- 現在の is_favorite を反転 ---
    # True → False / False → True
    note.is_favorite = not note.is_favorite

    # --- DB に保存 ---
    note.save()

    # --- Ajax 用に JSON レスポンスで状態を返す ---
    return JsonResponse({"is_favorite": note.is_favorite})