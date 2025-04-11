import re
import shutil
import subprocess

from py4j.java_gateway import JavaGateway
from py4j.protocol import Py4JNetworkError
from spacy.tokens import Doc

from temporal_normalization.commons.print_utils import console
from temporal_normalization.commons.temporal_models import TemporalExpression


def start_process(doc: Doc, expressions: list[TemporalExpression], jar_path):
    check_java_version()

    java_process = subprocess.Popen(
        ["java", "-jar", jar_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
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
    print("Java server is shutting down...")


def gateway_conn(doc: Doc, expressions: list[TemporalExpression]) -> JavaGateway:
    """Connect to the running Py4J Gateway"""

    gateway = JavaGateway()
    print("Python connection established.")

    if isinstance(doc, Doc):
        java_object = gateway.jvm.ro.webdata.normalization.timespan.ro.TimeExpression(
            doc.text, False, "\n"
        )
        time_expression = TemporalExpression(java_object)

        if time_expression.is_valid:
            expressions.append(time_expression)

    return gateway


def check_java_version():
    min_version = 11
    java_path = shutil.which("java")

    try:
        if java_path:
            # Run the command to check the Java version
            result = subprocess.run(
                [java_path, "-version"], capture_output=True, text=True
            )

            # Print the version information (Java version is printed to stderr)
            if result.returncode == 0:
                version_output = result.stderr
                match = re.search(r'version "(\d+\.\d+)', version_output)

                if match:
                    crr_version = float(match.group(1))
                    if crr_version < min_version:
                        console.error(
                            f"Java {crr_version} is installed, but version {min_version} is required."  # noqa 501
                        )
                else:
                    console.error("Could not extract Java version.")
            else:
                console.error("Error occurred while checking the version.")
        else:
            console.error("Java not found.")
    except Exception as e:
        console.error(e.__str__())


if __name__ == "__main__":
    pass
