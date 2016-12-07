import csv, json
fr = open('chinese.json', 'r')
fw = open('wikichineseno.json', 'w')
f = open('wikichineseyes.json', 'w')

for line in fr:
    l = json.loads(line)
    if  not 'zh' in l['labels']:
        fw.write(json.dumps(l) + '\n')
    else:
        f.write(json.dumps(l) + '\n')