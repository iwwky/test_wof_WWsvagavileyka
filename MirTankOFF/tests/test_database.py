import os
import tempfile
import unittest

from data.database import Database


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_results.db")

        import data.database as database_module
        self.original_name = database_module.DATABASE_NAME
        database_module.DATABASE_NAME = self.db_path
        self.db = Database()

    def tearDown(self):
        self.db.close()
        import data.database as database_module
        database_module.DATABASE_NAME = self.original_name
        self.temp_dir.cleanup()

    def test_add_and_get_statistics(self):
        self.db.add_result("СРЕДНЯЯ", 1000, 5, 3, 0, False, 120.5)
        self.db.add_result("СРЕДНЯЯ", 2000, 10, 5, 1, True, 300.0)

        stats = self.db.get_statistics()
        self.assertEqual(stats["games"], 2)
        self.assertEqual(stats["wins"], 1)
        self.assertEqual(stats["losses"], 1)
        self.assertEqual(stats["best_score"], 2000)
        self.assertEqual(stats["coins"], 15)
        self.assertEqual(stats["enemies"], 8)
        self.assertEqual(stats["bosses"], 1)

    def test_filter_by_difficulty(self):
        self.db.add_result("ЛЕГКАЯ", 500, 1, 1, 0, True, 60.0)
        self.db.add_result("СЛОЖНАЯ", 1500, 2, 2, 0, False, 90.0)

        easy_stats = self.db.get_statistics("ЛЕГКАЯ")
        self.assertEqual(easy_stats["games"], 1)
        self.assertEqual(easy_stats["best_score"], 500)

        all_stats = self.db.get_statistics("ВСЕ")
        self.assertEqual(all_stats["games"], 2)

    def test_score_history(self):
        self.db.add_result("СРЕДНЯЯ", 100, 0, 0, 0, False, 10.0)
        self.db.add_result("СРЕДНЯЯ", 300, 0, 0, 0, True, 20.0)

        history = self.db.get_score_history(limit=5)
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0][0], 100)
        self.assertEqual(history[1][0], 300)


if __name__ == "__main__":
    unittest.main()
