import requests

API_URL = "http://127.0.0.1:8000/api/chat/"  # URL de ton API

def test_chatbot(question: str):
    payload = {"question": question}
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            data = response.json()
            print(" Question :", data["question"])
            print(" Réponse :", data["answer"])
            print(" Source :", data["source"])
        else:
            print(f" Erreur {response.status_code} :", response.text)
    except requests.exceptions.ConnectionError:
        print(" Impossible de se connecter à l'API. Vérifie que Django tourne sur le port 8000.")

if __name__ == "__main__":
    test_question = "Qu’est-ce que CitizenLab Sénégal ?"
    test_chatbot(test_question)
