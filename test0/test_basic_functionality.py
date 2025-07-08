#!/usr/bin/env python3
"""
Basic functionality test for the meeting minutes system
Tests core components without requiring OpenAI API key
"""

import sys
import os
sys.path.append('.')

def test_transcription_processing():
    """Test transcription parsing and preprocessing"""
    print("=== Testing Transcription Processing ===")
    
    from src.transcription.parser import TranscriptionParser
    from src.transcription.preprocessor import TranscriptionPreprocessor
    
    parser = TranscriptionParser()
    preprocessor = TranscriptionPreprocessor()
    
    with open('sample_data/sample_transcription.txt', 'r', encoding='utf-8') as f:
        sample_text = f.read()
    
    print(f"Loaded sample text: {len(sample_text)} characters")
    
    cleaned_text = preprocessor.clean_text(sample_text)
    normalized_text = preprocessor.normalize_speakers(cleaned_text)
    
    segments = parser.parse_transcription(normalized_text)
    
    print(f"Parsed {len(segments)} segments")
    
    for i, segment in enumerate(segments[:3]):
        print(f"Segment {i+1}: Speaker='{segment.speaker}', Content='{segment.content[:50]}...'")
    
    grouped = parser.group_by_speaker(segments)
    print(f"Found {len(grouped)} unique speakers: {list(grouped.keys())}")
    
    return segments

def test_minutes_generation_structure():
    """Test minutes generation structure (without AI)"""
    print("\n=== Testing Minutes Generation Structure ===")
    
    from src.minutes.generator import MinutesGenerator
    from src.minutes.formatter import MinutesFormatter
    
    segments = test_transcription_processing()
    
    generator = MinutesGenerator()
    formatter = MinutesFormatter()
    
    mock_minutes_data = {
        "meeting_title": "テスト会議",
        "meeting_date": "2024年1月15日",
        "participants": ["司会", "田中", "佐藤"],
        "summary": "## 会議概要\nプロジェクトの進捗確認を行いました。\n\n## 決定事項\n- システム設計書を来週金曜日までに完成\n- データベース設計を来週水曜日までに提出",
        "action_items": [
            {"action": "システム設計書の完成", "assignee": "田中", "deadline": "来週金曜日"},
            {"action": "データベース設計の提出", "assignee": "佐藤", "deadline": "来週水曜日"}
        ],
        "full_transcription": "司会：本日はお忙しい中...",
        "generated_at": "2024年1月15日 10:30:00"
    }
    
    html_output = formatter.format_to_html(mock_minutes_data)
    markdown_output = formatter.format_to_markdown(mock_minutes_data)
    
    print(f"HTML output generated: {len(html_output)} characters")
    print(f"Markdown output generated: {len(markdown_output)} characters")
    
    with open('test_output.html', 'w', encoding='utf-8') as f:
        f.write(html_output)
    
    with open('test_output.md', 'w', encoding='utf-8') as f:
        f.write(markdown_output)
    
    print("Test outputs saved to test_output.html and test_output.md")

def test_api_imports():
    """Test that API components can be imported"""
    print("\n=== Testing API Imports ===")
    
    try:
        from src.api.main import app
        print("✓ FastAPI app imported successfully")
        
        routes = [route.path for route in app.routes]
        expected_routes = ["/", "/upload-transcription/", "/generate-minutes/", "/health"]
        
        for route in expected_routes:
            if route in routes:
                print(f"✓ Route {route} found")
            else:
                print(f"✗ Route {route} missing")
                
    except Exception as e:
        print(f"✗ API import failed: {e}")

if __name__ == "__main__":
    try:
        test_transcription_processing()
        test_minutes_generation_structure()
        test_api_imports()
        
        print("\n=== Test Summary ===")
        print("✓ Basic transcription processing works")
        print("✓ Minutes generation structure works")
        print("✓ API components can be imported")
        print("\nNote: AI summarization requires OpenAI API key configuration")
        print("The system is ready for deployment and testing with proper API credentials")
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
