from multiprocessing import Pool, cpu_count
import time

def factorize(*numbers):
    results = []
    for number in numbers:
        factors = []
        for i in range(1, number + 1):
            if number % i == 0:
                factors.append(i)
        results.append(factors)
    return results

def factorize_parallel(*numbers):
    pool = Pool(cpu_count())
    results = pool.map(factorize, numbers)
    pool.close()
    pool.join()
    return results


if __name__ == '__main__':
    start_time = time.time()
    a, b, c, d = factorize(128, 255, 99999, 206510600)
    end_time = time.time()
    execution_time = end_time - start_time
    print("Один процес: ", execution_time)

    start_time_p = time.time()
    a, b, c, d = factorize_parallel(128, 255, 99999, 206510600) # 
    end_time_p = time.time()
    execution_time_p = end_time_p - start_time_p
    print("Мультипроцес: ", execution_time_p)
