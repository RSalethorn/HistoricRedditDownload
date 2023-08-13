import psutil

class MemoryHandler:
    def __init__(self):
        self.process = psutil.Process()

        # How many mb of memory can be used by this process
        memory_allocated = 14000
        self.memory_allocated_bytes = memory_allocated * 1024 * 1024

    def is_memory_allocated_full(self):
        memory_info = self.process.memory_info()
        
        # Total memory used by HRD in bytes (SWAP inclusive)
        memory_used = memory_info.vms

        if (memory_used >= self.memory_allocated_bytes):
            return True
        else:
            return False