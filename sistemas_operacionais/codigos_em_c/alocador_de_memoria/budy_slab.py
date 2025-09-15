import math
from dataclasses import dataclass
from typing import Optional, List, Dict

@dataclass
class Block:
    start: int
    size: int
    free: bool = True
    process_id: Optional[int] = None
    next: Optional['Block'] = None

class BuddySlabAllocator:
    def __init__(self, total_memory: int, min_block_size: int = 16):
        self.total_memory = total_memory
        self.min_block_size = min_block_size
        if self.total_memory < self.min_block_size:
            raise ValueError("Memória total deve ser maior ou igual ao tamanho mínimo de bloco")
        self.max_level = int(math.floor(math.log2(self.total_memory / self.min_block_size))) + 1
        self.free_lists: List[List[Block]] = [[] for _ in range(self.max_level)]
        self.free_lists[-1].append(Block(0, self.total_memory, True))
        self.allocated_blocks: Dict[int, Block] = {}
        print(f"Alocador Buddy Slab inicializado:")
        print(f"Memória total: {self.total_memory} bytes")
        print(f"Tamanho mínimo do bloco: {self.min_block_size} bytes")
        print(f"Níveis de buddy: {self.max_level}")
    
    def get_level(self, size: int) -> int:
        if size < self.min_block_size:
            size = self.min_block_size
        required_size = 2 ** math.ceil(math.log2(size))
        if required_size > self.total_memory:
            return -1
        level = int(math.log2(self.total_memory / required_size))
        return max(0, min(level, self.max_level - 1))
    
    def find_buddy_address(self, block: Block) -> int:
        return block.start ^ block.size
    
    def find_buddy(self, block: Block, level: int) -> Optional[Block]:
        buddy_address = self.find_buddy_address(block)
        for i, free_block in enumerate(self.free_lists[level]):
            if free_block.start == buddy_address and free_block.free:
                return free_block, i
        return None, -1
    
    def split_block(self, level: int) -> bool:
        if level <= 0:
            return False
        if not self.free_lists[level]:
            if not self.split_block(level + 1):
                return False
        block = self.free_lists[level].pop(0)
        new_size = block.size // 2
        self.free_lists[level - 1].append(Block(block.start, new_size, True))
        self.free_lists[level - 1].append(Block(block.start + new_size, new_size, True))
        return True
    
    def allocate(self, process_id: int, size: int) -> Optional[Block]:
        if process_id in self.allocated_blocks:
            print(f"Processo {process_id} já alocado.")
            return None
        if size > self.total_memory:
            print(f"Tamanho solicitado maior que memória total.")
            return None
        level = self.get_level(size)
        if level == -1:
            print(f"Não é possível alocar {size} bytes.")
            return None
        if not self.free_lists[level]:
            if not self.split_block(level + 1):
                print(f"Memória insuficiente para {size} bytes.")
                return None
        block = self.free_lists[level].pop(0)
        block.free = False
        block.process_id = process_id
        self.allocated_blocks[process_id] = block
        print(f"Alocado: Processo {process_id} → {block.size} bytes [{block.start}-{block.start + block.size - 1}]")
        return block
    
    def deallocate(self, process_id: int) -> bool:
        if process_id not in self.allocated_blocks:
            print(f"Processo {process_id} não encontrado.")
            return False
        block = self.allocated_blocks[process_id]
        level = self.get_level(block.size)
        block.free = True
        block.process_id = None
        self.free_lists[level].append(block)
        print(f"Memória liberada: Processo {process_id} → {block.size} bytes [{block.start}-{block.start + block.size - 1}]")
        self.coalesce(block, level)
        del self.allocated_blocks[process_id]
        return True
    
    def coalesce(self, block: Block, level: int):
        if level >= self.max_level - 1:
            return
        buddy, buddy_index = self.find_buddy(block, level)
        if buddy is not None and buddy.free:
            self.free_lists[level].remove(block)
            self.free_lists[level].pop(buddy_index)
            start = min(block.start, buddy.start)
            coalesced_block = Block(start, block.size * 2, True)
            self.free_lists[level + 1].append(coalesced_block)
            print(f"Coalescência: 2 blocos de {block.size} bytes → {coalesced_block.size} bytes")
            self.coalesce(coalesced_block, level + 1)
    
    def display_memory_state(self):
        print("\nEstado atual da memória:")
        for level in range(self.max_level):
            block_size = self.total_memory // (2 ** level)
            free_count = len(self.free_lists[level])
            if free_count:
                print(f"Nível {level} ({block_size} bytes): {free_count} blocos livres")
        print(f"Processos alocados: {list(self.allocated_blocks.keys())}\n")

def demo_buddy_slab():
    allocator = BuddySlabAllocator(total_memory=2048, min_block_size=32)
    allocator.display_memory_state()
    
    allocator.allocate(1, 100)
    allocator.allocate(2, 200)
    allocator.allocate(3, 50)
    allocator.display_memory_state()
    
    allocator.deallocate(2)
    allocator.deallocate(3)
    allocator.display_memory_state()
    
    allocator.allocate(4, 180)
    allocator.display_memory_state()
    
    for pid in list(allocator.allocated_blocks.keys()):
        allocator.deallocate(pid)
    allocator.display_memory_state()

if __name__ == "__main__":
    demo_buddy_slab()
