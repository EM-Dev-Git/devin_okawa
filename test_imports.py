try:
    from src.modules.azure_openai_client import AzureOpenAIClient
    from src.modules.minutes_generator import MinutesGenerator
    from src.schemas.transcript import TranscriptInput
    from src.schemas.minutes import MinutesOutput
    from src.routers.minutes import router
    print('✅ All imports successful')
except Exception as e:
    print(f'❌ Import error: {e}')
