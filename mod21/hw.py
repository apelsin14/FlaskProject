import csv
from datetime import datetime, timedelta

from flask import session, request, jsonify, Flask
from sqlalchemy import Column, Integer, String, Date, Boolean, Float, DateTime, \
    create_engine, ForeignKey, func, extract
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql.elements import or_

Base = declarative_base()
engine = create_engine('sqlite:///sqlite.db')
Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    author = relationship("Author", backref="books")
    students = relationship("ReceivingBooks", backref="book")
    associated_students = association_proxy("students", "student")


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, nullable=True, unique=False)
    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)


class ReceivingBooks(Base):
    __tablename__ = 'receiv_books'

    id = Column(Integer, primary_key=True, nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    date_issue = Column(DateTime, nullable=False)
    date_returned = Column(DateTime)
    book = relationship("Book", backref="receiv_books",
                        cascade="all, delete")
    student = relationship("Student", backref="receiv_books",
                           cascade="all, delete")

    @hybrid_property
    def count_date_with_book(self):
        if self.date_of_return:
            days = (datetime.now() - self.date_returned).days
            return days
        else:
            days = (datetime.now() - self.date_issue).days
            return days


class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)
    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)
    phone = Column(String(255), nullable=False, unique=True)
    books = relationship("ReceivingBooks", backref="student")
    associated_books = association_proxy("books", "book")

    @classmethod
    def get_students_in_dorm(cls):
        return cls.query.filter_by(scholarship=True).all()

    @classmethod
    def higher_average_score(cls, score):
        return cls.query.filter(cls.average_score > score).all()


@app.route('/book', methods=['GET'])
def get_books():
    books = session.query(Book).all()
    books = [book.serialize() for book in books]
    return jsonify(books)


@app.route('/overdue', methods=['GET'])
def get_overdue_students():
    due_date = datetime.now() - timedelta(days=14)
    overdue_books = session.query(ReceivingBooks).filter(
        ReceivingBooks.date_returned.is_(None),
        ReceivingBooks.date_issue < due_date
    ).all()
    students = []
    for book in overdue_books:
        student = session.query(Student).get(book.student_id)
        students.append({'student_id': student.id, 'name': student.name,
                         'surname': student.surname, 'book_id': book.book_id,
                         'date_issue': book.date_issue})

    return jsonify({'overdue_students': students})


@app.route('/issue_books', methods=['POST'])
def issue_book():
    book_id = request.json.get('book_id')
    student_id = request.json.get('student_id')
    book = session.query(Book).get(book_id)
    student = session.query(Student).get(student_id)
    if book is None or student is None:
        return 404

    receiv_book = ReceivingBooks(book_id=book_id, student_id=student_id,
                                 date_of_issue=datetime.now())
    session.add(receiv_book)
    session.commit()
    book.count -= 1
    session.commit()
    return jsonify({'message': 'Книга успешно издана'}), 200


@app.route('/return_book', methods=['POST'])
def return_book():
    book_id = request.json.get('book_id')
    student_id = request.json.get('student_id')
    receiving_book = session.query(ReceivingBooks).filter_by(book_id=book_id,
                                                             student_id=student_id,
                                                             date_of_return=None).first()
    if receiving_book is None:
        return jsonify({'err': 'Книга не найдена или уже возвращена'}), 404

    receiving_book.date_of_return = datetime.now()
    session.commit()
    book = session.query(Book).get(book_id)
    book.count += 1
    session.commit()
    return jsonify({'message': 'Книга успешно возвращена'}), 200


@app.route('/search', methods=['GET'])
def search_books():
    books = session.query(Book).filter(
        or_(Book.name.ilike(f"%{request.args.get('query')}%"))).all()
    book_list = []
    for book in books:
        book_list.append({'id': book.id, 'name': book.name})
    return jsonify(book_list)


@app.route('/books/count/<int:author_id>', methods=['GET'])
def get_books_count_by_author(author_id):
    author = session.query(Author).get(author_id)
    if author is None:
        return jsonify({'error': 'Автор не найден'}), 404

    book_count = session.query(func.sum(Book.count)).filter(
        Book.author_id == author_id).scalar()
    if book_count is None:
        book_count = 0

    return jsonify({'author_id': author_id, 'author_name': author.name,
                    'book_count': book_count})


@app.route('/books/unread/<int:student_id>', methods=['GET'])
def get_unread_books_by_student(student_id):
    student = session.query(Student).get(student_id)
    if student is None:
        return jsonify({'error': 'Студент не найден'}), 404

    student_books = student.associated_books
    author_ids = set(book.author_id for book in student_books)

    unread_books = session.query(Book).filter(
        Book.author_id.in_(author_ids),
        ~Book.id.in_([book.id for book in student_books])
    ).all()

    unread_books_data = [{'id': book.id, 'name': book.name} for book in
                         unread_books]

    return jsonify(
        {'student_id': student_id, 'unread_books': unread_books_data})


@app.route('/books/avg_count', methods=['GET'])
def get_average_books_count():
    current_month = datetime.now().month
    current_year = datetime.now().year

    average_count = session.query(func.avg(ReceivingBooks.book_id)).filter(
        extract('month', ReceivingBooks.date_issue) == current_month,
        extract('year', ReceivingBooks.date_issue) == current_year
    ).scalar()

    if average_count is None:
        average_count = 0

    return jsonify({'average_count': average_count})


@app.route('/books/popular', methods=['GET'])
def get_popular_book():
    students = session.query(Student).filter(Student.average_score > 4.0).all()

    book_counts = {}
    for student in students:
        for book in student.associated_books:
            if book.id in book_counts:
                book_counts[book.id] += 1
            else:
                book_counts[book.id] = 1

    if not book_counts:
        return jsonify({
                           'error': 'Среди студентов с средним баллом больше 4.0 нет популярных книг'}), 404

    popular_book_id = max(book_counts, key=book_counts.get)
    popular_book = session.query(Book).get(popular_book_id)

    return jsonify({'popular_book': popular_book.serialize()})


@app.route('/students/top', methods=['GET'])
def get_top_students():
    current_year = datetime.now().year

    top_students = session.query(Student).join(ReceivingBooks).filter(
        extract('year', ReceivingBooks.date_issue) == current_year
    ).group_by(Student.id).order_by(func.count(ReceivingBooks.id).desc()).limit(10).all()

    top_students_data = [{'student_id': student.id, 'name': student.name, 'surname': student.surname} for student in top_students]

    return jsonify({'top_students': top_students_data})


@app.route('/upload', methods=['POST'])
def upload_students():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'Файл не найден'}), 400

    students = []
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        student_data = {'email': row.get('email'), 'average_score': float(row.get('average_score')),
            'scholarship': bool(row.get('scholarship')), 'name': row.get('name'), 'surname': row.get('surname'),
            'phone': row.get('phone')}

        students.append(student_data)

    session.bulk_insert_mappings(Student, students)
    session.commit()

    return jsonify({'message': 'Студенты успешно добавлены'}), 200


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    app.run(debug=True)
