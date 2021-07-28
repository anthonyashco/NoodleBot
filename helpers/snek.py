import re


def snekkify(message: str) -> str:
    messsage = re.sub(r"(ss|s)", "sss", str(message))
    return re.sub(r"(Ss|S)", "Sss", messsage)
