from flask import Flask, render_template
import psycopg2

app = Flask(__name__)


@app.route('/')
def hello_world():
    rows = queryHitters()
    return render_template('main.html', rows=rows)


def connect():
    try:
        conn = psycopg2.connect(host="ec2-54-157-78-113.compute-1.amazonaws.com", database="d1oh3vt134d6nv",
                                user="seawikidnnuwrk", port="5432",
                                password="b22cc1de4f913fcf525204dacad4a53f52b1040551e2caa67515d7d3bdf61f20")
    except:
        print("Not working....")

    return conn.cursor()

def queryHitters():
    cursor = connect();
    cursor.execute("select hitters.id - 763 as rank, hitters.first_name, hitters.last_name, teams.abbr, string_agg(positions.position, ',') as pos, hitter_proj.avg, hitter_proj.r, hitter_proj.rbi, hitter_proj.hr, hitter_proj.sb from hitters INNER JOIN hitter_proj ON (hitters.id = hitter_proj.id)inner join teams on (hitters.team_id = teams.id)inner join hitter_pos on (hitters.id = hitter_pos.hitter_id)inner join positions on (hitter_pos.pos_id = positions.id)GROUP BY 1, 2, 3, 4, 6, 7, 8, 9, 10 ORDER BY 1;")
    rows = cursor.fetchall();
    return rows


if __name__ == '__main__':
    app.run()
