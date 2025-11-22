# GesTurner

GesTurner は、Webカメラを使用してジェスチャー（現在は口の開閉）を検知し、楽譜などのページめくり（下矢印キーの送信）を行うアプリケーションです。

## 概要

- **機能**: Webカメラでユーザーの顔を認識し、特定のジェスチャー（口を開ける）を検知すると、キーボード入力（Page Down / 下矢印）をエミュレートします。
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

### 操作方法

1. アプリが起動すると、Webカメラの映像が表示されたデバッグウィンドウと、ステータスオーバーレイが表示されます。
2. カメラに向かって **口を開ける** 動作をします。
3. ステータスが "Mouth Open" になり、その状態を **約1秒間** 維持すると、システムに **下矢印キー (Down Arrow)** が送信されます。
4. アプリを終了するには、デバッグウィンドウを選択した状態で `Esc` キーを押します。

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
