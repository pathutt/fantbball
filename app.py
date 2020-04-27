import sys

from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)


#     cursor.execute("select hitters.id - 763 as rank, hitters.first_name, hitters.last_name, teams.abbr, string_agg(positions.position, ',') as pos, hitter_proj.avg, hitter_proj.r, hitter_proj.rbi, hitter_proj.hr, hitter_proj.sb from hitters INNER JOIN hitter_proj ON (hitters.id = hitter_proj.id)inner join teams on (hitters.team_id = teams.id)inner join hitter_pos on (hitters.id = hitter_pos.hitter_id)inner join positions on (hitter_pos.pos_id = positions.id)GROUP BY 1, 2, 3, 4, 6, 7, 8, 9, 10 ORDER BY 1;")

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'GET':
        hitter_categories = ['avg', 'r', 'rbi', 'hr', 'sb']
        hitter_query = create_hitters_query(hitter_categories)
        hitter_rows = generate_post_table(hitter_query)
        num_hitter_cols = len(hitter_rows[0])
        hitter_col_names = get_table_header(hitter_query)

        pitcher_categories = ['k', 'w', 'sv', 'era', 'whip']
        pitcher_query = create_pitchers_query(pitcher_categories)
        pitcher_rows = generate_post_table(pitcher_query)
        num_pitcher_cols = len(pitcher_rows[0])
        pitcher_col_names = get_table_header(pitcher_query)
        return render_template('main.html', hitter_rows=hitter_rows, hitter_cols=hitter_col_names,
                               num_hitter_cols=num_hitter_cols, pitcher_rows=pitcher_rows,
                               pitcher_cols=pitcher_col_names, num_pitcher_cols=num_pitcher_cols)

    if request.method == 'POST':
        categories = request.form.getlist('hitter')
        query = create_hitters_query(categories)
        rows = generate_post_table(query)
        num_cols = len(rows[0])
        names = get_table_header(query)
        return render_template('main.html', rows=rows, cols=names, length=num_cols)


# Connect to db
def connect():
    try:
        conn = psycopg2.connect(host="ec2-54-157-78-113.compute-1.amazonaws.com", database="d1oh3vt134d6nv",
                                user="seawikidnnuwrk", port="5432",
                                password="b22cc1de4f913fcf525204dacad4a53f52b1040551e2caa67515d7d3bdf61f20")
    except:
        print("Not working....")

    return conn.cursor()


# Generates categories selected in query based on checkboxes. Used to create the hitter query
def generate_hitters_columns(checked):
    category_str = ""
    for i in checked:
        category_str = category_str + ", hitter_proj." + i
    return category_str


# Creates query based on selected hitter categories
def create_hitters_query(checked):
    query = "select hitters.id - 763 as rank, hitters.first_name as first, hitters.last_name as last, teams.abbr as " \
            "team, string_agg(positions.position, ',') as pos" + generate_hitters_columns(checked) + \
            " from hitters INNER JOIN " \
            "hitter_proj ON (hitters.id = " \
            "hitter_proj.id)inner join teams on " \
            "(hitters.team_id = teams.id)inner " \
            "join hitter_pos on (hitters.id = " \
            "hitter_pos.hitter_id)inner join " \
            "positions on (hitter_pos.pos_id = " \
            "positions.id)GROUP BY 1, 2, 3, 4, " \
            "6, 7, 8, 9, 10 ORDER BY 1; "
    return query


# Creates cursor based on query
def create_cursor(query):
    cursor = connect()
    cursor.execute(query)
    return cursor


# Retrieves all rows based on query
def generate_post_table(query):
    cursor = create_cursor(query)
    rows = cursor.fetchall()
    return rows


# Retrieves table head names based on query
def get_table_header(query):
    cursor = create_cursor(query)
    names = [description[0] for description in cursor.description]
    return names


# Generates categories selected in query based on checkboxes. Used to create the hitter query
def generate_pitchers_columns(checked):
    category_str = ""
    for i in checked:
        category_str = category_str + ", pitcher_proj." + i
    return category_str


# Creates query based on selected hitter categories
def create_pitchers_query(checked):
    query = "select pitchers.id as rank, pitchers.first_name as first, pitchers.last_name as last, teams.abbr as " \
            "team, string_agg(positions.position, ',') as pos" + generate_pitchers_columns(checked) + \
            " from pitchers INNER JOIN " \
            "pitcher_proj ON (pitchers.id = " \
            "pitcher_proj.pitcher_id)inner join " \
            "teams on " \
            "(pitchers.team_id = teams.id)inner " \
            "join pitcher_pos on (pitchers.id = " \
            "pitcher_pos.pitcher_id)inner join " \
            "positions on (pitcher_pos.pos_id = " \
            "positions.id)GROUP BY 1, 2, 3, 4, " \
            "6, 7, 8, 9, 10 ORDER BY 1; "
    return query


if __name__ == '__main__':
    app.run()
