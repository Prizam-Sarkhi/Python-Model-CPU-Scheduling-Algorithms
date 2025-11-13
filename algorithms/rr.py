class RRScheduler:
    def __init__(self, tq): self.tq=tq; self.slice=0
    def select(self, ready_q, current):
        if current is None and ready_q:
            p=ready_q.popleft(); self.slice=min(self.tq,p.remaining_time); return p
        return current
    def tick(self): 
        if self.slice>0: self.slice-=1
