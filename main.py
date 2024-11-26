import os
import flet as ft

# ファイル名を一括変更する関数
def rename_files(directory, page, rename_option):
    for root, dirs, files in os.walk(directory):
        folder_name = os.path.basename(root)
        file_count = {}  # 拡張子ごとのファイル数をカウントする辞書
        for filename in files:
            file_extension = os.path.splitext(filename)[1]
            if file_extension.lower() in [".mp4", ".html"]:
                file_path = os.path.join(root, filename)
                
                # 変換方法に応じた新しい名前を生成
                if rename_option == "folder_name":
                    # ディレクトリ名と同じファイル名に変更
                    if file_extension not in file_count:
                        file_count[file_extension] = 0
                    file_count[file_extension] += 1
                    new_name = f"{folder_name}_{file_count[file_extension]}{file_extension}"
                elif rename_option == "content":
                    # ファイル名を content.拡張子 に変更
                    new_name = f"content{file_extension}"

                new_path = os.path.join(root, new_name)

                try:
                    os.rename(file_path, new_path)
                    page.add(ft.Text(f"Renamed {filename} to {new_name}"))
                except Exception as e:
                    page.add(ft.Text(f"Error renaming {filename}: {e}", color="red"))

# Fletアプリのメイン関数
def main(page: ft.Page):
    page.title = "ファイル名一括変更ツール"
    page.window_width = 1200
    page.window_height = 1000
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # 横方向の中央揃え
    page.vertical_alignment = ft.MainAxisAlignment.CENTER      # 縦方向の中央揃え
    page.update()

    selected_folder = ft.Text(value="フォルダが選択されていません", size=16, text_align="center")
    select_button = ft.ElevatedButton(text="フォルダを選択")
    execute_button = ft.ElevatedButton(text="実行", disabled=True)

    # 変換方法を選択するドロップダウンメニュー
    rename_options = ft.Dropdown(
        options=[
            ft.dropdown.Option("folder_name", "ディレクトリ名と同じファイル名にする"),
            ft.dropdown.Option("content", "content.拡張子 にする"),
        ],
        value="folder_name",
    )

    # フォルダ選択ピッカーを初期化
    file_picker = ft.FilePicker(on_result=lambda e: folder_selected(e.path if e.path else None))
    page.overlay.append(file_picker)

    # フォルダを選択する関数
    def folder_selected(folder):
        if folder:
            selected_folder.value = f"選択されたフォルダ: {folder}"
            execute_button.disabled = False
            execute_button.update()
            selected_folder.update()
            page.folder_path = folder

    # ファイル名を変更する関数
    def execute_rename(e):
        if page.folder_path:
            rename_option = rename_options.value  # 選択された変換方法
            rename_files(page.folder_path, page, rename_option)
            page.add(ft.Text("完了しました！", color="green"))
        else:
            page.add(ft.Text("エラー: フォルダが選択されていません", color="red"))

    # ボタンイベントの設定
    select_button.on_click = lambda _: file_picker.get_directory_path()
    execute_button.on_click = execute_rename

    # コンテンツを中央配置
    page.add(
        ft.Column(
            [
                ft.Text("ファイル名を一括変更", size=20, weight="bold", text_align="center"),
                rename_options,
                selected_folder,
                select_button,
                execute_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(target=main)