"""
ShikshaKendra (शिक्षाकेंद्र) - SIH PS 26239
Ministry of Tribal Affairs (MoTA) AI-Enabled Scholarship & Fellowship Management Portal
Server Runner & Lifecycle Manager
"""
import os
import sys
import argparse
import socket
import webbrowser
import uvicorn

# Ensure UTF-8 output encoding for Windows terminal
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

def is_port_in_use(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex((host, port)) == 0

def main():
    parser = argparse.ArgumentParser(description="Run the ShikshaKendra MoTA Portal Server")
    parser.add_argument("--host", default=os.environ.get("HOST", "127.0.0.1"), help="Host address to bind (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", 8000)), help="Port to listen on (default: 8000)")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload on code changes")
    parser.add_argument("--open-browser", action="store_true", help="Automatically launch portal in default web browser")
    args = parser.parse_args()

    # Verify static directory exists
    static_dir = os.path.join(BASE_DIR, "app", "static")
    index_file = os.path.join(static_dir, "index.html")
    if not os.path.exists(index_file):
        print(f"[WARNING] Static UI file not found at: {index_file}")

    print("=" * 68)
    print("  ShikshaKendra (शिक्षाकेंद्र) | MoTA AI Scholarship Portal")
    print("  Smart India Hackathon (SIH) • Problem Statement 26239")
    print("=" * 68)
    print(f"  * Web Portal UI:        http://{args.host}:{args.port}")
    print(f"  * Interactive API Docs: http://{args.host}:{args.port}/docs")
    print(f"  * Database Snapshot:    {os.path.join(BASE_DIR, 'db_snapshot.json')}")
    print(f"  * 5-Count Garbage OCR:  ACTIVE (Auto-Sanitizing up to 5 tokens)")
    print(f"  * JAGO AI Voice Engine: ACTIVE (6 Vernacular Languages)")
    print("=" * 68)

    if is_port_in_use(args.host, args.port):
        print(f"\n[NOTICE] Port {args.port} is currently bound or active.")

    if args.open_browser:
        try:
            webbrowser.open(f"http://{args.host}:{args.port}")
        except Exception:
            pass

    try:
        uvicorn.run(
            "app.main:app",
            host=args.host,
            port=args.port,
            reload=args.reload,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n[INFO] Server stopped gracefully by user.")
    except Exception as e:
        print(f"\n[ERROR] Server execution halted: {e}")

if __name__ == "__main__":
    main()
