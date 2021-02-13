from unittest import TestCase
import filecmp
from pathlib import Path
from src.exporter import export


class TestExportJupyterNotebook(TestCase):
    def setUp(self) -> None:
        self.notebook_path = "data/input/01-TestNotebook.ipynb"
        self.test_output_path = "data/output/01-TestNotebook-Test.py"
        self.output_path = "data/output/01-TestNotebook.py"

        self.without_export_comments_notebook_path = "data/input/02-TestNotebook.ipynb"
        self.without_export_comments_test_output_path = "data/output/02-TestNotebook-Test.py"
        self.without_export_comments_output_path = "data/output/02-TestNotebook.py"

        self.not_existing_notebook_path = "data/input/NotExisyingNotebook.ipynb"

        self.no_exported_cells_notebook_path = "data/input/03-TestNotebook.ipynb"
        self.no_exported_cells_test_output_path = "data/output/03-TestNotebook-Test.py"

    def test_export_jupyter_notebook(self):
        #  Export Jupyter Notebook
        export(self.notebook_path, self.test_output_path, delete_export_comments=False)
        #  shallow=False to compare contents of files.
        assert filecmp.cmp(self.test_output_path, self.output_path, shallow=False)

    def test_export_jupyter_notebook_with_deleting_export_comments(self):
        # Export Jupyter Notebook
        export(self.without_export_comments_notebook_path, self.without_export_comments_test_output_path,
               delete_export_comments=True)
        assert filecmp.cmp(self.without_export_comments_test_output_path, self.without_export_comments_output_path)

    def test_not_existing_notebook_path_gives_error(self):
        # Should throw an exception
        self.assertRaises(FileNotFoundError, export, self.not_existing_notebook_path, "")

    def test_no_exported_cells(self):
        export(self.no_exported_cells_notebook_path, self.no_exported_cells_test_output_path)
        # No cell exported so test_output_path should be missing
        assert not Path(self.no_exported_cells_test_output_path).exists()
