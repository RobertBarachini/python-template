import psutil
from typing import cast


def kill_process(pid: int) -> bool:
	'''
	Kill a process by its PID.
	'''
	try:
		process = psutil.Process(pid)
		process.kill()
		print(f"Process {pid} killed.")
		return True
	except psutil.NoSuchProcess:
		print(f"Process {pid} not found.")
		return False
	except Exception as e:
		print(f"Failed to kill process {pid}: {e}")
		return False


def kill_process_and_children(pid: int) -> dict[int, bool]:
	'''
	Kill a process by its PID and its children.
	'''
	results = {}
	parent = cast(psutil.Process, None)

	try:
		parent = psutil.Process(pid)
	except psutil.NoSuchProcess:
		print(f"Process {pid} not found.")
		results[pid] = False
		return results

	for child in parent.children(recursive=True):
		try:
			child.kill()
			results[child.pid] = True
		except Exception as e:
			print(f"Failed to kill child process {child.pid}: {e}")
			results[child.pid] = False

	try:
		parent.kill()
		results[pid] = True
	except Exception as e:
		print(f"Failed to kill process {pid}: {e}")
		results[pid] = False

	return results
