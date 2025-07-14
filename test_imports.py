try:
    from modules.azure_openai_client import AzureOpenAIClient
    from modules.minutes_generator import MinutesGenerator
    from schemas.transcript import TranscriptInput
    from schemas.minutes import MinutesOutput
    from routers.minutes import router
    print('✅ All imports successful')
except Exception as e:
    print(f'❌ Import error: {e}')
