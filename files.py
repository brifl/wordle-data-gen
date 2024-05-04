def from_input(file_name: str) -> str:
    with open(f"input/{file_name}", "r") as file:
        return file.read()


def to_output(file_name: str, data: str) -> None:
    with open(f"output/{file_name}", "w") as file:
        file.write(data)
