#!/usr/bin/env python3

import sys
import os
sys.path.append('/home/ubuntu/repos/devin_okawa')

print("=== Complete Azure OpenAI Configuration Test ===")
print()

try:
    from src.config import settings
    print("✅ Config module imported successfully")
    
    print("\n=== Configuration Values ===")
    print(f"openai_api_key: {'SET' if settings.openai_api_key else 'NOT SET'}")
    print(f"openai_model: {settings.openai_model}")
    print(f"openai_max_tokens: {settings.openai_max_tokens}")
    print(f"openai_temperature: {settings.openai_temperature}")
    print(f"openai_timeout: {settings.openai_timeout}")
    print(f"azure_openai_endpoint: {settings.azure_openai_endpoint}")
    print(f"azure_openai_api_version: {settings.azure_openai_api_version}")
    
    print(f"\n=== Azure OpenAI Configuration Check ===")
    is_configured = settings.is_azure_openai_configured()
    print(f"Azure OpenAI properly configured: {is_configured}")
    
    print("\n=== Azure OpenAI Client Test ===")
    from src.modules.openai_client import OpenAIClient
    
    client = OpenAIClient()
    print(f"OpenAI client created: {client.client is not None}")
    
    if client.client:
        print("✅ Azure OpenAI client initialized successfully")
        print("Ready for API calls")
    else:
        print("❌ Azure OpenAI client is None - using fallback mode")
        print("This is expected when using placeholder values")
    
    print("\n=== Minutes Generator Test ===")
    from src.modules.minutes_generator import MinutesGenerator
    from src.schemas.transcript import TranscriptInput
    
    generator = MinutesGenerator()
    
    test_transcript = TranscriptInput(
        meeting_title="テスト会議",
        meeting_date="2025-01-14T10:00:00",
        participants=["田中", "佐藤"],
        transcript_text="短いテストトランスクリプト"
    )
    
    print("Testing minutes generation with small transcript...")
    try:
        result = generator.generate_minutes(test_transcript)
        print("✅ Minutes generation completed")
        print(f"Result type: {type(result)}")
        print(f"Meeting title: {result.meeting_title}")
    except Exception as e:
        print(f"❌ Minutes generation failed: {e}")
    
    print("\n=== Large Transcript Performance Test ===")
    large_transcript = TranscriptInput(
        meeting_title="大規模会議",
        meeting_date="2025-01-14T14:00:00", 
        participants=["田中", "佐藤", "鈴木"],
        transcript_text="これは非常に長いトランスクリプトです。" * 1000
    )
    
    print("Testing with large transcript (performance monitoring)...")
    try:
        result = generator.generate_minutes(large_transcript)
        print("✅ Large transcript processing completed")
        print("Check logs for performance timing information")
    except Exception as e:
        print(f"❌ Large transcript processing failed: {e}")
    
except Exception as e:
    print(f"❌ Error during test: {e}")
    import traceback
    traceback.print_exc()

print()
print("=== Test Complete ===")
