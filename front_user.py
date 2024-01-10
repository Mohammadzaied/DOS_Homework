import json
import requests
client_url='http://localhost:5000'
while True:
        print("\n"+"Please Choose the method number: ")
        print("1-Info.")
        print("2-Search.")
        print("3-Purchase.")
        print("4-Add.")
        print("5-End.")
        user_input = int(input())
        if user_input==1:
                print('\nplease enter id:')
                user_input=input().strip()
                catalog_response = requests.get(f"{client_url}/info/{user_input}")
                json_string = json.dumps(catalog_response.json() ,indent=4)
                print("\n"+json_string)  
        elif user_input==2:
                print('\nplease enter name topic:')
                user_input=input().strip()
                catalog_response = requests.get(f"{client_url}/search/{user_input}")
                json_string = json.dumps(catalog_response.json() ,indent=4)
                print("\n"+json_string)
        elif user_input==3:
                print('\nplease enter id:')
                user_input=input().strip()
                catalog_response = requests.get(f"{client_url}/purchase/{user_input}")
                json_string = json.dumps(catalog_response.json() ,indent=4)
                print("\n"+json_string)
        elif user_input==4:
                print('\nplease enter id:')
                user_input=input().strip()
                catalog_response = requests.get(f"{client_url}/add/{user_input}")
                json_string = json.dumps(catalog_response.json() ,indent=4)
                print("\n"+json_string)
        elif user_input==5:
            exit()

        else:   
             print('Wrong choice')
