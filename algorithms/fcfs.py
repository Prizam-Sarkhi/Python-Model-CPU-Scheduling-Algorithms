class FCFSScheduler:
    def select(self, ready_q, current):
        if current is None and ready_q:
            return ready_q.popleft()
        return current
