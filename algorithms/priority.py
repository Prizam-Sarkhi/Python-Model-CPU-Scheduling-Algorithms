class PriorityScheduler:
    def select(self, ready_q, current):
        if current is None and ready_q:
            lst = list(ready_q)
            lst.sort(key=lambda p:(p.priority, p.arrival_time))
            chosen = lst[0]; ready_q.remove(chosen); return chosen
        return current
