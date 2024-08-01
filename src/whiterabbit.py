import pandas as pd
import matplotlib.pyplot as plt
import regex as re
from ucimlrepo import fetch_ucirepo
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.impute import KNNImputer
from sklearn.tree import DecisionTreeClassifier
import pickle


class WhiteRabbit:
    data = fetch_ucirepo(id=73)
    knn = KNNImputer()
    tree_of_wisdom = DecisionTreeClassifier(random_state=42)
    key = {}

    def __init__(self):
        self.data_dusting()
        self.the_process()

    def data_dusting(self):
        self.data = pd.concat([self.data.data.features, self.data.data.targets], axis=1)
        for i in self.data.drop(columns='poisonous').columns:
            dic = {j: 0 for j in self.data[i].unique()}
            count = 1
            for j in dic.keys():
                dic[j] += count
                count += 1
            self.data[i] = self.data[i].map(dic)
            self.key[i] = dic
        self.y = self.data['poisonous'].map({'p':0, 'e':1})
        self.x = pd.DataFrame(self.knn.fit_transform(self.data.drop(columns='poisonous')), columns=self.data.drop(columns='poisonous').columns, index=self.data.index)
        for i in self.x.columns:
            self.x[i] = self.x[i].apply(int)
        self.xtr, self.xte, self.ytr, self.yte = train_test_split(self.x, self.y, test_size=.2, random_state=42)

    def the_process(self):
        self.tree_of_wisdom.fit(self.xtr, self.ytr)
        importances = self.tree_of_wisdom.feature_importances_
        self.xte = self.xte[self.xte.columns[importances > 0]]
        self.xtr = self.xtr[self.xtr.columns[importances > 0]]
        self.key = {k:v for k, v in self.key.items() if k in self.xtr.columns}
        self.tree_of_wisdom.fit(self.xtr, self.ytr)
        pred = self.tree_of_wisdom.predict(self.xte)
        with open('./models/fun_guy.dat', 'wb') as file:
            pickle.dump(self.tree_of_wisdom, file)

    def laziest(self, col, key):
        a = self.key[col]
        b = re.findall(r'=\w', key)
        c = re.findall(r'\w+=', key)
        d = {i[-1]:j[:-1] for i, j in zip(b, c)}
        result = (f'\t<label for="{col}">INSERT QUESTION HERE</label>\n'
                  f'\t\t<select id="{col+'_'}" name="{col+'_'}">\n')
        if len(d) > len(a):
            d = {i: d[i] for i in a.keys()}
        for k, v in d.items():
            result += f'\t\t\t<option value="{a[k]}">{v}</option>\n'
        result += '\t\t</select>\n'
        return result

    def lazier_still(self):
        chonker = """     
     1. cap-shape:                bell=b,conical=c,convex=x,flat=f,knobbed=k,sunken=s

     2. cap-surface:              fibrous=f,grooves=g,scaly=y,smooth=s

     3. cap-color:                brown=n,buff=b,cinnamon=c,gray=g,green=r,pink=p,purple=u,red=e,white=w,yellow=y

     4. bruises?:                 bruises=t,no=f

     5. odor:                     almond=a,anise=l,creosote=c,fishy=y,foul=f,musty=m,none=n,pungent=p,spicy=s

     6. gill-attachment:          attached=a,descending=d,free=f,notched=n

     7. gill-spacing:             close=c,crowded=w,distant=d

     8. gill-size:                broad=b,narrow=n

     9. gill-color:               black=k,brown=n,buff=b,chocolate=h,gray=g,green=r,orange=o,pink=p,purple=u,red=e,white=w,yellow=y

    10. stalk-shape:              enlarging=e,tapering=t

    11. stalk-root:               bulbous=b,club=c,cup=u,equal=e,rhizomorphs=z,rooted=r,missing=?

    12. stalk-surface-above-ring: fibrous=f,scaly=y,silky=k,smooth=s

    13. stalk-surface-below-ring: fibrous=f,scaly=y,silky=k,smooth=s

    14. stalk-color-above-ring:   brown=n,buff=b,cinnamon=c,gray=g,orange=o,pink=p,red=e,white=w,yellow=y

    15. stalk-color-below-ring:   brown=n,buff=b,cinnamon=c,gray=g,orange=o,pink=p,red=e,white=w,yellow=y

    16. veil-type:                partial=p,universal=u

    17. veil-color:               brown=n,orange=o,white=w,yellow=y

    18. ring-number:              none=n,one=o,two=t

    19. ring-type:                cobwebby=c,evanescent=e,flaring=f,large=l,none=n,pendant=p,sheathing=s,zone=z

    20. spore-print-color:        black=k,brown=n,buff=b,chocolate=h,green=r,orange=o,purple=u,white=w,yellow=y

    21. population:               abundant=a,clustered=c,numerous=n,scattered=s,several=v,solitary=y

    22. habitat:                  grasses=g,leaves=l,meadows=m,paths=p,urban=u,waste=w,woods=d
    """
        a = re.findall(r'\S+:', chonker)
        b = re.findall(r'\s+\S+\n', chonker)
        c = {i[:-1]: j.strip() for i, j in zip(a, b) if i[:-1] in self.xtr.columns}
        result = ''
        for k, v in c.items():
            result += self.laziest(k, v)
        print(result)





if __name__ == '__main__':
    WhiteRabbit()