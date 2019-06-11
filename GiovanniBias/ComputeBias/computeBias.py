import json
closest_domain = {} #
bias =  {}
closest_domain_variable = ''
bias_variable = 0
greatest_bias = 0
domain_seed_appeare = False
domain_user_appeare = False

list_dataset_seed = {'abcnews.go.com': 0, 'edition.cnn.com': 0, 'jacobinmag.com': 0, 'nypost.com': 0,
                     'slate.com': 0, 'spectator.org': 0, 'thefederalist.com': 0, 'thehill.com': 0,
                     'theintercept.com': 0, 'www.alternet.org': 0, 'www.apnews.com': 0, 'www.bbc.com': 0,
                     'www.bloomberg.com': 0, 'www.breitbart.com': 0, 'www.buzzfeednews.com': 0, 'www.cbs.com': 0,
                     'www.cnn.com': 0, 'www.csmonitor.com': 0, 'www.dailywire.com': 0, 'www.economist.com': 0,
                     'www.examinerlive.co.uk': 0, 'www.foxnews.com': 0, 'www.huffpost.com': 0,
                     'www.motherjones.com': 0, 'www.msnbc.com': 0, 'www.nationalreview.com': 0, 'www.nbc.com': 0,
                     'www.newsmax.com': 0, 'www.newyorker.com': 0, 'www.npr.org': 0, 'www.nytimes.com': 0,
                     'www.politico.com': 0, 'www.reuters.com': 0, 'www.theatlantic.com': 0,
                     'www.thedailybeast.com': 0, 'www.theguardian.com': 0, 'www.thenation.com': 0,
                     'www.usatoday.com': 0, 'www.vox.com': 0, 'www.washingtonpost.com': 0,
                     'www.washingtontimes.com': 0, 'www.wsj.com': 0}


with open('/home/giovanni/PycharmProjects/ProgettoWIR/listDomain.json', 'r') as myfile:
    data = myfile.read()

obj = json.loads(data)

with open('/home/giovanni/PycharmProjects/ProgettoWIR/dataset.json', 'r') as myfile1:
    data1 = myfile1.read()

obj3 = json.loads(data1)


for domain in obj:
    for domain_seed in list_dataset_seed:
        for user in obj3:
            for domains_user in range(0,len(obj3[user])):
                if obj3[user][domains_user]== domain:
                    domain_user_appeare =True
                if obj3[user][domains_user] == domain_seed:
                    domain_seed_appeare = True
                if domain_seed_appeare and domain_user_appeare:
                    bias_variable = bias_variable +1
                    domain_user_appeare = False
                    domain_seed_appeare = False
                    break
            domain_user_appeare = False
            domain_seed_appeare = False
        if bias_variable > greatest_bias:
            greatest_bias = bias_variable
            closest_domain_variable = domain_seed
            bias_variable = 0
        bias_variable=0
    closest_domain[domain] = closest_domain_variable
    bias[domain] = greatest_bias
    greatest_bias=0
    print(domain)
    print(closest_domain[domain])
    print(bias[domain])

with open('bias.json', 'w') as outfile:
    json.dump(bias, outfile)

with open('closestDomain.json', 'w') as outfile:
    json.dump(closest_domain, outfile)

