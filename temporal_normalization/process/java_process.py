import re
import shutil
import subprocess

from py4j.java_gateway import JavaGateway
from py4j.protocol import Py4JNetworkError

from temporal_normalization.commons.print_utils import console


def start_conn(root_path: str) -> tuple[subprocess.Popen, JavaGateway]:
    """
    Starts the Java temporal normalization process and establishes a Py4J gateway connection.

    Args:
        root_path (str): The root directory of the project.

    Returns:
        tuple[subprocess.Popen, JavaGateway]:
            - The subprocess.Popen object representing the running Java process.
            - The JavaGateway object representing the active Py4J connection.

    Note:
        - Requires Java 11 or higher to be installed and accessible in the system PATH.
        - Requires `temporal-normalization-2.1.0.jar` to be present in the `libs` directory.
        - The caller is responsible for closing the gateway and terminating the Java process
            after usage to avoid orphaned processes.
    """

    check_java_version()

    jar_path = (
        f"{root_path}/temporal_normalization/libs/temporal-normalization-2.1.0.jar"
    )

    java_process = subprocess.Popen(
        ["java", "-jar", jar_path, "--python"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    for line in java_process.stdout:
        if "Gateway Server Started." in line:
            print(line.strip())
            break

    gateway = JavaGateway()
    print("Python connection established.")

    return java_process, gateway


def close_conn(java_process: subprocess.Popen, gateway: JavaGateway) -> None:
    """
    Closes the active connection between Python and the Java process started via Py4J.

    This function ensures a proper shutdown sequence:
    1. Attempts to gracefully shut down the Py4J gateway connection.
       - If the Java process is already closed, a Py4JNetworkError is caught and logged.
    2. Terminates the underlying Java process.
    3. Prints status messages for debugging/confirmation.

    Args:
        java_process (subprocess.Popen): The Java process launched with subprocess.
        gateway (JavaGateway): The active Py4J gateway connection.

    Notes:
        - Call this function once you have finished all interactions with the Java process.
        - It is safe to call even if the Java process has already exited.
    """

    try:
        # Proper way to shut down Py4J
        gateway.shutdown()
        print("Python connection closed.")
    except Py4JNetworkError:
        print("Java process already shut down.")

    # Terminate Java process
    java_process.terminate()
    print("Java server is shutting down...")


def check_java_version() -> None:
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
