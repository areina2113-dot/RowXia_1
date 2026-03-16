import subprocess
import sys

video = sys.argv[1]

subprocess.run(["python","ai/stroke_ai.py",video])
