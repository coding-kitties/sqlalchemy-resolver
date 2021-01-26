from tests.resources import FlaskSQLiteTestBase, flask_sql_lite_db
from sqlalchemy import Column, Integer


class TestModel(flask_sql_lite_db.Model):
    table_name = 'members'
    id = Column(Integer, primary_key=True, autoincrement=True)


class TestPagination(FlaskSQLiteTestBase):

    def setUp(self) -> None:
        super(TestPagination, self).setUp()

        for i in range(0, 1000):
            model = TestModel()
            model.save()

        flask_sql_lite_db.session.commit()

    def test_pagination(self):
        self.assertEqual(1000, TestModel.query.count())
        paginated_query = TestModel.query.paginate()

        self.assertEqual(1, paginated_query.page)
        self.assertEqual(1000, paginated_query.total)
        self.assertEqual(20, paginated_query.per_page)
        self.assertEqual(20, len(paginated_query.items))

        paginated_query = TestModel.query.paginate(page=2)

        self.assertEqual(2, paginated_query.page)
        self.assertEqual(1000, paginated_query.total)
        self.assertEqual(20, paginated_query.per_page)
        self.assertEqual(20, len(paginated_query.items))

        paginated_query = TestModel.query.paginate(page=4)

        self.assertEqual(4, paginated_query.page)
        self.assertEqual(1000, paginated_query.total)
        self.assertEqual(20, paginated_query.per_page)
        self.assertEqual(20, len(paginated_query.items))

        paginated_query = TestModel.query.paginate(page=50)

        self.assertEqual(50, paginated_query.page)
        self.assertEqual(1000, paginated_query.total)
        self.assertEqual(20, paginated_query.per_page)
        self.assertEqual(20, len(paginated_query.items))

        paginated_query = TestModel.query.paginate(page=51)

        self.assertEqual(51, paginated_query.page)
        self.assertEqual(1000, paginated_query.total)
        self.assertEqual(20, paginated_query.per_page)
        self.assertEqual(0, len(paginated_query.items))

        paginated_query = TestModel.query.paginate(page=-1)

        self.assertEqual(1, paginated_query.page)
        self.assertEqual(1000, paginated_query.total)
        self.assertEqual(20, paginated_query.per_page)
        self.assertEqual(20, len(paginated_query.items))
