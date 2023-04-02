from auto_everything.python import Python
python = Python()

def test_documentation_generation():
    python.generate_documentation_for_a_python_project(
        python_project_folder_path="/Users/yingshaoxo/CS/auto_everything/auto_everything",
        markdown_file_output_folder_path="/Users/yingshaoxo/CS/auto_everything/test_docs",
        only_generate_those_functions_that_has_docstring=False
    )