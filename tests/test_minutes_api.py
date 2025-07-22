import pytest
from unittest.mock import patch, MagicMock
from fastapi import status

class TestMinutesAPI:
    
    @patch('src.modules.azure_openai_client.AzureOpenAI')
    def test_generate_minutes_success(self, mock_azure_client, client, auth_headers, sample_transcript):
        mock_response = MagicMock()
        mock_response.choices[0].message.content = '''
        {
            "summary": "Team discussed project progress and upcoming deadlines",
            "key_points": ["Project update from Bob", "Deadline next week"],
            "action_items": ["Complete remaining tasks", "Prepare for deadline"],
            "next_meeting": "2024-01-22T10:00:00"
        }
        '''
        
        mock_client_instance = MagicMock()
        mock_client_instance.chat.completions.create.return_value = mock_response
        mock_azure_client.return_value = mock_client_instance
        
        response = client.post(
            "/api/v1/minutes/generate",
            json=sample_transcript,
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["meeting_title"] == "Weekly Team Meeting"
        assert data["summary"] == "Team discussed project progress and upcoming deadlines"
        assert len(data["key_points"]) == 2
        assert len(data["action_items"]) == 2
        assert "generated_at" in data
    
    @patch('src.modules.azure_openai_client.AzureOpenAI')
    def test_generate_minutes_invalid_json_response(self, mock_azure_client, client, auth_headers, sample_transcript):
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Invalid JSON response from AI"
        
        mock_client_instance = MagicMock()
        mock_client_instance.chat.completions.create.return_value = mock_response
        mock_azure_client.return_value = mock_client_instance
        
        response = client.post(
            "/api/v1/minutes/generate",
            json=sample_transcript,
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["meeting_title"] == "Weekly Team Meeting"
        assert "Invalid JSON response from AI" in data["summary"]
    
    def test_generate_minutes_no_auth(self, client, sample_transcript):
        response = client.post("/api/v1/minutes/generate", json=sample_transcript)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_generate_minutes_invalid_token(self, client, sample_transcript):
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.post(
            "/api/v1/minutes/generate",
            json=sample_transcript,
            headers=headers
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_generate_minutes_invalid_data(self, client, auth_headers):
        invalid_data = {
            "meeting_title": "",
            "participants": [],
            "transcript_text": ""
        }
        
        response = client.post(
            "/api/v1/minutes/generate",
            json=invalid_data,
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    @patch('src.modules.azure_openai_client.AzureOpenAI')
    def test_generate_minutes_azure_api_error(self, mock_azure_client, client, auth_headers, sample_transcript):
        mock_client_instance = MagicMock()
        mock_client_instance.chat.completions.create.side_effect = Exception("Azure API Error")
        mock_azure_client.return_value = mock_client_instance
        
        response = client.post(
            "/api/v1/minutes/generate",
            json=sample_transcript,
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Failed to generate meeting minutes" in response.json()["detail"]
