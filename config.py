import json

def save_to_json(info, path = 'login_params.json'):
    with open(path, 'w') as f:
        json.dump(info, f, indent=2)

def main():
    info = {'CONSUMER_KEY': 'YVbi4D8JuPKlUzBJpRsmMKZmp',
        'CONSUMER_SECRET': 'FaKzPfxnUyhj9MiPqbYlFehFOdQOh6lVBkwWsx6KZGHt5Ucw1X',
        'ACCESS_TOKEN': '1170987661978300416-zL7VW8nE19d9X7dlIzxh77WUnTrkCZ',
        'ACCESS_SECRET': 'g8VttjP6hCIM7E9KTXlOfOcFT2hCOh8cmhodwyQRctCnA'}

    save_to_json(info=info)

if __name__ == '__main__':
    main()