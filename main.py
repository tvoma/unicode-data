from flask import Flask, render_template, url_for, request
import unicodedata

app = Flask(__name__)

# HOME
@app.route("/")
def index():

    return render_template('index.html')


# SEARCH
@app.route("/search/", methods=['GET', 'POST'])
def search():

    codepoints = []
    results = []
    error = ''
     
    q = request.args.get('q')

    if q != '' and q != None:

        # codepoint from character
        if len(q) == 1 and q != None:
        
            q = ord(q)
            codepoints.append(str(q))

        # codepoint from U+HEX
        elif q[0:2] == 'U+' or q[0:2] == '0x' and int(len(q)) > 1:

            q = q[2:]
            q = int(q, 16)
            codepoints.append(str(q))

        # codepoint from unicode name
        elif int(len(q)) > 2 and q[0:2] != 'U+' and q.isdigit() == False:

            r = range(1, 230000)
            q = q.upper()

            for i in r:
                
                n = unicodedata.name(chr(i), '')
                if q in n:
                    codepoints.append(i)

        # codepoint from codepoint
        elif q.isdigit() and int(len(q)) > 2:

            try:

                testQ = int(q)
                chr(testQ)
                codepoints.append(str(q))

            except ValueError:

                error = "Codepoint n'existe pas"

        else:

            error = 'Aucun resultat'


    if len(codepoints) != 0:

        for c in codepoints:

            result = {}

            result['codepoint'] = c
            result['character'] = chr(int(c))
            result['name'] = unicodedata.name(result['character'])

            results.append(result)
    else:

        error = "Aucun resultat..."


    return render_template('search.html', results=results, error=error)



# UNICODE
@app.route("/unicode/<codepoint>")
def unicode(codepoint):

    result = {}

    result['codepoint'] = codepoint
    result['character'] = chr(int(codepoint))
    result['hex'] = hex(int(codepoint))
    result['binary'] = bin(int(codepoint))
    result['pycode'] = '\\u' + result['hex'][2:]
    result['name'] = unicodedata.name(result['character'])
    result['category'] = unicodedata.category(result['character'])
    result['class'] = unicodedata.bidirectional(result['character'])

    return render_template('unicode.html', result=result)