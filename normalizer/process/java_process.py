import subprocess

from py4j.java_gateway import JavaGateway
from py4j.protocol import Py4JNetworkError
from spacy.tokens import Doc

from normalizer.commons.temporal_models import TemporalExpression


def start_process(doc: Doc, expressions: list[TemporalExpression], sub_path: str = ""):
    java_process = subprocess.Popen(
        ["java", "-jar", f"{sub_path}timespan-normalization-1.6.jar"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    for line in java_process.stdout:
        if "Gateway Server Started..." in line:
            print(line.strip())
            break

    gateway = gateway_conn(doc, expressions)

    try:
        # Proper way to shut down Py4J
        gateway.shutdown()
        print("Python connection closed.")
    except Py4JNetworkError:
        print("Java process already shut down.")

    # Terminate Java process
    java_process.terminate()
    print("Java server is shutting down.")


def gateway_conn(doc: Doc, expressions: list[TemporalExpression]) -> JavaGateway:
    """Connect to the running Py4J Gateway"""

    gateway = JavaGateway()
    print("Python connection established.")

    if isinstance(doc, Doc):
        java_object = gateway.jvm.ro.webdata.normalization.timespan.ro.TimeExpression(doc.text, False, "\n")
        time_expression = TemporalExpression(java_object)

        if time_expression.is_valid:
            expressions.append(time_expression)

    return gateway


if __name__ == "__main__":
    pass
