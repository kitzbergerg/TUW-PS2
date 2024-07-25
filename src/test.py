from main import run


def run_on_file(file_path):
    print(f"\nRunning {file_path}...")

    # Read the code from a file
    with open(file_path, 'r') as file:
        code = file.read()

    run(code)


if __name__ == '__main__':
    # Positive test runs:
    run_on_file('../test/plus.lang')
    run_on_file('../test/func_no_params.lang')
    run_on_file('../test/returned_func_captures.lang')
    run_on_file('../test/partial_functions.lang')
    run_on_file('../test/recursive_func.lang')
    run_on_file('../test/list_at_index.lang')
    run_on_file('../test/list_reduce.lang')
    run_on_file('../test/list_map.lang')
    run_on_file('../test/print_values.lang')

    # Negative test runs:
    try:
        run_on_file('../test/define_var_after_func_fails.lang')
        assert False
    except Exception as e:
        pass
