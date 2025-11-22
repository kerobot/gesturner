# GesTurner

GesTurner は、Webカメラを使用してジェスチャー（口の開閉や視線）を検知し、楽譜などのページめくり（上下矢印キーの送信）を行うアプリケーションです。

## 概要

- **機能**: Webカメラでユーザーの顔を認識し、特定のジェスチャーを検知すると、キーボード入力をエミュレートします。
  - **口を開ける**: 下矢印キー (Down Arrow) を送信（ページ送り）
  - **上を見る**: 上矢印キー (Up Arrow) を送信（ページ戻し）
- **用途**: 演奏中など、手が離せない状況での電子楽譜のページめくり。
- **技術スタック**: Python, OpenCV, MediaPipe, PyAutoGUI

## 前提条件

- Windows (推奨)
- Python 3.12 以上
- [Poetry](https://python-poetry.org/) (パッケージ管理ツール)
- Webカメラ

## 環境構築

1. **リポジトリのクローン**

   ```bash
   git clone <repository-url>
   cd gesturner
   ```

2. **依存関係のインストール**
   Poetry を使用して依存パッケージをインストールします。

   ```bash
   poetry install
   ```

## 実行方法

以下のコマンドでアプリケーションを起動します。

```bash
poetry run gesturner
```

または

```bash
poetry run python -m gesturner.main
```

### オプション

- `--debug`: デバッグウィンドウを表示します。カメラ映像と検知状況を確認できます。

```bash
poetry run python -m gesturner.main --debug
```

### 操作方法

1. アプリが起動すると、ステータスオーバーレイが表示されます（`--debug` オプション指定時はデバッグウィンドウも表示）。
2. **ページ送り（下へ）**: カメラに向かって **口を開ける** 動作をし、その状態を **約1秒間** 維持します。
3. **ページ戻し（上へ）**: カメラに向かって **視線を上に** 向け、その状態を **約1秒間** 維持します。
4. アプリを終了するには、デバッグウィンドウを選択した状態で `Esc` キーを押すか、ターミナルで `Ctrl+C` を押します。

## VS Code でのデバッグ実行

VS Code でデバッグを行うための設定手順です。

1. **拡張機能の確認**
   VS Code に "Python" 拡張機能がインストールされていることを確認してください。

2. **launch.json の設定**
   `.vscode/launch.json` ファイルを作成（または編集）し、以下の構成を追加します。

   ```json
   {
       "version": "0.2.0",
       "configurations": [
           {
               "name": "Python: GesTurner",
               "type": "debugpy",
               "request": "launch",
               "module": "gesturner.main",
               "console": "integratedTerminal",
               "justMyCode": true
           }
       ]
   }
   ```

3. **デバッグの開始**
   - VS Code の左サイドバーから「実行とデバッグ」アイコンをクリックします。
   - 上部のドロップダウンから "Python: GesTurner" を選択します。
   - 緑色の再生ボタン（デバッグの開始）をクリックするか、`F5` キーを押します。
   - ブレークポイントを設定してステップ実行などが可能です。

## 開発者向け情報

- **エントリポイント**: `gesturner/main.py`
- **検知ロジック**: `gesturner/gesture_detector.py` (現在は `MouthDetector` を使用)
- **設定**: `pyproject.toml`
