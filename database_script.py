#tujuan : segala yang berkaitan dengan database 

import sqlite3
db_name = 'quiz.sqlite'
conn = None #Membuat koneksi ke database
cursor = None #Cursor untuk akses database

# Mekanisme Akses Database
## Buka Database
def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

## Tutup Database
def close():
    cursor.close()
    conn.close()

## Jelajah Database
def do(query):
    cursor.execute(query)
    #conn.close()

## Reset Database
def clear_db():
    open()
    query1 = '''DROP TABLE IF EXISTS quiz_content''' #tabel penghubung
    query2 = '''DROP TABLE IF EXISTS questions''' #tabel question
    query3 = '''DROP TABLE IF EXISTS quiz''' #tabel quiz
    do(query1)
    do(query2)
    do(query3)
    close()

## Membuat Tabel
def create():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')
    query_create_quiz_table = '''
        CREATE TABLE IF NOT EXISTS quiz(
            id      INTEGER PRIMARY KEY, 
            name    VARCHAR
        )
    '''
    query_create_questions_table = '''
        CREATE TABLE IF NOT EXISTS questions(
            id          INTEGER PRIMARY KEY, 
            question    VARCHAR,
            answer      VARCHAR,
            wrong_1     VARCHAR,
            wrong_2     VARCHAR, 
            wrong_3     VARCHAR
        )
    '''
    query_create_quiz_content_table = '''
        CREATE TABLE IF NOT EXISTS quiz_content(
            id          INTEGER PRIMARY KEY,
            quiz_id     INTEGER,
            question_id INTEGER, 

            FOREIGN KEY (quiz_id) REFERENCES quiz(id),
            FOREIGN KEY (question_id) REFERENCES questions(id)
        )
    '''

    do(query_create_quiz_table)
    do(query_create_questions_table)
    do(query_create_quiz_content_table)
    close()

## Membuat daftar pertanyaan
def add_questions():
    questions = [
        ("Proses sosial ketika seseorang atau kelompok menyesuaikan diri dengan kebudayaan baru tanpa menghilangkan kebudayaan aslinya disebut...", "Akulturasi","Asimilasi", "Amalgamasi", "Akomodasi"),
        ("Sikap atau pandangan yang menilai kebudayaan lain berdasarkan ukuran dan standar kebudayaannya sendiri disebut...", "Etnosentrisme", "Xenosentrisme", "Relativisme budaya","Chauvinisme"),
        ("Tindakan sosial yang dilakukan berdasarkan nilai-nilai mutlak tanpa memperhitungkan cara untuk mencapainya disebut tindakan...", "Rasional nilai", "Rasional instrumental", "Afektif", "Tradisional"),
        ("Perubahan sosial yang terjadi secara lambat dan memerlukan waktu yang lama serta melalui serangkaian tahapan disebut...", "Evolusi", "Revolusi", "Inovasi", "Modernisasi"),

        ("Lapisan atmosfer yang menjadi tempat terjadinya fenomena cuaca seperti hujan, angin, dan awan adalah...", "Troposfer", "Stratosfer", "Mesosfer", "Termosfer"),
        ("Prinsip geografi yang menjelaskan fenomena geosfer secara runtut dan terpadu dengan menggabungkan prinsip persebaran, interaksi, dan deskripsi disebut...", "Prinsip korologi", "Prinsip deskripsi", "Prinsip interelasi", "Prinsip distribusi"),
        ("Proses pergerakan lempeng tektonik yang saling menjauh satu sama lain disebut pergerakan...", "Divergen", "Konvergen", "Transform", "Subduksi"),
        ("Batuan yang terbentuk dari hasil pendinginan dan pembekuan magma atau lava disebut batuan...", "Beku", "Sedimen", "Metamorf", "Mihanik"),

        ("Ilmu ekonomi yang membahas tentang perilaku unit-unit ekonomi secara keseluruhan (agregat) disebut...", "Ekonomi makro", "Ekonomi mikro", "Ekonomi deskriptif", "Ekonomi terapan"),
        ("Tindakan manusia untuk memenuhi berbagai kebutuhan dengan pengorbanan sekecil-kecilnya untuk mendapatkan hasil tertentu disebut...", "Prinsip ekonomi", "Motif ekonomi", "Politik ekonomi", "Hukum ekonomi"),
        ("Jenis inflasi yang tingkat parahnya berada di kisaran 10% sampai 30% per tahun disebut...", "Inflasi sedang", "Inflasi ringan", "Inflasi berat", "Hiperinflasi"),
        ("Pasar yang di dalamnya hanya terdapat satu penjual yang menguasai pasar untuk melayani banya,k pembeli disebut...", "Monopoli", "Oligopoli", "Monopsoni", "Persaingan sempurna")
    ]

    open()
    cursor.executemany(
        '''
            INSERT INTO questions
            (question, answer, wrong_1, wrong_2, wrong_3)
            VALUES (?, ?, ?, ?, ?)
        ''', questions
    )
    conn.commit()
    close()

## Membuat daftar Type Quiz
def add_quiz():
    quizes = [
        ('Sosiologi',),
        ('Geografi',),
        ('Ekonomi',)
    ]

    open()
    cursor.executemany(
        '''
            INSERT INTO quiz
            (name)
            VALUES (?)
        ''', quizes
    )
    conn.commit()
    close()

## Membuat hubungan antara pertanyaan dan Type Quiz
def add_links():
    link = [
        (1, 1),
        (1, 2),
        (1, 3),
        (1, 4),
        (2, 5),
        (2, 6),
        (2, 7),
        (2, 8),
        (3, 9),
        (3, 10),
        (3, 11),
        (3, 12),
    ]
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')
    cursor.executemany(
        '''
        INSERT INTO quiz_content(quiz_id, question_id) VALUES (?, ?)
        ''', link
    )
    conn.commit ()
    close()
    print('Data seede successfuly')

    #apa yang diperlukan untuk menampilkan pertanyaan berikutnya
    #nomor pertanyaan yang sudah ditanyakan.
    #nomor quiz (quiz id)

def get_question_after(question_id = 0, quiz_id = 1):
    open()
    query = '''
        SELECT 
            quiz_content.id,
            questions.question,
            questions.answer,
            questions.wrong_1,
            questions.wrong_2,
            questions.wrong_3
        FROM 
            questions,
            quiz_content
        WHERE
            quiz_content.question_id == questions.id
            AND quiz_content.id > ?
            AND quiz_content.quiz_id == ?
        ORDER BY
            quiz_content.id
    '''
    cursor.execute(query, [question_id, quiz_id])
    result = cursor.fetchone() #fetchone untuk mengambil 1 data saja (1row)
    close()
    return result 


def get_quiz():
    query = '''
        SELECT * FROM quiz ORDER BY id 
    '''
    open()
    cursor.execute(query)
    result = cursor.fetchall()
    close()
    return result 

def check_answer(q_id, ans_text):
    query = '''
        SELECT questions.answer
        FROM quiz_content, questions
        WHERE quiz_content.id = ?
        AND quiz_content.question_id = questions.id
    '''
    open()
    cursor.execute(query, str(q_id))
    result = cursor.fetchone()
    close()

    if result is None:
        print('false')
        return False
    else:
        if result[0] == ans_text:
            print('t')
            return True # Jawabann benar
        else:
            print('false 2')
            return False # Jawaban salah

## Entry Point untuk menjalankan program
def main():
    clear_db()
    create()
    add_questions()
    add_quiz()
    add_links()
    #def get_question_after(question_id = 0, quiz_id = 1)
    print(get_question_after(3, 2))

if __name__ == "__main__":
    main()