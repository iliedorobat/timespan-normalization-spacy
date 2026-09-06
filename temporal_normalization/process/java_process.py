import io
import re
import shutil
import subprocess
import threading
import time

from py4j.java_gateway import JavaGateway, GatewayParameters
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
        - Requires `temporal-normalization-2.2.0.jar` to be present in the `libs` directory.
        - The caller is responsible for closing the gateway and terminating the Java process
            after usage to avoid orphaned processes.
    """

    check_java_version()

    gateway_started = threading.Event()
    gateway_error = threading.Event()

    jar_path = (
        f"{root_path}/temporal_normalization/libs/temporal-normalization-2.2.0.jar"
    )

    def stdout_callback(line: str):
        if "Gateway Server Started" in line:
            gateway_started.set()
        print(line.strip())

    stderr_lines = []
    def stderr_callback(line: str):
        stderr_lines.append(line)

        if "Failed to bind" in line or "Address already in use" in line:
            gateway_error.set()

    java_process = subprocess.Popen(
        ["java", "-jar", jar_path, "--python"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    threading.Thread(target=drain_stream, args=(java_process.stdout, stdout_callback), daemon=True).start()
    threading.Thread(target=drain_stream, args=(java_process.stderr, stderr_callback), daemon=True).start()

    timeout = 10.0
    start_time = time.monotonic()

    while not gateway_started.is_set():
        if gateway_error.wait(timeout=0.1):
            error = "\n\t".join(stderr_lines)

            if java_process.poll() is None:
                java_process.terminate()

            raise RuntimeError(
                "Java Gateway failed to start.\n"
                f"Java stderr:\n\t{error}"
            )

        if time.monotonic() - start_time >= timeout:
            error = "\n\t".join(stderr_lines)

            java_process.terminate()
            java_process.wait()

            raise RuntimeError(
                f"Java Gateway did not start within 10 seconds.\n"
                f"Java stderr:\n\t{error}"
            )

        time.sleep(0.1)

    gateway = JavaGateway(
        gateway_parameters=GatewayParameters(auto_convert=True, read_timeout=None),
        callback_server_parameters=None,
    )

    print("Python connection established.")

    return java_process, gateway


def close_conn(java_process: subprocess.Popen | None, gateway: JavaGateway | None) -> None:
    """
    Closes the Py4J gateway connection and terminates the associated Java process.

    This function performs the shutdown sequence by:
    1. Attempting to gracefully close the Py4J gateway connection.
       - If the Java process has already terminated, the resulting
         Py4JNetworkError is handled without raising an exception.
    2. Terminating the Java process if it is still running.
    3. Reporting the shutdown status for each resource.

    Args:
        java_process (subprocess.Popen | None): The Java process launched
            with subprocess, or None if the process was not successfully
            initialized.
        gateway (JavaGateway | None): The active Py4J gateway connection,
            or None if the gateway was not successfully initialized.

    Notes:
        - Call this function once all interactions with the Java process
          have been completed.
        - It is safe to call even if either the gateway or Java process
          has already been closed or was not successfully initialized.
        - The Py4J gateway is closed before the Java process is terminated.
    """

    _close_gateway_conn(gateway)
    _close_java_conn(java_process)


def _close_gateway_conn(gateway: JavaGateway | None) -> None:
    """
    Closes the active Py4J gateway connection, if one exists.

    Attempts to gracefully shut down the connection between Python and
    the Java process. If the Java process has already terminated, the
    resulting Py4JNetworkError is handled and reported without raising
    an exception.

    Args:
        gateway (JavaGateway | None): The active Py4J gateway connection,
            or None if the connection was not successfully initialized.

    Notes:
        - It is safe to call this function when the gateway is None.
        - It is safe to call this function after the Java process has
          already terminated.
        - Unexpected errors during gateway shutdown are caught and
          reported rather than propagated.
    """

    if gateway is not None:
        try:
            # Proper way to shut down Py4J
            gateway.shutdown()
            print("✅ Python connection closed.")
        except Py4JNetworkError:
            print("⚠️ Java process already shut down.")
        except Exception as e:
            print(f"⚠️ Error shutting down gateway: {e}")
    else:
        print(f"⚠️ No Python connection to close.")


def _close_java_conn(java_process: subprocess.Popen | None) -> None:
    """
    Terminates the Java process, if it is still running.

    Checks whether the Java process is active before attempting to
    terminate it. If the process has already exited, no termination
    is attempted and a status message is printed.

    Args:
        java_process (subprocess.Popen | None): The Java process started
            with subprocess, or None if the process was not successfully
            initialized.

    Notes:
        - It is safe to call this function when java_process is None.
        - It is safe to call this function after the Java process has
          already terminated.
        - If the process is still running, terminate() is called and the
          function waits for the process to exit.
    """

    if java_process is None:
        print("⚠️ No Java process to close.")
        return

    if java_process.poll() is None:
        # Terminate Java process
        java_process.terminate()
        java_process.wait()
        print("✅ Java process terminated.")
    else:
        print("⚠️ Java process already terminated.")


def drain_stream(stream: io.TextIOBase, callback=None) -> None:
    """
    Consumes the output from a given stream until a specific marker is found,
    then closes the stream.

    This function is typically used to monitor the stdout or stderr of a subprocess
    (e.g., a Java process started from Python) and detect when a certain event occurs,
    such as the initialization of a gateway server. Once the marker line is encountered,
    the function prints it (or logs it) and terminates the stream reading.

    Args:
        stream (io.TextIOBase): A text-based stream object to read from, usually
                                subprocess.stdout or subprocess.stderr.
        callback (callable, optional): A function that takes a single string argument (line).
                                       It will be called for every line read from the stream.
                                       Useful for detecting specific markers, logging, or
                                       triggering events when certain output appears.

    Raises:
        AttributeError: If the provided `stream` does not have `readline` or `close` methods.
    """

    for line in iter(stream.readline, ""):
        line = line.strip()
        if callback:
            callback(line)

    stream.close()


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
