"""Deterministic scheduling lesson; no network, money or persistent state."""
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier, Lock

def demonstrate(fixed):
    gate=Barrier(2);lock=Lock();state={'used':False}
    def redeem():
        if fixed:
            gate.wait(timeout=3)
            with lock:
                if state['used']:return False
                state['used']=True;return True
        permitted=not state['used']
        gate.wait(timeout=3)  # Both readers have observed the same old state.
        if permitted:state['used']=True
        return permitted
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures=[pool.submit(redeem) for _ in range(2)]
        return sum(f.result(timeout=5) for f in futures)

if __name__=='__main__':
    print('vulnerable successes:',demonstrate(False))
    print('fixed successes:',demonstrate(True))
