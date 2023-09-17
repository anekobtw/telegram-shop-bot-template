import sqlite3

con = sqlite3.connect("database.db")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS reviews(nickname text,\
                                                review text)")


def insert(nickname: str, review: str == None) -> None:
    if review is None:
        review = 'Отзыв отсутствует.'

    if not review_exists(nickname):
        cur.execute("INSERT INTO reviews(nickname, review) VALUES (?, ?)", (nickname, review))
    else:
        cur.execute('UPDATE reviews SET review = ? WHERE nickname = ?', [review, nickname])
    con.commit()  

def review_exists(nickname: str) -> bool:
    res = cur.execute("SELECT review FROM reviews WHERE nickname = ?", [nickname])
    return res.fetchone() is not None

def get_all_reviews() -> str:
    res = cur.execute("SELECT * FROM reviews")
    return ''.join(f'{review[0]}:\n{review[1]}\n\n' for review in res.fetchall())
