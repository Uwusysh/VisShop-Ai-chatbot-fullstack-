import json
from unittest.mock import patch, MagicMock
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from chatbot_api.utils import collection
from chatbot_api.nlp import get_best_answer


class ChatbotViewTests(APITestCase):
    def setUp(self):
        self.client = Client()
        self.chat_url = reverse('chat')
        
        # Mock FAQ data
        self.mock_qa_list = [
            {
                "question": "How many cameras can be connected simultaneously?",
                "answer": "The system supports several dozen cameras depending on the server capacity."
            },
            {
                "question": "What types of cameras are compatible?",
                "answer": "Most IP cameras with RTSP or HTTP protocol are compatible."
            }
        ]

    @patch('chatbot_api.views.collection.find')
    @patch('chatbot_api.views.get_best_answer')
    def test_chatbot_view_success(self, mock_get_best_answer, mock_collection_find):
        """Test successful chatbot response"""
        # Mock the database response
        mock_collection_find.return_value = self.mock_qa_list
        mock_get_best_answer.return_value = "Mocked answer from knowledge base"
        
        data = {"query": "How many cameras can I connect?"}
        response = self.client.post(
            self.chat_url, 
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("answer", response.data)
        mock_get_best_answer.assert_called_once_with(
            "How many cameras can I connect?", 
            self.mock_qa_list
        )

    def test_chatbot_view_missing_query(self):
        """Test chatbot view with missing query parameter"""
        data = {}
        response = self.client.post(
            self.chat_url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should handle empty query gracefully

    @patch('chatbot_api.views.collection.find')
    def test_chatbot_view_database_error(self, mock_collection_find):
        """Test chatbot view when database fails"""
        mock_collection_find.side_effect = Exception("Database connection failed")
        
        data = {"query": "Test query"}
        response = self.client.post(
            self.chat_url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Should still return 200 but with error handling
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class NLPModuleTests(TestCase):
    def setUp(self):
        self.qa_list = [
            {
                "question": "How many cameras can be connected simultaneously?",
                "answer": "The system supports several dozen cameras depending on the server capacity."
            },
            {
                "question": "What types of cameras are compatible?",
                "answer": "Most IP cameras with RTSP or HTTP protocol are compatible."
            }
        ]

    @patch('chatbot_api.nlp.embedder.encode')
    @patch('chatbot_api.nlp.util.cos_sim')
    def test_get_best_answer_high_similarity(self, mock_cos_sim, mock_encode):
        """Test get_best_answer with high similarity match"""
        # Mock embeddings and similarity
        mock_encode.side_effect = [
            MagicMock(),  # query_embedding
            MagicMock()   # question_embeddings
        ]
        
        # Mock high similarity score (0.95)
        mock_similarity = MagicMock()
        mock_similarity.argmax.return_value.item.return_value = 0
        mock_similarity.__getitem__.return_value.__getitem__.return_value.item.return_value = 0.95
        mock_cos_sim.return_value = mock_similarity
        
        answer = get_best_answer("cameras connected", self.qa_list)
        
        self.assertEqual(answer, self.qa_list[0]["answer"])

    @patch('chatbot_api.nlp.embedder.encode')
    @patch('chatbot_api.nlp.util.cos_sim')
    @patch('chatbot_api.nlp.client.chat.completions.create')
    def test_get_best_answer_low_similarity_fallback(self, mock_groq, mock_cos_sim, mock_encode):
        """Test get_best_answer with low similarity falling back to Groq"""
        # Mock embeddings and similarity
        mock_encode.side_effect = [
            MagicMock(),  # query_embedding
            MagicMock()   # question_embeddings
        ]
        
        # Mock low similarity score (0.5)
        mock_similarity = MagicMock()
        mock_similarity.argmax.return_value.item.return_value = 0
        mock_similarity.__getitem__.return_value.__getitem__.return_value.item.return_value = 0.5
        mock_cos_sim.return_value = mock_similarity
        
        # Mock Groq response
        mock_groq_response = MagicMock()
        mock_groq_response.choices[0].message.content = "Mocked Groq response"
        mock_groq.return_value = mock_groq_response
        
        answer = get_best_answer("random question", self.qa_list, threshold=0.9)
        
        self.assertEqual(answer, "Mocked Groq response")
        mock_groq.assert_called_once()

    def test_get_best_answer_empty_qa_list(self):
        """Test get_best_answer with empty QA list"""
        with patch('chatbot_api.nlp.client.chat.completions.create') as mock_groq:
            mock_groq_response = MagicMock()
            mock_groq_response.choices[0].message.content = "Groq fallback answer"
            mock_groq.return_value = mock_groq_response
            
            answer = get_best_answer("test question", [])
            
            self.assertEqual(answer, "Groq fallback answer")


class URLTests(TestCase):
    def test_home_url(self):
        """Test home URL returns correct response"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Chatbot backend is running", response.content)

    def test_chat_url_exists(self):
        """Test chat URL exists"""
        response = self.client.get('/chat/')
        # POST is required, GET might return 405 Method Not Allowed
        self.assertIn(response.status_code, [200, 405])


class UtilityTests(TestCase):
    def test_collection_connection(self):
        """Test MongoDB collection connection"""
        # This is a simple test to verify the collection object exists
        self.assertIsNotNone(collection)
        self.assertEqual(collection.name, "FAQs")