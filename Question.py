from pymongo import MongoClient

# Connect to MongoDB (update URI if using Atlas)
client = MongoClient("mongodb://localhost:27017/")

# Database & Collection
db = client["CameraSystem"]
collection = db["FAQs"]

# New Q&A list (camera-related + chatbot strategy)
qa_list = [
    {"question": "How many cameras can be connected simultaneously?",
     "answer": "The system supports several dozen cameras depending on the server capacity."},

    {"question": "What types of cameras are compatible?",
     "answer": "Most IP cameras with RTSP or HTTP protocol are compatible."},

    {"question": "Do the cameras require specific power supply?",
     "answer": "IP cameras require standard electrical power or PoE (Power over Ethernet)."},

    {"question": "Can the name or location of an already added camera be changed?",
     "answer": "Yes, through the camera settings in the platform."},

    {"question": "How to delete a camera?",
     "answer": "From the camera list, select the one to delete and click on “Delete.”"},

    {"question": "Do the cameras record continuously?",
     "answer": "Yes, they record continuously or according to a defined schedule."},

    {"question": "How long are the videos stored?",
     "answer": "The duration depends on the settings, generally 24 hours."},

    {"question": "Can a PDF report be generated from incidents?",
     "answer": "Yes, a PDF report generator is available."},

    {"question": "Does the system keep an activity log?",
     "answer": "Yes, all user actions are recorded in a log."},

    # Chatbot Strategy (stored as Q&A so chatbot can explain its design)
    {"question": "What is the complete strategy for a chatbot with NLP?",
     "answer": (
         "Knowledge Base Collection and Organization: Gather essential Q&A and store them in MongoDB. "
         "Data Preprocessing: Clean text (remove spelling errors, normalize case, remove stop words, apply stemming/lemmatization). "
         "Vectorization: Convert text into vectors (e.g., TF–IDF). "
         "Similarity Measurement: Use cosine similarity to match user queries with stored questions. "
         "Implementation: Process queries, find closest match, and retrieve answer. "
         "Integration: Package chatbot as REST API (Django/Flask) or embed as a widget in a web/mobile app."
     )}
]

# Insert new Q&A (ignoring duplicates)
collection.insert_many(qa_list)

print("Inserted", len(qa_list), "new Q&A into MongoDB successfully!")
