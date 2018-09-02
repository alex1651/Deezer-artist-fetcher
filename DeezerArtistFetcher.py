from client import Client
import json
client = Client(app_id='	296644', app_secret='04d7ebb46868db98dffc28a18e8bfb12')

input_file_name = "list.txt"
output_file_name = "output.txt"

with open(output_file_name, 'w', encoding="utf-8" ) as outfile1:
    with open(input_file_name, "r", encoding="utf-8") as ins:
        for line in ins:
            response = client.search(line.strip(), relation=None)
            data = response.json()
            artist = ''
            for dataset in data['data'] :
                # print(dataset['artist']['name'].lower())
                if dataset['artist']['name'].lower().strip() == line.lower().strip():
                    artist = dataset['artist']['name'] +' - '+dataset['artist']['link']+'\n'

            print('api response output : $s',artist)
            print('')
            if len(data['data']) > 0 :
                # print (data['data'][0]['artist'])
                outfile1.write(artist)
                # json.dump(data['data'][0]['artist'] , outfile1, indent=4)



