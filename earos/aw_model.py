import json
import multiprocessing
import os
import psutil
import shutil
import time
from transformers import pipeline


def unit_model_processor(result_queue, task_name="text-generation", model_type="gpt2",
                         params=["Hello earos", "Hello AW"]):
    pipe = pipeline(task=task_name, model=model_type)
    results = []
    for param in params:
        param = param[:50]
        res = pipe(param, truncation=True, max_length=100, pad_token_id=50256)
        for r in res:
            r = r["generated_text"]
            print(f"************ AI response ************\n{param}\n{r}")
        results.append(res)
    print(f"************ Collect AI response for contributions. Count: {len(results)}...************")
    result_queue.put(results)


def generate_progress_bar(percentage, length=30):
    filled_length = int(length * percentage / 100)
    bar = "█" * filled_length + "-" * (length - filled_length)
    return f"[{bar}] {percentage:.2f}%"


def format_output(cpu_usage, mem_usage, net_sent, net_recv):
    term_width = shutil.get_terminal_size().columns
    separator = "-" * term_width

    cpu_bar = generate_progress_bar(cpu_usage)
    mem_bar = generate_progress_bar(mem_usage)

    output = (
        f"\n{separator}\n"
        f"CPU Usage:  {cpu_bar}\n"
        f"Memory Usage: {mem_bar}\n"
        f"Net Sent:   {net_sent:.2f} KB/s\n"
        f"Net Recv:   {net_recv:.2f} KB/s\n"
        f"{separator}\n"
    )
    return output


def monitor_task(pid, interval=1):
    print(f"Monitoring process {pid} in process {os.getpid()}")
    try:
        process = psutil.Process(pid)
        prev_net = psutil.net_io_counters()
        prev_sent = prev_net.bytes_sent
        prev_recv = prev_net.bytes_recv

        while process.is_running():
            cpu_percent = psutil.cpu_percent(interval=interval, percpu=True)
            avg_cpu_percent = sum(cpu_percent) / len(cpu_percent)

            mem_info = process.memory_info()
            mem_percent = (mem_info.rss / psutil.virtual_memory().total) * 100

            current_net = psutil.net_io_counters()
            sent_diff = current_net.bytes_sent - prev_sent
            recv_diff = current_net.bytes_recv - prev_recv
            net_sent = sent_diff / 1024 / interval
            net_recv = recv_diff / 1024 / interval
            prev_sent = current_net.bytes_sent
            prev_recv = current_net.bytes_recv

            print(format_output(avg_cpu_percent, mem_percent, net_sent, net_recv))
            time.sleep(interval)
    except psutil.NoSuchProcess:
        print("Target process ended.")
    print("Monitoring stopped.")


def model_processor(task_func, task_args=None, monitor_interval=2.5):
    task_args = task_args or ()

    multiprocessing.set_start_method("spawn", force=True)
    result_queue = multiprocessing.Queue()
    task_args = task_args or ()
    args = (result_queue,) + tuple(task_args)
    task_process = multiprocessing.Process(target=task_func,
                                           args=args)
    task_process.start()

    monitor_process = multiprocessing.Process(target=monitor_task,
                                              args=(task_process.pid, monitor_interval))
    monitor_process.start()

    task_process.join()
    results = []
    while not result_queue.empty():
        results = result_queue.get()
        serialized_results = json.dumps(results, sort_keys=True)
        results = hash(serialized_results)

    if monitor_process.is_alive():
        monitor_process.terminate()
        monitor_process.join()
    print("Model processes have ended.")
    return results
