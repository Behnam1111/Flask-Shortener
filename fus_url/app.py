import time
import datetime
from hashids import Hashids
from flask import Flask, render_template, request, flash, redirect, url_for, g
from user_agents import parse
from redis import Redis
from fus_url.dao.request_dao import RequestDao
from fus_url.dao.url_dao import UrlDao

redis = Redis(host='redis', port=6379, decode_responses=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this should be a secret random string'

hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])


@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)
    g.struct_time = time.localtime()


@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        url = request.form['url']
        if not url:
            flash('The URL is required!')
            return redirect(url_for('index'))
        url_id = UrlDao().get_last_url_id()
        hashid = hashids.encode(url_id)
        short_url = request.host_url + hashid
        UrlDao().add(short_url, url, g.request_start_time)
        if not redis.exists(short_url):
            redis.set(short_url, url)
        return render_template('index.html', short_url=short_url)

    return render_template('index.html')


@app.route('/<id>')
def url_redirect(id):
    original_id = hashids.decode(id)
    short_url = request.host_url + id

    if original_id:
        if redis.exists(short_url):
            original_url = redis.get(short_url)
        else:
            original_url = UrlDao().get_url_by_short_url(short_url=short_url)
        user_agent = parse(request.headers["User-Agent"])
        mobile = user_agent.is_mobile
        elapsed_time = g.request_time()
        ip_address = request.remote_addr
        if mobile:
            mobile_desktop_type = 'mobile'
        else:
            mobile_desktop_type = 'desktop'
        RequestDao().add(ip_address, mobile_desktop_type, g.request_start_time, elapsed_time, short_url)
        return redirect(original_url)
    else:
        flash('Invalid URL')
        return redirect(url_for('index'))


@app.route('/stats')
def stats():
    db_urls = RequestDao().get_all_requests()
    urls = [url for url in db_urls]
    for url in urls:
        url.request_timestamp = datetime.datetime.fromtimestamp(url.request_timestamp)
        url.original_url = UrlDao().get_url_by_short_url(url.short_url)

    return render_template('stats.html', urls=urls)


if __name__ == '__main__':
    UrlDao().create_table()
    RequestDao().create_table()
    app.run(host="0.0.0.0", port=5000)
