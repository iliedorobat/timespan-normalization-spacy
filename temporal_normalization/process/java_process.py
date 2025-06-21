import os
import re
import shutil
import subprocess

from py4j.java_gateway import JavaGateway
from py4j.protocol import Py4JNetworkError

from temporal_normalization.commons.print_utils import console
from temporal_normalization.commons.temporal_models import TemporalExpression


def start_process(text: str, expressions: list[TemporalExpression]):
    """
    Launches the Java-based temporal normalization process and populates a list
    of temporal expressions extracted from the input text.

    This function starts a Java subprocess that hosts the temporal-normalization
    server via Py4J. Once the gateway is connected, it sends the input text for
    processing, retrieves the temporal expressions, and then shuts down both
    the Python and Java sides of the connection.

    Args:
        text (str): The input text to be analyzed for temporal expressions.
        expressions (list[TemporalExpression]): A list to be populated with
            extracted temporal expressions.

    Example:
        >>> expressions: list[TemporalExpression] = []
        >>> start_process("Sec al II-lea a.ch. a fost o perioadă de mari schimbări.", expressions)
        >>> # ... use the list of normalized temporal expressions.

    Note:
        Requires `temporal-normalization-2.0.jar` to be present in the `libs` directory.
        Also requires Java 11 or higher to be installed and accessible in the system PATH.
    """

    check_java_version()

    jar_path = os.path.join(
        os.path.dirname(__file__), "../libs/temporal-normalization-2.0.jar"
    )

    java_process = subprocess.Popen(
        ["java", "-jar", jar_path, "--python"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    for line in java_process.stdout:
        if "Gateway Server Started..." in line:
            print(line.strip())
            break

    gateway = gateway_conn(text, expressions)

    try:
        # Proper way to shut down Py4J
        gateway.shutdown()
        print("Python connection closed.")
    except Py4JNetworkError:
        print("Java process already shut down.")

    # Terminate Java process
    java_process.terminate()
    print("Java server is shutting down...")


def gateway_conn(text: str, expressions: list[TemporalExpression]) -> JavaGateway:
    """
    Establishes a connection to the Java Py4J gateway and initializes the
    temporal expression extraction.

    It creates an instance of the Java class ``TimeExpression``, wraps it in
    a Python ``TemporalExpression``, and appends it to the given list if valid.

    Args:
        text (str): The input text to analyze.
        expressions (list[TemporalExpression]): A list to store extracted expressions.

    Returns:
        JavaGateway: The Py4J JavaGateway object used to manage the connection.

    Example:
        >>> from py4j.java_gateway import JavaGateway
        >>> expressions: list[TemporalExpression] = []
        >>> gateway = gateway_conn("Sec al II-lea a.ch. a fost o perioadă de mari schimbări.", expressions)
        >>> # ... use the list of normalized temporal expressions.
        >>> gateway.shutdown()

    Note:
        Assumes that a Py4J-compatible Java process is already running and exposing
        the `ro.webdata.normalization.timespan.ro.TimeExpression` class.
    """

    gateway = JavaGateway()
    print("Python connection established.")

    java_object = gateway.jvm.ro.webdata.normalization.timespan.ro.TimeExpression(text)
    time_expression = TemporalExpression(java_object)

    if time_expression.is_valid:
        expressions.append(time_expression)

    return gateway


def check_java_version():
    """
    Verifies that Java is installed and meets the minimum required version.

    This function checks for the presence of the Java executable in the system PATH,
    runs ``java -version``, and ensures that the version is at least 11. If Java is not
    installed or the version is too low, it logs an error using ``console.error``.

    Raises:
        Logs error messages, but does not raise exceptions directly.
    """

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
