import sys

  
print("Argument List:", str(sys.argv))

query = sys.argv[1]
filename = f"Exam-{query}"
print(filename)