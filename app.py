import sys

from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'GET':
        # Uses default list of rows to generate columns for select query
        hitter_categories = ['avg', 'r', 'rbi', 'hr', 'sb']
        # Uses the list of categories and table name to generate the hitter select query
        hitter_query = create_table_query(hitter_categories, "hitter")
        # Runs the select query
        hitter_rows = generate_table(hitter_query)
        # Gets the total number of projection columns
        num_hitter_cols = len(hitter_rows[0])
        # Uses the query to create the html tables thead
        hitter_col_names = get_table_header(hitter_query)

        # Same as with the hitter table but with pitcher categories and table instead
        pitcher_categories = ['k', 'w', 'sv', 'era', 'whip']
        pitcher_query = create_table_query(pitcher_categories, "pitcher")
        pitcher_rows = generate_table(pitcher_query)
        num_pitcher_cols = len(pitcher_rows[0])
        pitcher_col_names = get_table_header(pitcher_query)
        return render_template('main.html', hitter_rows=hitter_rows, hitter_cols=hitter_col_names,
                               num_hitter_cols=num_hitter_cols, pitcher_rows=pitcher_rows,
                               pitcher_cols=pitcher_col_names, num_pitcher_cols=num_pitcher_cols)

    if request.method == 'POST':
        # Column names are generated using the list returned by the form. Based on the categories checked by the user
        hitter_categories = request.form.getlist('hitter')
        hitter_query = create_table_query(hitter_categories, "hitter")
        hitter_rows = generate_table(hitter_query)
        num_hitter_cols = len(hitter_rows[0])
        hitter_col_names = get_table_header(hitter_query)

        pitcher_categories = request.form.getlist('pitcher')
        pitcher_query = create_table_query(pitcher_categories, "pitcher")
        pitcher_rows = generate_table(pitcher_query)
        num_pitcher_cols = len(pitcher_rows[0])
        pitcher_col_names = get_table_header(pitcher_query)
        return render_template('main.html', hitter_rows=hitter_rows, hitter_cols=hitter_col_names,
                               num_hitter_cols=num_hitter_cols, pitcher_rows=pitcher_rows,
                               pitcher_cols=pitcher_col_names, num_pitcher_cols=num_pitcher_cols)


# Connects to the db and returns a cursor to perform queries
def connect():
    try:
        conn = psycopg2.connect(host="ec2-54-157-78-113.compute-1.amazonaws.com", database="d1oh3vt134d6nv",
                                user="seawikidnnuwrk", port="5432",
                                password="b22cc1de4f913fcf525204dacad4a53f52b1040551e2caa67515d7d3bdf61f20")
    except:
        print("Not working....")

    return conn.cursor()


# Generates categories selected in query based on a list
def generate_table_columns(checked, table):
    category_str = ""
    for i in checked:
        category_str = category_str + ", " + table + "_proj." + i
    return category_str


# Creates select query used to create the html table. Uses a list and the name of the table
def create_table_query(checked, table):
    query = create_with(checked, table) + \
            "select DENSE_RANK() OVER(order by ranks.rank asc) as rank, " + table + ".first_name as first, " \
            + table + ".last_name as last, teams.abbr as " \
            "team, string_agg(positions.position, ',') as pos" + generate_table_columns(checked, table) + \
            " from " + table + " INNER JOIN " \
            + table + "_proj ON (" + table + ".id = " \
            + table + "_proj." + table + "_id) inner join teams on (" \
            + table + ".team_id = teams.id) inner " \
            "join " + table + "_pos on (" + table + ".id = " \
            + table + "_pos." + table + "_id) inner join " \
            "positions on (" + table + "_pos.pos_id = " \
            "positions.id) inner join ranks on (" + table + ".id = ranks.id)" \
            " GROUP BY ranks.rank, 2, 3, 4" + \
            generate_group_by(checked) + " ORDER BY 1; "
    print(query)
    return query


# Creates the with statement that ranks the players. Uses the category list and name of the targeted table
def create_with(checked, table):
    with_query = "WITH ranks AS (SELECT " + table + ".id, 0" + generate_dense_rank(checked, table) + " as rank "\
                 "from " + table + " inner join " + table + "_proj on (" + table + ".id = " + \
                 table + "_proj." + table + "_id))"
    return with_query


# Creates the dense_rank part of the with statement. Uses the category list and name of targeted table.
def generate_dense_rank(checked, table):
    dense_rank = ""
    for i in checked:
        if i.lower() in ['era', 'whip', 'er', 'hits', 'bb', 'hrs', 'l', "strikeouts"]:
            dense_rank = dense_rank + " + DENSE_RANK() OVER(ORDER BY " + table + "_proj." + i + " asc)"
        else:
            dense_rank = dense_rank + " + DENSE_RANK() OVER(ORDER BY " + table + "_proj." + i + " desc)"
    return dense_rank


# Creates cursor based on query
def create_cursor(query):
    cursor = connect()
    cursor.execute(query)
    return cursor


# Retrieves all rows based on the select query
def generate_table(query):
    cursor = create_cursor(query)
    rows = cursor.fetchall()
    return rows


# Retrieves table head names based on query column names
def get_table_header(query):
    cursor = create_cursor(query)
    names = [description[0] for description in cursor.description]
    return names


# Creates the group by clause based on the number of categories selected by the user
def generate_group_by(checked):
    num_categories = len(checked)
    group_by_str = ""
    for x in range(num_categories):
        group_by_str = group_by_str + ", " + str(x + 6)
    return group_by_str


if __name__ == '__main__':
    app.run()
