from src.utils.log import write_log
import socket


class PortConfiguration:

    def __init__(self) -> None:
        self.default_port = 8000
        self.reserved_ports = {5000, 7000}


    def check_port(self, port: int) -> bool:
        """
        Check if a given port is currently in use.

        Args:
            port (int): Port number to check.

        Returns:
            bool: True if the port is in use, False otherwise.
        """
        try:
            if port in self.reserved_ports:
                return True

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.settimeout(1)
                    s.connect(("localhost", port))
                    return True
                except (socket.timeout, ConnectionRefusedError):
                    return False
                
        except Exception as e:
            write_log("error", f"Failed to check port: {e}")


    def get_available_port(self) -> int:
        """
        Find an available port in the range 5001-9999 (excluding reserved ports).

        Returns:
            int: Available port number, or the default port if no available port is found.
        """
        try:
            for port in range(5001, 10000):
                if not self.check_port(port):
                    return port
            
            return self.default_port
        
        except Exception as e:
            write_log("error", f"Failed to get available port: {e}")


    def get_port(self) -> int:
        """
        Get the default port if it's available, otherwise find an available port.

        Returns:
            int: The port number to use.
        """
        try:
            if not self.check_port(self.default_port):
                write_log("info", "Starting interface on the default port 8000")
                return self.default_port
            else:
                available_port = self.get_available_port()
                write_log("info", f"Default port is in use, starting interface on port {available_port}")
                return available_port
        except Exception as e:
            write_log("error", f"Failed to get port: {e}")