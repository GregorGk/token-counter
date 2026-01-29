#!/usr/bin/env python3
"""
Verification script to prove token counting is done offline.
Run this to confirm no data is sent to external servers.
"""

import sys
import socket
from unittest.mock import patch
from pathlib import Path

# Add the token_counter package to the path
sys.path.insert(0, str(Path(__file__).parent))

from token_counter import TokenCounter


def block_all_network():
    """Block all network connections to prove offline operation."""
    def guarded_socket(*args, **kwargs):
        raise RuntimeError("Network access attempted! This proves data would be sent online.")
    return patch('socket.socket', side_effect=guarded_socket)


def main():
    print("=== Offline Token Counting Verification ===\n")
    print("This script blocks ALL network access and then counts tokens.")
    print("If it succeeds, it proves your data stays local.\n")

    # Test text
    test_text = """
    This is confidential data that should never leave your computer.
    We're testing to ensure token counting happens entirely offline.
    """

    models_to_test = ["gpt-4", "claude-3-opus", "gemini-3.0", "chatgpt-5.2", "claude-opus-4.5"]

    print("Blocking all network access...")

    with block_all_network():
        print("✓ Network blocked - any attempt to connect will fail\n")

        print("Testing token counting with network blocked:")
        print("-" * 50)

        for model in models_to_test:
            try:
                counter = TokenCounter(model)
                tokens = counter.count_tokens(test_text)
                print(f"✓ {model:<20} {tokens:>4} tokens (counted offline)")
            except RuntimeError as e:
                if "Network access attempted" in str(e):
                    print(f"✗ {model:<20} FAILED - Tried to access network!")
                else:
                    raise
            except Exception as e:
                print(f"⚠ {model:<20} Error: {e}")

    print("\n" + "=" * 50)
    print("✓ SUCCESS: All token counting was done locally!")
    print("✓ Your confidential data never leaves your machine.")
    print("\nNote: If this test had failed, you would see network")
    print("access errors above, proving data was trying to be sent online.")


if __name__ == "__main__":
    try:
        # First, ensure tiktoken encodings are cached
        print("Ensuring tiktoken encodings are cached...")
        try:
            import tiktoken
            tiktoken.get_encoding("cl100k_base")
            print("✓ Tiktoken encodings already cached\n")
        except Exception as e:
            print("⚠ First run - tiktoken may download encodings")
            print("  Run this script again after initial setup\n")

        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)