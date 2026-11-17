#!/usr/bin/env python3
"""Simple HTTP server for serving the ren.py game."""

import http.server
import socketserver
import os

PORT = 8000
DIRECTORY = os.path.join(os.path.dirname(__file__), "public")


class Handler(http.server.SimpleHTTPRequestHandler):
    """Handle requests with custom directory."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)


def run_server(port: int = PORT) -> None:
    """Start the HTTP server."""
    os.chdir(os.path.dirname(__file__) or ".")
    
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"Serving on http://localhost:{port}")
        print("Press Ctrl+C to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")


if __name__ == "__main__":
    run_server()
