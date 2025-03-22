#flask mein app means website
from flask import Flask, render_template
from flask_pymongo import PyMongo 

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)
@app.route('/') #yha pe slash ke baad jo v lgaoge wo change krete rhega.endpoint aise bnte h
def home():
    mongo.db.inventory.insert_one({"a":1})
    return render_template('index.html')
   #  return "my World"
   #render ka use return ke saath hota

if __name__ == "__main__":
    app.run(debug=True) #we can change port by changing port here,debug=true use krke jo v bug hoga wo browser m hi aajayega
