import os
import sys
import vertexai
from dotenv import load_dotenv

# デプロイ対象のエージェントアプリケーションをインポート
from ai_agent_idea_generator.agent import root_agent as app

def deploy_to_agent_engine():
    """Agent Engineにエージェントをデプロイする関数。"""
    
    print("--- Agent Engineへのデプロイを開始します ---")
    
    # .envファイルから環境変数を読み込む
    # ai_agent_idea_generatorディレクトリ内の.envを読み込むようにパスを指定
    dotenv_path = os.path.join(os.path.dirname(__file__), 'ai_agent_idea_generator', '.env')
    load_dotenv(dotenv_path=dotenv_path)
    
    # --- 1. Vertex AIの初期化 ---
    try:
        PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
        LOCATION = os.environ["GOOGLE_CLOUD_LOCATION"]
        STAGING_BUCKET = os.environ["STAGING_BUCKET"]
        
        print(f"プロジェクトID: {PROJECT_ID}")
        print(f"ロケーション: {LOCATION}")
        print(f"ステージングバケット: {STAGING_BUCKET}")
        
        vertexai.init(
            project=PROJECT_ID,
            location=LOCATION,
            staging_bucket=STAGING_BUCKET,
        )
    except KeyError as e:
        print(f"エラー: 環境変数 {e} が.envファイルに設定されていません。")
        print("デプロイを中止します。")
        sys.exit(1)
        
    # --- 2. デプロイの実行 ---
    try:
        from vertexai import agent_engines
        
        print("\nエージェントのデプロイを開始します。これには数分かかる場合があります...")
        
        remote_app = agent_engines.create(
            display_name="AI Agentアイディアジェネレーター",
            description="添付された企業情報のファイルからどのようなAI Agentを企業内で作成すると良いか提案するアドバイザーです",
            agent_engine=app,
            requirements=[
                # agent.pyが必要とするライブラリをここに記述
                "google-cloud-aiplatform[adk,agent_engines]",
                "cloudpickle",
                "python-dotenv"
            ],
        )
        
        print("\n🎉 デプロイが正常に完了しました！ 🎉")
        print("\nデプロイされたエージェントのリソース名は以下の通りです:")
        print(remote_app.resource_name)
        
    except Exception as e:
        print(f"\nデプロイ中にエラーが発生しました: {e}")
        print("デプロイに失敗しました。")

if __name__ == "__main__":
    deploy_to_agent_engine()
