'''
   A service for allow treasure generation for 
   GURPS Dungeon Fantasy per the #8 suppliment.

   Created on Sep 23, 2015

   @author=brian-thomas
   @email=galactictaco@gmail.com

'''
from flask import jsonify, Flask

# this should reflect both this service and the backing
# assorted libraries
SERVICE_VERSION='1.0.0'

# textmining-ocio library version backing this service
#LIBRARY_VERSION = '0.0.0' 

app = Flask(__name__)

@app.route('/')
def home():
    return 'The DF Treasure Generator service. generator obj:'

@app.route('/generate/<ttype>/<int:number>/', methods=['GET'])
def generate_treasure_full(ttype, number):
    return __generate__treasure(ttype=ttype,number=number)

@app.route('/generate/<int:number>/', methods=['GET'])
def generate_treasure_num_only(number):
    return __generate__treasure(number=number)

def __generate__treasure(ttype="All", number=1):
    try:
        from gdftg.generator import Generator
        generator = Generator(ttype)
        items = generator.run(numberToGenerate=number, max_item_value=None, min_item_value=None, max_enchantments=None)

        results = "<html><body><table>"
        for item in items:
            results += '<tr><td>' + str(item) + "</td></tr>" 
        results += "</table></body></html>"

        return results

    except Exception as ex:
        return str(ex)

if __name__ == '__main__':
    print ("Starting service")

    # TODO: set library version
    #LIBRARY_VERSION=df.__version__

    app.run()

