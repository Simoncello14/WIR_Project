import json, os
counter = 0
flag= 0
dictionary = {} # key is the user, item list of domain twiited

path_to_json = '/home/giovanni/PycharmProjects/ProgettoWIR/git/WIR_Project-master/domain2users/'
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

with open('/home/giovanni/PycharmProjects/ProgettoWIR/user2doms_40.json', 'r') as myfile:
    data=myfile.read()

obj = json.loads(data)

for file in range (0, len(json_files)): #pick a file at time
    file_position = '/home/giovanni/PycharmProjects/ProgettoWIR/git/WIR_Project-master/domain2users/' + json_files[file]
    with open(file_position, 'r') as myfile1: #open the file
        data1 = myfile1.read()
        obj3 = json.loads(data1)
    for user_for_domain in obj3: #analyze the user
        if counter < 50: #number of user pick from obj3
             for users_from_dataset in obj:
                 if user_for_domain == users_from_dataset:
                     if user_for_domain in dictionary :
                         flag=flag+1
                     else:
                         counter = counter + 1
                         dictionary[user_for_domain] = obj[user_for_domain]
                         break
        else:
            counter = 0
            break

with open('dataset.json', 'w') as outfile:
    json.dump(dictionary, outfile)
print(len(dictionary))