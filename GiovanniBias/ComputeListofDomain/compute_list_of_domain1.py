import json
flag = 0
domain_notSeed = ''
list_of_domain = {}
list_dataset_seed ={'abcnews.go.com':0,'edition.cnn.com':0,'jacobinmag.com':0,'nypost.com':0,'slate.com':0,'spectator.org':0,'thefederalist.com':0,'thehill.com':0,'theintercept.com':0,'www.alternet.org':0,'www.apnews.com':0,'www.bbc.com':0,'www.bloomberg.com':0,'www.breitbart.com':0,'www.buzzfeednews.com':0,'www.cbs.com':0,'www.cnn.com':0,'www.csmonitor.com':0,'www.dailywire.com':0,'www.economist.com':0,'www.examinerlive.co.uk':0,'www.foxnews.com':0,'www.huffpost.com':0,'www.motherjones.com':0,'www.msnbc.com':0,'www.nationalreview.com':0,'www.nbc.com':0,'www.newsmax.com':0,'www.newyorker.com':0,'www.npr.org':0,'www.nytimes.com':0,'www.politico.com':0,'www.reuters.com':0,'www.theatlantic.com':0,'www.thedailybeast.com':0,'www.theguardian.com':0,'www.thenation.com':0,'www.usatoday.com':0,'www.vox.com':0,'www.washingtonpost.com':0,'www.washingtontimes.com':0,'www.wsj.com':0}


with open('/home/giovanni/PycharmProjects/ProgettoWIR/dataset.json', 'r') as myfile:
    data = myfile.read()
c=0
obj = json.loads(data)
for user in obj:
    for domain_Dataset in range(0,len(obj[user])):
        for domain_inSeed in list_dataset_seed:
            if obj[user][domain_Dataset] == domain_inSeed :
                flag=flag+1
            else:
                domain_notSeed= obj[user][domain_Dataset]
                list_of_domain[domain_notSeed]=0


with open('listDomain.json', 'w') as outfile:
    json.dump(list_of_domain, outfile)
print(len(list_of_domain))
