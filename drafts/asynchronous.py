import multiprocessing


def second_thread(conn):
    while True:
        print("second loop")
        signal = conn.recv()
        if signal == "START":
            print("second thread")
            break


if __name__ == "__main__":
    parent_conn, child_conn = multiprocessing.Pipe()

    p = multiprocessing.Process(target=second_thread, args=(child_conn,))
    p.start()

    print("main thread")
    import time

    time.sleep(2)
    parent_conn.send("START")
