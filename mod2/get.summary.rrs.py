from flask import Flask

app = Flask(__name__)


@app.route("/get_summary_rss/<string:file_path>")
def get_summary_rss(file_path):
    count = 0
    with open('output_file.txt') as book:
        lines = book.readlines()
        for line in lines[1:]:
            array = line.split()
            count += int(array[5])
        return f'{str(count / 1048576)} MiB, {str(count / 1024)} KiB, {str(count)} B'


if __name__ == '__main__':
    app.run(debug=True)
