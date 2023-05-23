from datetime import datetime, timedelta

from flask import session, request, jsonify, Flask
from sqlalchemy import Column, Integer, String, Date, Boolean, Float, DateTime, \
    create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.elements import or_

Base = declarative_base()
engine = create_engine('sqlite:///sqlite.db')
Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)


class Book(Base):
    __tablename__ = 'books'

    id = Column(
        Integer,
        primary_key=True,
        nullable=False
    )
    name = Column(String(255), nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, nullable=False)


class Author(Base):
    __tablename__ = 'authors'

    id = Column(
        Integer,
        primary_key=True,
        nullable=True,
        unique=False)
    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)


class ReceivingBooks(Base):
    __tablename__ = 'receiv_books'

    id = Column(
        Integer,
        primary_key=True,
        nullable=False
    )
    book_id = Column(Integer, nullable=False)
    student_id = Column(Integer, nullable=False)
    date_issue = Column(DateTime, nullable=False)
    date_returned = Column(DateTime)

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
            'surname': student.surname, 'book_id': book.book_id, 'date_issue': book.date_issue})

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
        student_id=student_id,date_of_return=None).first()
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


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    app.run(debug=True)
