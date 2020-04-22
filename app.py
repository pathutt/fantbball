import sys

from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)


#     cursor.execute("select hitters.id - 763 as rank, hitters.first_name, hitters.last_name, teams.abbr, string_agg(positions.position, ',') as pos, hitter_proj.avg, hitter_proj.r, hitter_proj.rbi, hitter_proj.hr, hitter_proj.sb from hitters INNER JOIN hitter_proj ON (hitters.id = hitter_proj.id)inner join teams on (hitters.team_id = teams.id)inner join hitter_pos on (hitters.id = hitter_pos.hitter_id)inner join positions on (hitter_pos.pos_id = positions.id)GROUP BY 1, 2, 3, 4, 6, 7, 8, 9, 10 ORDER BY 1;")

@app.route('/', methods = ['GET', 'POST'])
def hello_world():
    if request.method == 'GET':
        rows = query_hitters()
        return render_template('main.html', rows=rows)

    if request.method == 'POST':
        categories = request.form.getlist('hitter')
        query = post_query(categories)
        rows = generate_post_table(query)
        num_cols = len(rows[0])
        names = get_table_header(query)
        return render_template('main.html', rows=rows, cols=names, length = num_cols)


@app.route('/catcher')
def get_catcher():
    rows = query_catchers()
    return render_template('main.html', rows=rows)


def connect():
    try:
        conn = psycopg2.connect(host="ec2-54-157-78-113.compute-1.amazonaws.com", database="d1oh3vt134d6nv",
                                user="seawikidnnuwrk", port="5432",
                                password="b22cc1de4f913fcf525204dacad4a53f52b1040551e2caa67515d7d3bdf61f20")
    except:
        print("Not working....")

    return conn.cursor()

def query_hitters():
    cursor = connect();
    cursor.execute("select hitters.id - 763 as rank, hitters.first_name, hitters.last_name, teams.abbr, string_agg("
                   "positions.position, ',') as pos, hitter_proj.avg, hitter_proj.r, hitter_proj.rbi, hitter_proj.hr, "
                   "hitter_proj.sb from hitters INNER JOIN hitter_proj ON (hitters.id = hitter_proj.id)inner join "
                   "teams on (hitters.team_id = teams.id)inner join hitter_pos on (hitters.id = "
                   "hitter_pos.hitter_id)inner join positions on (hitter_pos.pos_id = positions.id)GROUP BY 1, 2, 3, "
                   "4, 6, 7, 8, 9, 10 ORDER BY 1;")
    rows = cursor.fetchall();
    return rows

def query_catchers():
    cursor = connect();
    cursor.execute("select hitters.id - 763 as rank, hitters.first_name, hitters.last_name, teams.abbr, string_agg("
                   "positions.position, ',') as pos, hitter_proj.avg, hitter_proj.r, hitter_proj.rbi, hitter_proj.hr, "
                   "hitter_proj.sb from hitters INNER JOIN hitter_proj ON (hitters.id = hitter_proj.id)inner join "
                   "teams on (hitters.team_id = teams.id)inner join hitter_pos on (hitters.id = "
                   "hitter_pos.hitter_id)inner join positions on (hitter_pos.pos_id = positions.id) WHERE position = "
                   "'C'GROUP BY 1, 2, 3, 4, 6, 7, 8, 9, 10 ORDER BY 1;")
    rows = cursor.fetchall();
    return rows


def generate_hitters_query(checked):
    category_str = ""
    for i in checked:
        category_str = category_str + ", hitter_proj." + i
    return category_str


def post_query(checked):
    query = "select hitters.id - 763 as rank, hitters.first_name, hitters.last_name, teams.abbr, string_agg(positions.position, ',') as pos"
    query = query + generate_hitters_query(checked)
    query = query + " from hitters INNER JOIN hitter_proj ON (hitters.id = hitter_proj.id)inner join teams on (hitters.team_id = teams.id)inner join hitter_pos on (hitters.id = hitter_pos.hitter_id)inner join positions on (hitter_pos.pos_id = positions.id)GROUP BY 1, 2, 3, 4, 6, 7, 8, 9, 10 ORDER BY 1;"
    return query


def generate_post_table(query):
    cursor = connect()
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows


def get_table_header(query):
    cursor = connect()
    cursor.execute(query)
    names = [description[0] for description in cursor.description]
    return names


if __name__ == '__main__':
    app.run()
