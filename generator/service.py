'''
   A service for allow treasure generation for 
   GURPS Dungeon Fantasy per the #8 suppliment.

   Created on Sep 23, 2015

   @author=brian-thomas
   @email=galactictaco@gmail.com

'''
from flask import jsonify, request, render_template, Flask
from gdftg.generator import Generator
import gdftg

# this should reflect both this service and the backing
# assorted libraries
SERVICE_VERSION='v1'

# textmining-ocio library version backing this service
LIBRARY_VERSION = gdftg.version

app = Flask(__name__)

def __generate__treasure(ttype="All", number=1):
    try:
        generator = Generator(ttype)
        items = generator.run(numberToGenerate=number, max_item_value=None, min_item_value=None, max_enchantments=None)

        results = "<html><body><table>"
        for item in items:
            results += '<tr><td>' + str(item) + "</td></tr>" 
        results += "</table></body></html>"

        return results

    except Exception as ex:
        return str(ex)

@app.route('/')
def home():
    gen = Generator()
    ttypes = sorted(list(gen.treasureClasses()))
    return render_template('home.html', version=SERVICE_VERSION, \
                            ttypes=ttypes, service_url=request.host)

@app.route('/generate/<int:number>/<ttype>/', methods=['GET'])
def generate_treasure_full(ttype, number):
    return __generate__treasure(ttype=ttype,number=number)

@app.route('/generate/<int:number>/', methods=['GET'])
def generate_treasure_num_only(number):
    return __generate__treasure(number=number)

@app.route('/generate/', methods=['GET'])
def generate_treasure_single():
    return __generate__treasure()

if __name__ == '__main__':
    app.run()

