# flask packages
from flask import Flask, jsonify
from yt_dlp import YoutubeDL

app = Flask(__name__)
  
@app.route('/post/<int:id>')
def show_post(id):
    # Shows the post with given id.
    return f'This post has the id {id}'
  
@app.route('/user/<username>')
def show_user(username):
    # Greet the user
    return f'Hello {username} !'
  
# Pass the required route to the decorator.
@app.route("/hello")
def hello():
    return "Hello, Welcome to GeeksForGeeks"
    
@app.route("/")
def index():
    return "Homepage of GeeksForGeeks"

@app.route('/tt/<oldurl>')
def get(oldurl):
    infourl = oldurl.split("/tt/", 1)[0].replace(":/","://")

    print('infourl is ' + infourl)

    with YoutubeDL() as ydl:
        result = ydl.extract_info('https://vm.tiktok.com/'+infourl, download=False)
    
    for res in result["formats"]:
        if 'tiktokv' in res["url"]:
            shortUrl = res["url"]
            break
    

    return  shortUrl #jsonify({'result': result})

def getFormat(ctx):
    # formats are already sorted worst to best
    formats = ctx.get('formats')[::-1]

    # acodec='none' means there is no audio
    best_video = next(f for f in formats
                      if f['vcodec'] != 'none' and f['acodec'] == 'none')

    # find compatible audio extension
    audio_ext = {'mp4': 'm4a', 'webm': 'webm'}[best_video['ext']]
    # vcodec='none' means there is no video
    best_audio = next(f for f in formats if (
        f['acodec'] != 'none' and f['vcodec'] == 'none' and f['ext'] == audio_ext))

    yield {
        # These are the minimum required fields for a merged format
        'format_id': f'{best_video["format_id"]}+{best_audio["format_id"]}',
        'ext': best_video['ext'],
        'requested_formats': [best_video, best_audio],
        # Must be + separated list of protocols
        'protocol': f'{best_video["protocol"]}+{best_audio["protocol"]}'
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0",port="5000",debug=True)
