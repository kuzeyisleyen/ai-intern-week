import time

end = time.monotonic() + 5

counter = 0
while time.monotonic() < end:
    counter += 1

print("CPU demo tamamlandı.")
print("Iterations:", counter)