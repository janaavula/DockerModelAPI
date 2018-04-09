import requests,json
headers = {'Content-type':'application/json'}
imageurl = 'http://www.homedepot.com/catalog/productImages/1000/a6/a619a055-6979-4b47-b0da-5dfa09d6ca2b_1000.jpg'
data = {'url':imageurl}
res = requests.post('http://localhost:5432/api/v1/classify_image', data=json.dumps(data), headers=headers)
print("predicted probabilities for each category")
print(res.text)
