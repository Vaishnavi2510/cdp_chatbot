from flask import Flask, request, render_template
from doc_indexer import DocIndexer

app = Flask(__name__)
doc_indexer = DocIndexer()
print("Indexing Documents... please wait...")
doc_indexer.build_index()
print("Indexing Complete")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        query = request.form["query"]
        cdp_name = request.form.get("cdp_name")
        results = doc_indexer.search(query, cdp_name)
        return render_template("results.html", query=query, results=results,cdp_name=cdp_name)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)