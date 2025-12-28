from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import collection
from .nlp import get_best_answer

class ChatbotView(APIView):
    def post(self, request):
        user_query = request.data.get("query", "")
        try:
            qa_list = list(collection.find({}, {"_id": 0}))
        except Exception as e:
            print(f"DB error: {e}")
            qa_list = []

        answer = get_best_answer(user_query, qa_list)
        return Response({"answer": answer})

