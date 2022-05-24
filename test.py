import time

start = time.time()
print("hello"*100000000)
end = time.time()

print(end - start)