from unittest import TestCase
from exporter.exporter import export
import filecmp


class TestExportJupyterNotebook(TestCase):
    def setUp(self) -> None:
        self.notebook_path = "data/input/01-TestNotebook.ipynb"
        self.test_output_path = "data/output/01-TestNotebook-Test.py"
        self.output_path = "data/output/01-TestNotebook.py"

        self.without_export_comments_notebook_path = "data/input/02-TestNotebook.ipynb"
        self.without_export_comments_test_output_path = "data/output/02-TestNotebook-Test.py"
        self.without_export_comments_output_path = "data/output/02-TestNotebook.py"

    def test_export_jupyter_notebook(self):
        #  Export Jupyter Notebook
        export(self.notebook_path, self.test_output_path, delete_export_comments=False)
        #  shallow=False to compare contents of files.
        assert filecmp.cmp(self.test_output_path, self.output_path, shallow=False)

    def test_export_jupyter_notebook_without_export_comments(self):
        # Export Jupyter Notebook
        export(self.without_export_comments_notebook_path, self.without_export_comments_test_output_path,
               delete_export_comments=True)
        assert filecmp.cmp(self.without_export_comments_test_output_path, self.without_export_comments_output_path)

    def test_not_existing_notebook_path_gives_error(self):
        pass
