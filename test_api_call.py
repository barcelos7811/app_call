import json, requests
import os

def buscar_dados():
    # request = requests.get("http://localhost:3002/api/todo")
    os.environ['NO_PROXY'] = '127.0.0.1'
    r = requests.get('http://127.0.0.1:5000/list_all_call')
    print('testando api')
    print(r.content)

    print(r)
    print(r.content)

    #print(sys.stdout.encoding)

if __name__ == '__main__':
    buscar_dados()
