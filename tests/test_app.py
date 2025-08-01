import pytest
import json
import sys
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import redis
import requests
from responses import RequestsMock

# Import the functions to test
from app import send, make_request, main


class TestSendFunction:
    """Test cases for the send function"""
    
    @patch('app.redis.Redis')
    def test_send_success(self, mock_redis):
        """Test successful message sending to Redis"""
        # Arrange
        mock_redis_instance = Mock()
        mock_redis.return_value = mock_redis_instance
        message = '{"test": "message"}'
        
        # Act
        send(message)
        
        # Assert
        mock_redis.assert_called_once_with(host='localhost', port=6379)
        mock_redis_instance.publish.assert_called_once_with('messages', message)
    
    @patch('app.redis.Redis')
    def test_send_redis_error(self, mock_redis):
        """Test Redis error handling"""
        # Arrange
        mock_redis_instance = Mock()
        mock_redis_instance.publish.side_effect = redis.RedisError("Connection failed")
        mock_redis.return_value = mock_redis_instance
        message = '{"test": "message"}'
        
        # Act & Assert
        with pytest.raises(redis.RedisError):
            send(message)
    
    @patch('app.redis.Redis')
    def test_send_unexpected_error(self, mock_redis):
        """Test unexpected error handling"""
        # Arrange
        mock_redis_instance = Mock()
        mock_redis_instance.publish.side_effect = Exception("Unexpected error")
        mock_redis.return_value = mock_redis_instance
        message = '{"test": "message"}'
        
        # Act & Assert
        with pytest.raises(Exception):
            send(message)


class TestMakeRequestFunction:
    """Test cases for the make_request function"""
    
    @patch('app.requests.get')
    def test_make_request_success(self, mock_get):
        """Test successful HTTP request"""
        # Arrange
        mock_response = Mock()
        mock_response.json.return_value = {"data": "test"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Act
        result = make_request("http://test.com", "test request")
        
        # Assert
        assert result == {"data": "test"}
        mock_get.assert_called_once_with("http://test.com", timeout=30)
    
    @patch('app.requests.get')
    def test_make_request_http_error(self, mock_get):
        """Test HTTP error handling"""
        # Arrange
        mock_get.side_effect = requests.exceptions.RequestException("HTTP Error")
        
        # Act & Assert
        with pytest.raises(requests.exceptions.RequestException):
            make_request("http://test.com", "test request")
    
    @patch('app.requests.get')
    def test_make_request_json_error(self, mock_get):
        """Test JSON decode error handling"""
        # Arrange
        mock_response = Mock()
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Act & Assert
        with pytest.raises(json.JSONDecodeError):
            make_request("http://test.com", "test request")
    
    @patch('app.requests.get')
    def test_make_request_unexpected_error(self, mock_get):
        """Test unexpected error handling"""
        # Arrange
        mock_get.side_effect = Exception("Unexpected error")
        
        # Act & Assert
        with pytest.raises(Exception):
            make_request("http://test.com", "test request")


class TestMainFunction:
    """Test cases for the main function"""
    
    @patch('app.make_request')
    @patch('app.send')
    @patch('app.config.url_tenders', 'http://test.com/tenders')
    @patch('app.config.url_by_code')
    def test_main_success(self, mock_url_by_code, mock_send, mock_make_request):
        """Test successful main function execution"""
        # Arrange
        mock_url_by_code.return_value = 'http://test.com/tender/123'
        
        # Mock tenders list response
        tenders_response = {
            'Listado': [
                {'CodigoExterno': '123'},
                {'CodigoExterno': '456'},
                {'CodigoExterno': '789'},
                {'CodigoExterno': '012'},
                {'CodigoExterno': '345'}
            ]
        }
        
        # Mock individual tender response
        tender_response = {
            'Listado': [{
                'CodigoExterno': '123',
                'Nombre': 'Test Tender',
                'Descripcion': 'Test Description'
            }]
        }
        
        # Mock responses: 1 for tenders list + 5 for individual tenders
        mock_make_request.side_effect = [tenders_response] + [tender_response] * 5
        
        # Act
        main()
        
        # Assert
        # 1 call for tenders list + 5 calls for individual tenders = 6 calls
        assert mock_make_request.call_count == 6
        assert mock_send.call_count == 5
        
        # Verify the message structure (check the last message sent)
        sent_message = json.loads(mock_send.call_args_list[-1][0][0])
        assert sent_message['id'] == 4  # Last tender processed (index 4)
        assert sent_message['status'] == 'pre-processed'
        assert sent_message['payload']['code'] == '123'
        assert sent_message['payload']['title'] == 'Test Tender'
        assert sent_message['payload']['description'] == 'Test Description'
    
    @patch('app.make_request')
    @patch('app.config.url_tenders', 'http://test.com/tenders')
    def test_main_invalid_tenders_response(self, mock_make_request):
        """Test main function with invalid tenders response"""
        # Arrange
        mock_make_request.return_value = {'invalid': 'response'}
        
        # Act & Assert
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1
    
    @patch('app.make_request')
    @patch('app.config.url_tenders', 'http://test.com/tenders')
    def test_main_empty_tenders_list(self, mock_make_request):
        """Test main function with empty tenders list"""
        # Arrange
        mock_make_request.return_value = {'Listado': []}
        
        # Act
        main()
        
        # Assert - should complete without error
        mock_make_request.assert_called_once()
    
    @patch('app.make_request')
    @patch('app.send')
    @patch('app.config.url_tenders', 'http://test.com/tenders')
    @patch('app.config.url_by_code')
    def test_main_individual_tender_error(self, mock_url_by_code, mock_send, mock_make_request):
        """Test main function when individual tender request fails"""
        # Arrange
        mock_url_by_code.return_value = 'http://test.com/tender/123'
        
        tenders_response = {
            'Listado': [
                {'CodigoExterno': '123'},
                {'CodigoExterno': '456'}
            ]
        }
        
        tender_response = {
            'Listado': [{
                'CodigoExterno': '456',
                'Nombre': 'Test Tender 2',
                'Descripcion': 'Test Description 2'
            }]
        }
        
        # First call succeeds (tenders list), second call fails (first tender), third call succeeds (second tender)
        mock_make_request.side_effect = [
            tenders_response,
            requests.exceptions.RequestException("Tender request failed"),
            tender_response  # Response for second tender
        ]
        
        # Act
        main()
        
        # Assert - should handle the error gracefully and continue
        # 1 call for tenders list + 2 calls for individual tenders = 3 calls
        assert mock_make_request.call_count == 3
        # send should be called once for the successful second tender
        assert mock_send.call_count == 1
    
    @patch('app.make_request')
    @patch('app.config.url_tenders', 'http://test.com/tenders')
    def test_main_critical_error(self, mock_make_request):
        """Test main function with critical error"""
        # Arrange
        mock_make_request.side_effect = Exception("Critical error")
        
        # Act & Assert
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1


class TestIntegration:
    """Integration test cases"""
    
    @patch('app.redis.Redis')
    @patch('app.requests.get')
    def test_full_workflow_success(self, mock_get, mock_redis):
        """Test the complete workflow from start to finish"""
        # Arrange
        mock_redis_instance = Mock()
        mock_redis.return_value = mock_redis_instance
        
        # Mock responses
        tenders_response = Mock()
        tenders_response.json.return_value = {
            'Listado': [{'CodigoExterno': '123'}]
        }
        tenders_response.raise_for_status.return_value = None
        
        tender_response = Mock()
        tender_response.json.return_value = {
            'Listado': [{
                'CodigoExterno': '123',
                'Nombre': 'Integration Test Tender',
                'Descripcion': 'Integration Test Description'
            }]
        }
        tender_response.raise_for_status.return_value = None
        
        mock_get.side_effect = [tenders_response, tender_response]
        
        # Act
        main()
        
        # Assert
        assert mock_get.call_count == 2
        mock_redis_instance.publish.assert_called_once()
        
        # Verify the published message
        published_message = mock_redis_instance.publish.call_args[0][1]
        message_data = json.loads(published_message)
        assert message_data['payload']['code'] == '123'
        assert message_data['payload']['title'] == 'Integration Test Tender'


# Test configuration
@pytest.fixture(autouse=True)
def setup_logging():
    """Disable logging during tests to avoid cluttering output"""
    import logging
    logging.getLogger('app').setLevel(logging.ERROR) 