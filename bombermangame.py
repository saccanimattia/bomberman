import subprocess
import sys

def run_tests():
    """
    run test from unit_test.py thanks to unittest module
    """
    try:
        print("test execution...")
        result = subprocess.run([sys.executable, "-m", "unittest", "unit_test.py"], capture_output=True, text=True)
        if result.returncode == 0:
            print("all tests passed!")
            return True
        else:
            print("some test went wrong. Details:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"error during test execution: {e}")
        return False

def start_game():
    """
    start game `main.py`.
    """
    try:
        print("start the game...")
        subprocess.run([sys.executable, "main.py"])
    except Exception as e:
        print(f"error during game start: {e}")

if __name__ == "__main__":
    if run_tests():
        start_game()
    else:
        print("game can't start due to test failure")
